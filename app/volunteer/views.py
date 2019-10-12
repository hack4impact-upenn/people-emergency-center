from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required
from flask_rq import get_queue

from app import db
from app.decorators import volunteer_required
from app.models import EditableHTML, Role, User

volunteer = Blueprint('volunteer', __name__)

@volunteer.route('/')
@login_required
@volunteer_required
def index():
    """Volunteer dashboard page."""
    return render_template('volunteer/index.html')

@volunteer.route('/upload_clearances')
@login_required
@volunteer_required
def upload_clearances():
    return render_template('volunteer/upload_clearances.html')
