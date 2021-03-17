from flask import render_template, make_response, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash

# Local Modules
from .forms import LoginForm, RegisterForm
from .models import UserInfo
from app import app, db


# VIEW ROUTES -->
@app.route('/')
@login_required
def Home():
    username = current_user.username
    return render_template('index.html', user=username)


@app.route('/<string:name>')
def html_pages(name):
    try:
        if name == 'index':
            return redirect('/')
        return render_template(f'{name}.html')
    except:
        return page_not_found(name)


# LOGIN VIEW FUNCTION -->
@app.route('/login', methods=['GET', 'POST'])
def Login():
    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            user = UserInfo.query.filter_by(email = form.email.data).first()

            if user:
                if check_password_hash(user.password, form.password.data):
                    login_user(user)
                    return redirect(url_for('Home'))
                elif user.password != form.password.data:
                    flash('Invalid Password')
                elif user.email != form.email.data:
                    flash('Invalid Username')


    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def Register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')

        username = form.username.data
        email = form.email.data
        password = hashed_password

        new_register = UserInfo(username=username, email=email, password=password)
        db.session.add(new_register)
        db.session.commit()

        flash("Registration was successful")
        return redirect(url_for('Login'))

    return render_template('registration.html', form=form)


@app.route('/logout')
@login_required
def Logout():
    logout_user()
    return redirect(url_for('Login'))


# ERROR HANDLING -->
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html')


# SETTING AND GETTING COOKIES -->
@app.route('/set')
def set_cookie():
    response = make_response('I have set the cookie')
    response.set_cookie('myapp', 'Flask Web Development')

    return response


@app.route('/get')
def get_cookie():
    myapp = request.cookies.get('myapp')
    return f'Cookie Content Is {myapp}'
