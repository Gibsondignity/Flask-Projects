from gibson import app, db
from flask import render_template, url_for, redirect, flash
from gibson.forms import RegistrationForm, LoginForm
from gibson.models import User

@app.route("/")
@app.route("/home")
def homepage():
    return render_template('homepage.html', title='Home')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/account")
def account():
    return render_template('account.html', title='Account')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user=User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f"Account has been created successfully for {form.username.data}. Login Now!", category='success')
        return redirect(url_for("login"))

    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user:
            if form.password.data == user.password:
                flash(f"Login successful for {form.email.data} ", category='success')
                return redirect(url_for("account"))
        else:
            flash(f"Login unsuccessful for {form.email.data}. Email and password does not match! ", category='danger')
            return redirect(url_for("login"))
    return render_template('login.html', title='Login', form=form)










