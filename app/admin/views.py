from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
    send_file
)
from flask_login import current_user, login_required
from flask_rq import get_queue

from app import db, os
from app.admin.forms import (
    ChangeAccountTypeForm,
    Clearance1StatusForm,
    Clearance2StatusForm,
    Clearance3StatusForm,
    Clearance4StatusForm,
    ChangeUserEmailForm,
    InviteUserForm,
    NewUserForm,
    ClearanceExpirationForm,
    NewVolunteerForm,
    DownloadCSVForm,
    UploadCSVForm
)

from app.decorators import admin_required
from app.email import send_email
from app.models import EditableHTML, Role, User, Volunteer, Status

from .. import csrf
import csv
import io
import json
from datetime import datetime


admin = Blueprint('admin', __name__)


@admin.route('/')
@login_required
@admin_required
def index():
    """Admin dashboard page."""
    return render_template('admin/index.html')

@admin.route('/new-volunteer', methods=['GET', 'POST'])
@login_required
@admin_required
def new_volunteer():
    """Create a new volunteer."""
    form = NewVolunteerForm()
    if form.is_submitted():
        print("submitted")

    if form.validate_on_submit():
        print("valid")

    print(form.errors)
    if form.validate_on_submit():
        user = User(
            role_id=1,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password=form.password.data,
            phone_number=form.phone_number.data,
            street=form.street.data,
            city=form.city.data,
            state=form.state.data,
            zip_code = form.zip_code.data,
            organization_corporation=form.organization_corporation.data,
            pa_residency=form.pa_residency.data,
            confirmed = True)
        db.session.add(user)
        if form.pa_residency.data == "Yes":
            volunteer = Volunteer(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                phone_number=form.phone_number.data,
                address_street=form.street.data,
                address_city=form.city.data,
                address_state=form.state.data,
                address_zip_code = form.zip_code.data,
                organization = form.organization_corporation.data,
                year_pa = form.pa_residency.data,
                status1=Status.NOT_SUBMITTED,
                status2=Status.NOT_SUBMITTED,
                status3=Status.NOT_NEEDED,
                status4=Status.NOT_SUBMITTED
            )
        if form.pa_residency.data == "No":
            volunteer = Volunteer(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                phone_number=form.phone_number.data,
                address_street=form.street.data,
                address_city=form.city.data,
                address_state=form.state.data,
                address_zip_code = form.zip_code.data,
                organization = form.organization_corporation.data,
                year_pa = form.pa_residency.data,
                status1=Status.NOT_SUBMITTED,
                status2=Status.NOT_SUBMITTED,
                status3=Status.NOT_SUBMITTED,
                status4=Status.NOT_SUBMITTED
            )
        db.session.add(volunteer)
        db.session.commit()
        flash('Volunteer {} successfully created'.format(user.full_name()),
              'form-success')
        return redirect(url_for('main.index'))
    return render_template('admin/new_volunteer.html', form=form, is_volunteer=True)


@admin.route('/new-user', methods=['GET', 'POST'])
@login_required
@admin_required
def new_user():
    """Create a new user."""
    form = NewUserForm()
    if form.is_submitted():
        print("submitted")

    if form.validate_on_submit():
        print("valid")

    print(form.errors)
    if form.validate_on_submit():
        user = User(
            role=form.role.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password=form.password.data,
            confirmed=True)
        db.session.add(user)
        db.session.commit()
        flash('User {} successfully created'.format(user.full_name()),
              'form-success')
        return redirect(url_for('main.index'))
    return render_template('admin/new_user.html', form=form, is_volunteer=False)


@admin.route('/invite-user', methods=['GET', 'POST'])
@login_required
@admin_required
def invite_user():
    """Invites a new user to create an account and set their own password."""
    form = InviteUserForm()
    if form.validate_on_submit():
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        invite_link = url_for(
            'account.join_from_invite',
            user_id=user.id,
            token=token,
            _external=True)
        get_queue().enqueue(
            send_email,
            recipient=user.email,
            subject='You Are Invited To Join',
            template='account/email/invite',
            user=user,
            invite_link=invite_link,
        )
        flash('User {} successfully invited'.format(user.full_name()),
              'form-success')
    return render_template('admin/new_user.html', form=form)


@admin.route('/users')
@login_required
@admin_required
def registered_users():
    """View all registered users."""
    users = User.query.all()
    roles = Role.query.all()
    return render_template(
        'admin/registered_users.html', users=users, roles=roles)


@admin.route('/user/<int:user_id>')
@admin.route('/user/<int:user_id>/info')
@login_required
@admin_required
def user_info(user_id):
    """View a user's profile."""
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        abort(404)
    return render_template('admin/manage_user.html', user=user)


