from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app import db
from app.models import Resource, ResourceTag
from app.forms import ResourceForm
from urllib.parse import urlparse

resources_bp = Blueprint("resources", __name__, template_folder="../templates")

# ----------------------------
# Resources List
# ----------------------------
@resources_bp.route("/resources")
def resources_list():
    page = request.args.get("page", 1, type=int)      
    pagination = Resource.query.order_by(Resource.id.desc()).paginate(
        page=page,
        per_page=10,
        error_out=False
    )

    return render_template("resources_list.html", 
                           resources=pagination.items,
                           pagination=pagination)

# ----------------------------
# Create resource
# ----------------------------
@login_required
@resources_bp.route("/resources/add", methods=["GET", "POST"])
def add_resource():

    form = ResourceForm()
    form.set_event_choices()

    if form.validate_on_submit():
        event_id = form.event_id.data if form.event_id.data != 0 else None
    
    parsed_url = urlparse(form.url.data)
    domain = parsed_url.netloc

    if form.validate_on_submit():
        
        resource = Resource(
            title=form.title.data,
            url=form.url.data,
            event_id=event_id,
            domain=domain,
            tag_id=form.tag.data
        )
        
        db.session.add(resource)
        db.session.commit()

        flash("Resource added!", "success")
        return redirect(url_for("resources.resources_list"))

    return render_template("resources_form.html", form=form)

# ----------------------------
# Delete Resource
# ----------------------------
@login_required
@resources_bp.route("/resources/delete/<int:resource_id>", methods=["POST"])
def delete_resource(resource_id):
    resource = Resource.query.get_or_404(resource_id)

    # Optional: only allow hosts or the user who created it
    if not current_user.is_host:
        flash("Not authorized.", "error")
        return redirect(url_for("resources.resources_list"))

    db.session.delete(resource)
    db.session.commit()

    flash("Resource deleted.", "success")
    return redirect(url_for("resources.resources_list"))
