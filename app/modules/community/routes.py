from flask import jsonify
from app.modules.community import community_bp
from app.modules.community.models import Community


@community_bp.route("/api/communities", methods=["GET"])
def list_communities():
    communities = Community.query.order_by(Community.name.asc()).all()
    return jsonify([{
        "id": c.id,
        "name": c.name,
        "logo_url": c.logo_url
    } for c in communities]), 200
