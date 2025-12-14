import hashlib
import os
import tempfile
from datetime import datetime, timezone
import uuid
from zipfile import ZipFile
import json
import logging

from app.modules.community.models import Community
from werkzeug.utils import secure_filename
from flask import current_app
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


@movie_bp.route("/moviedataset/my-datasets", methods=["GET"])
@login_required
def my_datasets():
    """Obtiene los datasets del usuario separados por estado de publicación"""
    # Usar los métodos del servicio que ya existen
    synchronized_datasets = movie_service.get_moviedataset_by_user(current_user.id)
    unsynchronized_datasets = movie_service.get_unsynchronized_datasets_by_user(current_user.id)

    return render_template(
        "movie/my_datasets.html",
        synchronized_datasets=synchronized_datasets,
        unsynchronized_datasets=unsynchronized_datasets
    )


@movie_bp.route("/moviedataset/<int:dataset_id>/publish", methods=["POST"])
@login_required
def publish_dataset(dataset_id):
    """Publica un dataset en Fakenodo"""
    try:
        dataset = movie_service.get_moviedataset(dataset_id)

        # Verificar permisos
        if dataset.user_id != current_user.id:
            return jsonify({"error": "You don't have permission to publish this dataset"}), 403

        # Buscar Fakenodo asociado
        from app.modules.fakenodo.models import Fakenodo
        fakenodo = Fakenodo.query.filter_by(dataset_id=dataset.id).first()

        if not fakenodo:
            return jsonify({"error": "Fakenodo record not found for this dataset"}), 404

        # Publicar en Fakenodo - esto ya verifica todo y actualiza
        published_fakenodo = fakenodo_adapter.publish_fakenodo(fakenodo.id)

        flash('Dataset published successfully in Fakenodo!', 'success')
        return jsonify({
            "message": "Dataset published successfully",
            "doi": published_fakenodo.doi,
            "status": published_fakenodo.status
        }), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.exception("Error publishing dataset")
        return jsonify({"error": f"Error publishing dataset: {str(e)}"}), 500


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

    communities = Community.query.order_by(Community.name.asc()).all()
    form.community_id.choices = [(0, "Any")] + [(c.id, c.name) for c in communities]

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

            # ==========================================
            # COMMUNITY: existing or new
            # ==========================================
            selected_community_id = form.get_selected_community_id()

            new_name = (form.new_community_name.data or "").strip()
            new_logo = form.new_community_logo.data

            if new_name:
                existing = Community.query.filter_by(name=new_name).first()
                if existing:
                    selected_community_id = existing.id
                else:
                    logo_filename = None

                    # Guardar logo si viene
                    if new_logo and getattr(new_logo, "filename", ""):
                        logo_dir = os.path.join(current_app.static_folder, "img", "community")
                        os.makedirs(logo_dir, exist_ok=True)

                        original = secure_filename(new_logo.filename)
                        ext = os.path.splitext(original)[1].lower()

                        logo_filename = f"community_{uuid.uuid4().hex}{ext}"
                        save_path = os.path.join(logo_dir, logo_filename)

                        new_logo.save(save_path)

                    new_c = Community(name=new_name, logo_url=logo_filename)
                    db.session.add(new_c)
                    db.session.flush()
                    selected_community_id = new_c.id


            # Detectar qué botón se presionó
            action = request.form.get('action')  # 'draft' o 'publish'

            if action == 'publish':
                # Publica
                logger.info("Action: Upload and Publish")
                movie_dataset, total_movies = movie_service.upload_and_publish_dataset(
                    form=form,
                    current_user=current_user,
                    dsmetadata_service=dsmetadata_service,
                    community_id=selected_community_id
                )
                action_text = 'publish'
            else:
                #   Manda a draft
                logger.info("Action: Save as Draft")
                movie_dataset, total_movies, _ = movie_service.upload_draft_dataset(
                    form=form,
                    current_user=current_user,
                    dsmetadata_service=dsmetadata_service,
                    community_id=selected_community_id
                )
                action_text = 'draft'

            logger.info(f"Dataset {movie_dataset.id} processed successfully with {total_movies} movies")

            return redirect(url_for(
                'movie.upload_dataset',
                success='true',
                action=action_text,
                dataset_id=movie_dataset.id
            ))

        except ValueError as e:
            logger.error(f"Validation error: {str(e)}")
            flash(f'Error: {str(e)}', 'error')
        except Exception as e:
            db.session.rollback()
            logger.exception("Error in upload_dataset")
            flash(f'Error uploading dataset: {str(e)}', 'error')

    return render_template("movie/upload_dataset.html", form=form)


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

    # Filtrar versiones con snapshot.json válido
    from app.modules.dataset.base_dataset import Version
    import os

    versions = (
        Version.query
        .filter_by(dataset_id=dataset.id)
        .filter(Version.snapshot_path.isnot(None))
        .all()
    )

    # solo las que existen en disco
    versions = [
        v for v in versions
        if os.path.exists(v.snapshot_path)
    ]

    versions.sort(key=lambda v: v.created_at, reverse=True)

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

    comparison = movie_service.compare_version_ids(v1_id, v2_id)

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


