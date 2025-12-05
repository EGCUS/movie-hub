import hashlib
import os
import tempfile
from datetime import datetime, timezone
import uuid
from zipfile import ZipFile
import json
import logging

from flask_login import current_user, login_required
from app import db
from app.modules.featuremodel.models import FMMetaData, FeatureModel
from app.modules.hubfile.models import Hubfile
from app.modules.movie.forms import MovieEditMetadataForm, MovieForm
from app.modules.movie.models import Movie, MovieDataset
from app.modules.dataset.models import DSMetaData, Author, DSDownloadRecord
from app.modules.fakenodo.adapter import FakenodoAdapter
from flask import render_template, request, redirect, url_for, flash, jsonify, abort, make_response, send_from_directory

logger = logging.getLogger(__name__)




from app.modules.movie import movie_bp
from app.modules.movie.forms import MovieForm
from app.modules.movie.services import MovieService
from app.modules.dataset.services import (
    AuthorService,
    DataSetService,
    DOIMappingService,
    DSDownloadRecordService,
    DSMetaDataService,
    DSViewRecordService,
)

dataset_service = DataSetService()
author_service = AuthorService()
dsmetadata_service = DSMetaDataService()
doi_mapping_service = DOIMappingService()
ds_view_record_service = DSViewRecordService()


movie_service = MovieService()
fakenodo_adapter = FakenodoAdapter()

#GET MOVIES
@movie_bp.route('/moviedataset', methods=['GET'])
def index():
    """Redirect to list all movie datasets"""
    return redirect(url_for('movie.list_datasets'))

@movie_bp.route("/moviedataset/list", methods=["GET"])
def list_datasets():
    datasets = movie_service.get_all_moviedatasets()
    
    return render_template(
        "movie/list_datasets.html",
        datasets=datasets
    )

#GET MY DATASETS
@movie_bp.route("/moviedataset/my-datasets", methods=["GET"])
@login_required
def my_datasets():
    #Obtengo los datasets de usuario act
    synchronized_datasets = movie_service.get_moviedataset_by_user(current_user.id)
    return render_template(
        "movie/my_datasets.html",
        synchronized_datasets=synchronized_datasets,
    )


@movie_bp.route("/moviedataset/<int:dataset_id>", methods=["GET"])
def view_dataset(dataset_id):
    """View a movie dataset with all its movies (public view)"""
    dataset = movie_service.get_moviedataset(dataset_id)
    user_cookie = ds_view_record_service.create_cookie(dataset=dataset)
    resp = make_response(render_template("movie/view_dataset.html", dataset=dataset))
    resp.set_cookie("view_cookie", user_cookie)
    
    return resp

# Manage
@movie_bp.route("/moviedataset/<int:dataset_id>/manage", methods=["GET"])
@login_required
def manage_dataset(dataset_id):
    dataset = movie_service.get_moviedataset(dataset_id)
    
    if dataset.user_id != current_user.id:
        abort(403, "You don't have permission to manage this dataset")
    
    return render_template(
        "movie/manage_dataset.html",
        dataset=dataset
    )

# Para ver los detalles de la pelÃ­cula
@movie_bp.route("/movie/<int:movie_id>", methods=["GET"])
def view_movie(movie_id):
    movie = movie_service.get_movie(movie_id)
    dataset = movie.dataset
    
    return render_template(
        "movie/view_movie.html",
        movie=movie,
        dataset=dataset
    )

@movie_bp.route("/moviedataset/<int:dataset_id>/download", methods=["GET"])
def download_dataset(dataset_id):
    dataset = movie_service.get_moviedataset(dataset_id)

    from app.modules.fakenodo.models import Fakenodo
    fakenodo = Fakenodo.query.filter_by(dataset_id=dataset.id).first()

    temp_dir = tempfile.mkdtemp()
    zip_path = os.path.join(temp_dir, f"movie_dataset_{dataset_id}.zip")

    if fakenodo and fakenodo.dataset_file_path and os.path.exists(fakenodo.dataset_file_path):
        with ZipFile(zip_path, "w") as zipf:
            # Recorrer todos los archivos dentro de la carpeta de Fakenodo
            for subdir, dirs, files in os.walk(fakenodo.dataset_file_path):
                for file in files:
                    full_path = os.path.join(subdir, file)
                    # Mantener estructura relativa dentro del ZIP
                    relative_path = os.path.relpath(full_path, fakenodo.dataset_file_path)
                    zipf.write(full_path, arcname=relative_path)
                    logger.info(f"Added to ZIP from Fakenodo: {relative_path}")

    else:
        file_path = f"uploads/user_{dataset.user_id}/dataset_{dataset.id}/"

        if not os.path.exists(file_path):
            abort(404, "No se encontró el dataset ni en Fakenodo ni en archivos locales")

        with ZipFile(zip_path, "w") as zipf:
            for subdir, dirs, files in os.walk(file_path):
                for file in files:
                    full_path = os.path.join(subdir, file)
                    relative_path = os.path.relpath(full_path, file_path)
                    zipf.write(full_path, arcname=relative_path)

    user_cookie = request.cookies.get("download_cookie")
    if not user_cookie:
        user_cookie = str(uuid.uuid4())

    existing_record = DSDownloadRecord.query.filter_by(
        user_id=current_user.id if current_user.is_authenticated else None,
        dataset_id=dataset_id,
        download_cookie=user_cookie,
    ).first()

    if not existing_record:
        DSDownloadRecordService().create(
            user_id=current_user.id if current_user.is_authenticated else None,
            dataset_id=dataset_id,
            download_date=datetime.now(timezone.utc),
            download_cookie=user_cookie,
        )

    resp = send_from_directory(
        temp_dir,
        f"movie_dataset_{dataset_id}.zip",
        as_attachment=True,
        mimetype="application/zip",
    )

    if not request.cookies.get("download_cookie"):
        resp.set_cookie("download_cookie", user_cookie)

    return resp

