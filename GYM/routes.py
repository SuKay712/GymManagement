from datetime import datetime, timedelta
import os
from flask import render_template, url_for, flash, redirect, request, abort
from GYM.form import RegistrationForm, LoginForm, UpdateAccountForm, AvailPlanForm, AddPlanForm, PaymentForm, AddEquipmentForm, AddCoachForm, UpdateCoachForm, UpdatePlanForm, UpdateEquipmentForm, RequestResetForm, ResetPasswordForm
from GYM.models import User, Plan, Equipment, Coach
from GYM import app, db, bcrypt, mail
from flask_mail import Message
from flask_login import login_user, current_user, logout_user, login_required
import secrets
from PIL import Image


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, phone=form.phone.data, password=hash_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title="Register", form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsucessful', 'danger')
    return render_template('login.html', title="Login", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))




def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        app.root_path, 'static/icon/avatar', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn
def isAdmin(username):
    if username == "admin":
        return True
    return False



@app.route("/user/profile", methods=['GET', 'POST'])
@login_required
def user():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password, form.current_password.data) and form.new_password.data == form.confirm_password.data:
            current_user.username = form.username.data
            current_user.email = form.email.data
            current_user.phone = form.phone.data
            hashed_password = bcrypt.generate_password_hash(
                form.new_password.data).decode('utf-8')
            current_user.password = hashed_password
            db.session.commit()
            flash('your account has been updated', 'success')
            return redirect(url_for('user'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.phone.data = current_user.phone
    image_file = url_for(
        'static', filename='icon/avatar/' + current_user.image_file)
    return render_template('user.html', title='User', image_file=image_file, form=form, username = current_user.username)


@app.route("/account")
@app.route("/account/profile", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password, form.current_password.data) and form.new_password.data == form.confirm_password.data:
            current_user.username = form.username.data
            current_user.email = form.email.data
            current_user.phone = form.phone.data
            hashed_password = bcrypt.generate_password_hash(
                form.new_password.data).decode('utf-8')
            current_user.password = hashed_password
            db.session.commit()
            flash('your account has been updated', 'success')
            return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.phone.data = current_user.phone
    image_file = url_for(
        'static', filename='icon/avatar/' + current_user.image_file)
    return render_template('adminProfile.html', title='Account', image_file=image_file, form=form, username = current_user.username)


@app.route("/account/availmember", methods=['POST', 'GET'])
@login_required
def avail_member():
    form = AvailPlanForm()
    plans = Plan.query.all()
    plans_name = [plan.name for plan in plans]
    form.plan.choices = plans_name
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash('1').decode('utf-8')
        plan = Plan.query.filter_by(name=form.plan.data).first()
        user = User(username=form.username.data,
                    email=form.email.data, phone=form.phone.data,
                    password=hash_password, plan=form.plan.data,
                    date_start=datetime.utcnow(), date_expired=datetime.utcnow() + plan.duration)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('dashboard'))
    return render_template('availMember.html', title='Avail Membership', form=form)


@app.route("/account/plan", methods=['POST', 'GET'])
@login_required
def plan():
    form = AddPlanForm()
    plans = Plan.query.all()
    if form.validate_on_submit():
        plan = Plan(name=form.name.data, duration=timedelta(
            days=form.duration.data), price=form.price.data)
        db.session.add(plan)
        db.session.commit()
        flash(f'Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('plan'))
    return render_template('plan.html', title='Plan', form=form, plans=plans)


@app.route("/account/payment", methods=['POST', 'GET'])
@login_required
def payment():
    form = PaymentForm()
    plans = Plan.query.all()
    plans_name = [plan.name for plan in plans]
    form.plan.choices = plans_name
    if form.validate_on_submit():
        user = User.query.filter_by(phone=form.phone.data).first()
        if user:
            user.plan = form.plan.data
            user.date_start = datetime.utcnow()
            plan = Plan.query.filter_by(name=form.plan.data).first()
            user.date_expired = datetime.utcnow() + plan.duration
            db.session.commit()
        flash(f'Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('payment'))
    return render_template('payment.html', title='Payment', form=form)


@app.route("/account/equipment", methods=['GET', 'POST'])
@login_required
def equipment():
    form = AddEquipmentForm()
    equipments = Equipment.query.all()
    if form.validate_on_submit():
        equipment = Equipment(name=form.name.data, quantity=form.quantity.data)
        db.session.add(equipment)
        db.session.commit()
        return redirect(url_for('equipment'))
    return render_template('inventory.html', title='Equipment', equipments=equipments, form=form)


@app.route("/account/coach", methods=['GET', 'POST'])
@login_required
def coach():
    form = AddCoachForm()
    coachs = Coach.query.all()
    if form.validate_on_submit():
        coach = Coach(name=form.name.data, phone=form.phone.data,
                      email=form.email.data)
        db.session.add(coach)
        db.session.commit()
        return redirect(url_for('coach'))
    return render_template('coach.html', title='Coach', coachs=coachs, form=form)


@app.route("/account/member", methods=['GET', 'POST'])
@login_required
def member():
    members = User.query.all()
    return render_template('member.html', title='Member', members=members)


@app.route("/account/update_coach<int:coach_id>", methods=['GET', 'POST'])
@login_required
def update_coach(coach_id):
    form = UpdateCoachForm()
    coach = Coach.query.get_or_404(coach_id)
    if form.validate_on_submit():
        coach.name = form.name.data
        coach.email = form.email.data
        coach.phone = form.phone.data
        db.session.commit()
        return redirect(url_for('coach'))
    elif request.method == 'GET':
        form.name.data = coach.name
        form.email.data = coach.email
        form.phone.data = coach.phone
    return render_template('updateCoach.html', title='Update Coach', form=form)


@app.route("/account/delete_coach<int:coach_id>", methods=['POST', 'GET'])
@login_required
def delete_coach(coach_id):
    coach = Coach.query.get_or_404(coach_id)
    db.session.delete(coach)
    db.session.commit()
    return redirect(url_for('coach'))



@app.route("/account/update_plan<int:plan_id>", methods=['GET', 'POST'])
@login_required
def update_plan(plan_id):
    form = UpdatePlanForm()
    plan = Plan.query.get_or_404(plan_id)
    if form.validate_on_submit():
        plan.name = form.name.data
        plan.duraion = timedelta(days=form.duration.data)
        plan.price = form.price.data
        db.session.commit()
        return redirect(url_for('plan'))
    elif request.method == 'GET':
        form.name.data = plan.name
        form.duration.data = plan.duraion.days
        form.price.data = plan.price
    return render_template('updatePlan.html', title='Update Plan', form=form)


@app.route("/account/delete_plan<int:plan_id>", methods=['POST', 'GET'])
@login_required
def delete_plan(plan_id):
    plan = Plan.query.get_or_404(plan_id)
    db.session.delete(plan)
    db.session.commit()
    return redirect(url_for('plan'))



@app.route("/account/update_equipment<int:equipment_id>", methods=['GET', 'POST'])
@login_required
def update_equipment(equipment_id):
    form = UpdateEquipmentForm()
    equipment = Equipment.query.get_or_404(equipment_id)
    if form.validate_on_submit():
        equipment.name = form.name.data
        equipment.quantity = form.quantity.data
        db.session.commit()
        return redirect(url_for('equipment'))
    elif request.method == 'GET':
        form.name.data = equipment.name
        form.quantity.data = equipment.quantity
    return render_template('updateEquipment.html', title='Update equipment', form=form)


@app.route("/account/delete_equipment<int:equipment_id>", methods=['POST', 'GET'])
@login_required
def delete_equipment(equipment_id):
    equipment = Equipment.query.get_or_404(equipment_id)
    db.session.delete(equipment)
    db.session.commit()
    return redirect(url_for('equipment'))


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='khoile712003@gmail.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
                {url_for('reset_token', token=token, _external=True)}

                    If you did not make this request then simply ignore this email and no changes will be made.
                '''
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('resetRequest.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('resetToken.html', title='Reset Password', form=form)
