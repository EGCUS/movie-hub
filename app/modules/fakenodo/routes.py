from flask import render_template, request, jsonify
from app.modules.fakenodo import fakenodo_bp
from app.modules.fakenodo.models import Fakenodo
from app.modules.fakenodo.services import FakenodoService
from app import db
import uuid


@fakenodo_bp.route("/fakenodo", methods=["GET"])
def index():
    return render_template("fakenodo/index.html")

@fakenodo_bp.route("/fakenodo", methods=["POST"])
def publish():
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "Missing field 'title'"}), 400
    fake_doi = f"10.1234/moviehub.fake.{uuid.uuid4().hex[:8]}"

    new_node = Fakenodo(
        movie_metadata=data,
        status="published",
        doi=fake_doi
    )

    db.session.add(new_node)
    db.session.commit()

    return jsonify({
        "message": f"Movie '{data['title']}' published succesfully!",
        "id": new_node.id,
        "status": new_node.status,
        "doi": new_node.doi
    }), 201

    