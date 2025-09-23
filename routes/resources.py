from flask import Blueprint, render_template
from flask_login import login_required

resources_bp = Blueprint("resources", __name__)

@resources_bp.route("/resources")
@login_required
def resources():
    # For now, just some placeholder resources
    dummy_resources = [
        {"title": "Campus Magazine - August Edition", "description": "Latest campus happenings and articles.", "file": "#"},
        {"title": "Case Study Compendium", "description": "Collection of top case studies for practice.", "file": "#"},
        {"title": "Research Paper: Analytics in Business", "description": "An in-depth look at analytics strategies.", "file": "#"}
    ]
    return render_template("resources.html", resources=dummy_resources)
