from flask import jsonify, render_template, request

from app.modules.explore import explore_bp
from app.modules.explore.forms import ExploreForm
from app.modules.explore.services import ExploreService
from app.modules.community.models import Community
from flask import jsonify, render_template, request, url_for


@explore_bp.route("/explore", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        query = request.args.get("query", "")
        form = ExploreForm()
        return render_template("explore/index.html", form=form, query=query)

    if request.method == "POST":
        criteria = request.get_json()
        datasets = ExploreService().filter(**criteria)
        return jsonify([dataset.to_dict() for dataset in datasets])


@explore_bp.route("/explore/communities", methods=["GET"])
def list_communities():
    communities = Community.query.order_by(Community.name).all()

    def build_logo_url(c: Community):
        # Si en BD guardas solo el nombre del fichero
        if c.logo_url:
            return url_for("static", filename=f"img/community/{c.logo_url}")
        # Default local
        return url_for("static", filename="img/community/default.svg")

    return jsonify([
        {
            "id": c.id,
            "name": c.name,
            "logo_url": build_logo_url(c),
        }
        for c in communities
    ])