@admin.route('/user/<int:user_id>/change-email', methods=['GET', 'POST'])
@login_required
@admin_required
def change_user_email(user_id):
    """Change a user's email."""
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        abort(404)
    form = ChangeUserEmailForm()
    if form.validate_on_submit():
        user.email = form.email.data
        db.session.add(user)
        db.session.commit()
        flash('Email for user {} successfully changed to {}.'.format(
            user.full_name(), user.email), 'form-success')
    return render_template('admin/manage_user.html', user=user, form=form)


@admin.route(
    '/user/<int:user_id>/change-account-type', methods=['GET', 'POST'])
@login_required
@admin_required
def change_account_type(user_id):
    """Change a user's account type."""
    if current_user.id == user_id:
        flash('You cannot change the type of your own account. Please ask '
              'another administrator to do this.', 'error')
        return redirect(url_for('admin.user_info', user_id=user_id))

    user = User.query.get(user_id)
    if user is None:
        abort(404)
    form = ChangeAccountTypeForm()
    if form.validate_on_submit():
        user.role = form.role.data
        db.session.add(user)
        db.session.commit()
        flash('Role for user {} successfully changed to {}.'.format(
            user.full_name(), user.role.name), 'form-success')
    return render_template('admin/manage_user.html', user=user, form=form)


@admin.route('/user/<int:user_id>/delete')
@login_required
@admin_required
def delete_user_request(user_id):
    """Request deletion of a user's account."""
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        abort(404)
    return render_template('admin/manage_user.html', user=user)


@admin.route('/user/<int:user_id>/_delete')
@login_required
@admin_required
def delete_user(user_id):
    """Delete a user's account."""
    if current_user.id == user_id:
        flash('You cannot delete your own account. Please ask another '
              'administrator to do this.', 'error')
    else:
        user = User.query.filter_by(id=user_id).first()
        db.session.delete(user)
        db.session.commit()
        flash('Successfully deleted user %s.' % user.full_name(), 'success')
    return redirect(url_for('admin.registered_users'))


@admin.route('/_update_editor_contents', methods=['POST'])
@login_required
@admin_required
def update_editor_contents():
    """Update the contents of an editor."""

    edit_data = request.form.get('edit_data')
    editor_name = request.form.get('editor_name')

    editor_contents = EditableHTML.query.filter_by(
        editor_name=editor_name).first()
    if editor_contents is None:
        editor_contents = EditableHTML(editor_name=editor_name)
    editor_contents.value = edit_data

    db.session.add(editor_contents)
    db.session.commit()

    return 'OK', 200

@admin.route('/view_volunteers', methods=['GET', 'POST'])
@csrf.exempt
@login_required
@admin_required
def view_clearances():
    """View all volunteer clearances."""
    volunteers = Volunteer.query.all()
    now = datetime.now()
    exp_arr = []
    for v in volunteers:
        if v.clearance_expiration:
            split_arr = v.clearance_expiration.split('-')
            if len(split_arr) != 3:
                exp_arr.append("NA")
            else:
                exp = datetime(int(split_arr[0]), int(split_arr[1]), int(split_arr[2]))
                delta = now - exp
                if delta.days > -60:
                    exp_arr.append("Yes")
                else:
                    exp_arr.append("No")
        else:
            exp_arr.append("NA")


    """Download CSV with all volunteer information"""
    download_csv_form = DownloadCSVForm()
    upload_csv_form = UploadCSVForm()

    if request.method == 'POST':
        if request.form.get('download_csv'):

            csv_file = io.StringIO()
            csv_writer = csv.writer(csv_file)
            filename = 'volunteers' + datetime.now().strftime("%Y%m%d-%H%M%S") + '.csv'

            csv_writer.writerow(['First Name', 'Last Name', 'Email',
                                 'Phone Number', 'Address Street', 'City', 'State', 'Zip Code', 'Organization',
                                 'Over 10 years in PA', 'Clearance Expiration Date', 'PA State Police Check Status', 'Comment 1',
                                 '(Link) PA State Police Check',
                                 'PA Childlink','Comment 2','(Link) PA Childlink',
                                  'FBI Clearance', 'Comment 3',
                                 '(Link) FBI Clearance',
                                 'Conflict of Interest','Comment 4', '(Link) Conflict of Interest'])

            for v in volunteers:
                csv_writer.writerow([
                    v.first_name,
                    v.last_name,
                    v.email,
                    v.phone_number,
                    v.address_street,
                    v.address_city,
                    v.address_state,
                    v.address_zip_code,
                    v.organization,
                    v.year_pa,
                    v.clearance_expiration,

                    str(v.status1),
                    v.comment1,
                    v.link1,

                    str(v.status2),
                    v.comment2,
                    v.link2,

                    str(v.status3),
                    v.comment3,
                    v.link3,

                    str(v.status4),
                    v.comment4,
                    v.link4,])

            csv_bytes = io.BytesIO()
            csv_bytes.write(csv_file.getvalue().encode('utf-8'))
            csv_bytes.seek(0)

            # Send file for download.
            return send_file(csv_bytes,
                             as_attachment=True,
                             attachment_filename=filename,
                             mimetype='text/csv')
                
        else:
            f = request.files['volunteer-file']
            name = f.filename
            stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
            csv_input = csv.reader(stream)
            header_row = True

            for row in csv_input:
                if header_row:
                    header_row = False
                    continue
                    
                u = User(
                        first_name = row[0],
                        last_name = row[1],
                        email = row[2],
                        phone_number = row[3],
                        street = row[4],
                        city = row[5],
                        state = row[6],
                        zip_code = row[7],
                        organization_corporation = row[8],
                        pa_residency = row[9],
                        password = 'password',
                        confirmed = True,
                        role_id = 1)

                db.session.add(u)

                if 'Y' in row[9]:
                    status3 = Status.NOT_NEEDED
                else:
                    status3 = Status.NOT_SUBMITTED

                v = Volunteer(
                    first_name=row[0],
                    last_name=row[1],
                    email=row[2],
                    phone_number=row[3],
                    address_street=row[4],
                    address_city=row[5],
                    address_state=row[6],
                    address_zip_code = row[7],
                    organization=row[8],
                    year_pa=row[9],
                    clearance_expiration = row[10],
                    status1=Status.NOT_SUBMITTED,
                    comment1='',
                    link1='',
                    status2=Status.NOT_SUBMITTED,
                    comment2='',
                    link2='',
                    status3=status3,
                    comment3='',
                    link3='',
                    status4=Status.CLEARED,
                    comment4='',
                    link4='')

                db.session.add(v)

                try:
                    db.session.commit()
                except IntegrityError:
                    db.session.rollback()



    return render_template('admin/view_clearances.html', volunteers = volunteers, download_csv_form = download_csv_form, upload_csv_form = upload_csv_form, exp_arr = exp_arr)


