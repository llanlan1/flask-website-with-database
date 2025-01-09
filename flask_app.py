from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, login_required, login_user, LoginManager, logout_user, UserMixin
import uuid
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['STRICT_SLASHES'] = False

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="gensgcsd03team01",
    password="passwordteam01",
    hostname="gensgcsd03team01.mysql.pythonanywhere-services.com",
    databasename="gensgcsd03team01$portfolios",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.secret_key = "gensgcsd03team01apikey"
login_manager = LoginManager()
login_manager.init_app(app)


db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))

    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username


default_users = [User("admin", generate_password_hash("secret")), User("tester", generate_password_hash("super-secret"))]


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(username=user_id).first()


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    content = db.Column(db.String(4096))
    posted = db.Column(db.DateTime, default=datetime.now)
    commenter_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True)
    commenter = db.relationship('User', foreign_keys=commenter_id)

comments = []

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == 'GET':
        return render_template("main_page.html", comments=comments)
    comments.append(request.form["contents"])
    return redirect(url_for('index'))

@app.route('/home', methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("home_page.html", comments=Comment.query.all())

    if not current_user.is_authenticated:
        return redirect(url_for('index'))

    comment = Comment(content=request.form["contents"], commenter=current_user)
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/wangshuo')
def gotowangshuo():
    return render_template("wangshuo.html")

@app.route('/lan')
def gotolan():
    return render_template("lan.html")

@app.route('/zuhairah')
def gotozuhairah():
    return render_template("zuhairah.html")

@app.route('/add_users')
def add_users():
    db.session.add_all(default_users)
    db.session.commit()
    return 'Success'

@app.route("/login", methods=["GET", "POST"])
@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login_page.html", error=False)
    user = load_user(request.form["username"])
    if user is None:
        return render_template("login_page.html", error=True)

    if not user.check_password(request.form["password"]):
        return render_template("login_page.html", error=True)

    login_user(user)
    return redirect(url_for('home'))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)