@movie_bp.route("/moviedataset/upload", methods=["GET", "POST"])
@login_required
def upload_dataset():
    form = MovieForm()

    if request.method == 'GET':
        if len(form.authors) == 0:
            form.authors.append_entry({
                'name': f"{current_user.profile.surname}, {current_user.profile.name}",
                'affiliation': current_user.profile.affiliation or '',
                'orcid': current_user.profile.orcid or ''
            })

    if form.validate_on_submit():
        try:
            logger.info("=== Starting dataset upload ===")
            
            movie_dataset, total_movies = movie_service.upload_and_publish_dataset( 
                form=form,
                current_user=current_user,
                dsmetadata_service=dsmetadata_service
            )
            
            logger.info(f"Dataset {movie_dataset.id} uploaded successfully with {total_movies} movies")
            flash(f'Dataset uploaded successfully! {total_movies} movies from {len(form.file.data)} files 🎬', 'success')
            return redirect(url_for('movie.view_dataset', dataset_id=movie_dataset.id))

        except ValueError as e:
            logger.error(f"Validation error: {str(e)}")
            flash(f'Error: {str(e)}', 'error')
        except Exception as e:
            db.session.rollback()
            logger.exception("Error in upload_dataset")
            flash(f'Error uploading dataset: {str(e)}', 'error')

    return render_template("movie/upload_dataset.html", form=form)


@movie_bp.route("/moviedataset/file/upload", methods=["POST"])
@login_required
def upload_file():
    """
    Quick file validation endpoint (optional, for AJAX previews)
    """
    try:
        file = request.files.get("file")
        if not file:
            return jsonify({"error": "No file provided"}), 400
        
        if not file.filename.endswith('.json'):
            return jsonify({"error": "Only JSON files allowed"}), 400
        
        # Validar JSON
        content = file.read()
        try:
            data = json.loads(content)
            movie_count = len(data.get('movies', []))
            return jsonify({
                "success": True,
                "filename": file.filename,
                "movie_count": movie_count
            }), 200
        except:
            return jsonify({"error": "Invalid JSON"}), 400
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@movie_bp.route("/moviedataset/file/delete", methods=["POST"])
@login_required
def delete_file():
    """
    TODO
    """
    return jsonify({"message": "File deletion temporarily disabled"}), 501

# SELECT VERSION SCREEN
@movie_bp.route("/moviedataset/<int:dataset_id>/versions", methods=["GET"])
def select_versions(dataset_id):
    """
    Muestra todas las versiones disponibles de un dataset y permite seleccionar dos para comparar.
    """
    dataset = movie_service.get_moviedataset(dataset_id)

    # Versions reales del dataset (tabla Version)
    versions = sorted(dataset.versions, key=lambda v: v.created_at, reverse=True)

    return render_template(
        "movie/select_versions.html",
        dataset=dataset,
        versions=versions
    )


# JSON: COMPARE TWO VERSIONS
@movie_bp.route("/moviedataset/version/<int:v1_id>/compare/<int:v2_id>", methods=["GET"])
def compare_versions_json(v1_id, v2_id):
    """
    Compara dos versiones usando snapshots y devuelve JSON.
    """
    dataset_v1 = movie_service.load_dataset_from_version(v1_id)
    dataset_v2 = movie_service.load_dataset_from_version(v2_id)

    comparison = movie_service.compare_datasets(dataset_v1, dataset_v2)

    return jsonify({
        "version_1": v1_id,
        "version_2": v2_id,
        "comparison": comparison
    })


# HTML: COMPARE TWO VERSIONS (VIEW)
@movie_bp.route("/moviedataset/version/<int:v1_id>/compare/<int:v2_id>/view", methods=["GET"])
def compare_versions_view(v1_id, v2_id):

    # Cargar versiones reconstruidas desde snapshot
    v1 = movie_service.load_dataset_from_version(v1_id)
    v2 = movie_service.load_dataset_from_version(v2_id)

    # ComparaciÃ³n real entre versiones
    comparison = movie_service.compare_version_ids(v1_id, v2_id)

    return render_template(
        "movie/compare_versions.html",
        v1=v1,
        v2=v2,
        comparison=comparison
    )


@movie_bp.route("/doi/<path:doi>/", methods=["GET"])
def movie_doi_view(doi):
    """
    View a movie dataset by its DOI
    """
    # Buscar el dataset por DOI
    ds_meta_data = dsmetadata_service.filter_by_doi(doi)
    
    if not ds_meta_data:
        abort(404, "Dataset not found")
    
    dataset = ds_meta_data.dataset
    
    # Verificar que sea un MovieDataset
    if not isinstance(dataset, MovieDataset):
        abort(404, "Not a movie dataset")
    
    # Crear cookie de visualización
    user_cookie = ds_view_record_service.create_cookie(dataset=dataset)
    resp = make_response(render_template("movie/view_dataset.html", dataset=dataset))
    resp.set_cookie("view_cookie", user_cookie)
    
    return resp