@admin.route('/view_one/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def view_one(id):
    v_entry = Volunteer.query.filter_by(id=id).first()
    v_form1 = Clearance1StatusForm()
    v_form2 = Clearance2StatusForm()
    v_form3 = Clearance3StatusForm()
    v_form4 = Clearance4StatusForm()

    expiration_date_form = ClearanceExpirationForm(clearance_expiration=v_entry.clearance_expiration)

    if expiration_date_form.submit_expiration_date.data and expiration_date_form.validate():
        if "submit_expiration_date" in request.form.keys():
            v_entry.clearance_expiration = expiration_date_form.clearance_expiration.data
            db.session.commit()

    if v_form1.submit_clearance_1.data and v_form1.validate():
        if "submit_clearance_1" in request.form.keys():
            v_entry.status1 = v_form1.new_status_1.data
        if v_form1.comment_1.data != '':
            v_entry.comment1 = v_form1.comment_1.data
        if v_form1.form1_file_urls.data != '':
            v_entry.link1 = v_form1.form1_file_urls.data
            if v_entry.status1 != Status.SUBMITTED:
                v_entry.status1 = Status.SUBMITTED
        db.session.commit()

    if v_form2.submit_clearance_2.data and v_form2.validate():
        if "submit_clearance_2" in request.form.keys():
            v_entry.status2 = v_form2.new_status_2.data
        if v_form2.comment_2.data != '':
            v_entry.comment2 = v_form2.comment_2.data
        if v_form2.form2_file_urls.data != '':
            v_entry.link2 = v_form2.form2_file_urls.data
            if v_entry.status2 != Status.SUBMITTED:
                v_entry.status2 = Status.SUBMITTED
        db.session.commit()

    if v_form3.submit_clearance_3.data and v_form3.validate():
        if "submit_clearance_3" in request.form.keys():
            v_entry.status3 = v_form3.new_status_3.data
        if v_form3.comment_3.data != '':
            v_entry.comment3 = v_form3.comment_3.data
        if v_form3.form3_file_urls.data != '':
            v_entry.link3 = v_form3.form3_file_urls.data
            if v_entry.status3 != Status.SUBMITTED:
                v_entry.status3 = Status.SUBMITTED
        db.session.commit()

    if v_form4.submit_clearance_4.data and v_form4.validate():
        if "submit_clearance_4" in request.form.keys():
            v_entry.status4 = v_form4.new_status_4.data
        if v_form4.comment_4.data != '':
            v_entry.comment4 = v_form4.comment_4.data
        if v_form4.form4_file_urls.data != '':
            v_entry.link4 = v_form4.form4_file_urls.data
            if v_entry.status4 != Status.SUBMITTED:
                v_entry.status4 = Status.SUBMITTED
        db.session.commit()

    return render_template('admin/view_one.html', v_entry=v_entry, v_form1=v_form1,
                           v_form2=v_form2, v_form3=v_form3, v_form4=v_form4,
                           expiration_date_form=expiration_date_form)
