from flask import (
    Blueprint,
    render_template,
)
from flask_login import login_required

from app.decorators import staff_required
from app.models import Volunteer, Status

staff = Blueprint('staff', __name__)


@staff.route('/')
@login_required
@staff_required
def index():
    """Volunteer dashboard page."""
    return render_template('staff/index.html')


@staff.route('/view_volunteers', methods=['GET', 'POST'])
@login_required
@staff_required
def view_volunteers():
    """View all volunteers."""
    volunteers = Volunteer.query.filter(Volunteer.status1 == Status.CLEARED,
                                        Volunteer.status2 == Status.CLEARED,
                                        Volunteer.status3 == Status.CLEARED,
                                        Volunteer.status3 == Status.NOT_NEEDED,
                                        Volunteer.status4 == Status.CLEARED,)
    return render_template('staff/view_volunteers.html', volunteers=volunteers)


@staff.route('/view_one/<int:id>', methods=['GET'])
@login_required
@staff_required
def view_one(id):
    volunteer = Volunteer.query.get(id)
    return render_template('staff/view_one.html', volunteer=volunteer)
