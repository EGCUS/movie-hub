from core.blueprints.base_blueprint import BaseBlueprint

community_bp = BaseBlueprint(
    "community",
    __name__,
    template_folder="templates",
    static_folder="assets"
)

from app.modules.community import models  # registra Community
from app.modules.community import routes  # registra el blueprint