@movie_bp.route("/moviedataset/<int:dataset_id>/changelog", methods=["GET"])
def view_changelog(dataset_id):
    """
    Muestra el historial de cambios menores del dataset.
    """
    dataset = movie_service.get_moviedataset(dataset_id)
    change_history = movie_service.get_change_history(dataset_id)

    return render_template(
        "movie/changelog.html",
        dataset=dataset,
        changes=change_history
    )


@movie_bp.route("/api/moviedataset/<int:dataset_id>/changelog", methods=["GET"])
def api_changelog(dataset_id):
    #CAMBIOS EN JSON
    dataset = movie_service.get_moviedataset(dataset_id)
    change_history = movie_service.get_change_history(dataset_id)

    return jsonify({
        "dataset_id": dataset_id,
        "dataset_title": dataset.ds_meta_data.title,
        "changes": [change.to_dict() for change in change_history]
    })


@movie_bp.route("/moviedataset/<int:dataset_id>/edit", methods=["GET", "POST"])
@login_required
def edit_dataset_metadata(dataset_id):
    dataset = movie_service.get_moviedataset(dataset_id)

    if dataset.user_id != current_user.id:
        abort(403, "You don't have permission to edit this dataset")

    form = MovieEditMetadataForm()

    if request.method == 'GET':
        form.title.data = dataset.ds_meta_data.title
        form.desc.data = dataset.ds_meta_data.description
        form.tags.data = dataset.ds_meta_data.tags

        # Prellenar autores
        while len(form.authors) > 0:
            form.authors.pop_entry()

        for author in dataset.ds_meta_data.authors:
            form.authors.append_entry({
                "name": author.name,
                "affiliation": author.affiliation or "",
                "orcid": author.orcid or "",
            })

    if form.validate_on_submit():
        try:

            new_authors = form.get_authors()

            # Proteger primer autor
            main = dataset.ds_meta_data.authors[0]
            new_authors[0] = {'name': main.name, 'affiliation': main.affiliation, 'orcid': main.orcid}

            metadata_changed = movie_service.edit_metadata(
                dataset, form.title.data, form.desc.data,
                form.tags.data, current_user.id, form.edit_comment.data
            )

            authors_changed = movie_service.edit_authors(
                dataset, new_authors, current_user.id, form.edit_comment.data
            )

            db.session.commit()

            flash('Dataset updated successfully!' if (metadata_changed or authors_changed)
                  else 'No changes made', 'success' if (metadata_changed or authors_changed) else 'info')

            return redirect(url_for('movie.view_dataset', dataset_id=dataset.id))

        except ValueError as e:
            db.session.rollback()
            flash(str(e), 'warning')

        except Exception as e:
            db.session.rollback()
            logger.exception("Error editing dataset")
            flash(f'Error: {str(e)}', 'error')

    return render_template("movie/edit_dataset.html", form=form, dataset=dataset)
