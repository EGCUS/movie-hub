from flask import render_template, request, jsonify
from app.modules.fakenodo import fakenodo_bp
from app.modules.fakenodo.models import Fakenodo
from app.modules.fakenodo.services import FakenodoService
from app import db
import uuid


@fakenodo_bp.route("/fakenodo", methods=["GET"])
def index():
    return render_template("fakenodo/index.html")

@fakenodo_bp.route("/fakenodo/publish/<int:fakenodo_id>", methods=["POST"])
def publish(fakenodo_id):
    try:
        service = FakenodoService()
        fakenodo = service.publish_fakenodo(fakenodo_id)

        return jsonify({
            "message": f"Fakenodo {fakenodo_id} published successfully!",
            "id": fakenodo.id,
            "status": fakenodo.status,
            "doi": fakenodo.doi
        }), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

@fakenodo_bp.route("/fakenodo/<int:fakenodo_id>", methods=["GET"])
def getOne(fakenodo_id):
    try:
        service = FakenodoService()
        data = service.get_fakenodo(fakenodo_id)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404
