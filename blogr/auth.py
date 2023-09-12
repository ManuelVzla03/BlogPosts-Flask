from flask import (
    Blueprint,
    render_template,
    request,
    url_for,
    redirect,
    flash,
    session,
    g,
)
import functools
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from blogr import db
from werkzeug.utils import secure_filename

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        user = User(username, email, generate_password_hash(password))

        error = None
        user_email = User.query.filter_by(email=email).first()

        if user_email is None:
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("auth.login"))
        else:
            error = f"El correo {email} ya está registrado"
        flash(error)
    return render_template("auth/register.html")


@bp.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        error = None
        user = User.query.filter_by(email=email).first()

        if user is None or not check_password_hash(user.password, password):
            error = "Email o contraseña incorrecta"

        if error is None:
            session.clear()
            session["user.id"] = user.id
            return redirect(url_for("post.posts"))

        flash(error)
    return render_template("auth/login.html")


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user.id")

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get_or_404(user_id)


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home.index"))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)

    return wrapped_view


@bp.route("/profile/<int:id>", methods=["POST", "GET"])
@login_required
def profile(id):
    user = User.query.get_or_404(id)

    if request.method == 'POST':
        user.username = request.form.get('username')
        password = request.form.get('password')

        error = None

        if len(password) != 0: 
            user.password = generate_password_hash(password)
        elif len(password) > 0 and len(password) < 6:
            error = 'La contraseña debe de tener más de 5 carácteres'

        if request.files['photo']:
            photo = request.files['photo']
            photo.save(f'blogr/static/media/{secure_filename(photo.filename)}')
            user.photo = f'media/{secure_filename(photo.filename)}'

        if error is not None:
            flash(error)
        else:
            db.session.commit()
            return redirect(url_for('auth.profile', id = user.id))
        flash(error)
    return render_template('auth/profile.html', user = user)
