from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user



app = Flask(__name__)
app.config["SECRET_KEY"] = 'kjghKGIykgVKGIUG2U987s'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///loginModels.db"
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'loginpage'
 

posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]
class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember')

class RegisterForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    email = StringField('email', validators=[InputRequired(), Email(message="Invalid email"), Length(max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    




class login(UserMixin, db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(25), nullable=False)

    def __repr__(self):
        return "Name: " + self.username + " and ID: "+ str(self.id)


@login_manager.user_loader
def load_user(user_id):
    return login.query.get(int(user_id))

@app.route("/")
def index():

    return render_template("dashboard.html")


@app.route("/login", methods=["POST", "GET"])
def loginpage():
    form = LoginForm()
    if form.validate_on_submit():
        user = login.query.filter_by(username=form.username.data).first()
            
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('mypage'))
        
        return '<h1> Invalid username and password </h1>'
            

    return render_template("login.html", form=form)


@app.route("/signup", methods=["POST", "GET"])
def signup():
    form = RegisterForm() 

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method="sha256")
        new_user = login(username=form.username.data, email=form.email.data, password=hashed_password)
        #return '<h1> '+ form.username.data + ' '+ form.email.data + ' '+ form.password.data + ' </h1>'
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("loginpage")) 


    return render_template("signup.html", form=form)




@app.route("/mypage")
@login_required
def mypage():

    return render_template("mypage.html", posts=posts)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))



if __name__ == "__main__":
    app.run(debug=True)