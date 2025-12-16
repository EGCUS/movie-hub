from flask import jsonify, render_template
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
    
@community_bp.route("/communities", methods=["GET"])
def view_communities():
    communities = Community.query.order_by(Community.name.asc()).all()
    return render_template('list_communities.html', communities=communities)


