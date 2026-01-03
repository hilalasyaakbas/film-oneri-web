import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import db, User, Movie, Rating

app = Flask(__name__)

# =======================
# APP + SESSION CONFIG
# =======================
app.secret_key = "dev-secret-key"

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# =======================
# ROUTES
# =======================

@app.route("/")
def home():
    return render_template("index.html")

# ---------- SIGN UP ----------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # Formdan verileri al
        fullname = request.form.get("fullname")
        email = request.form.get("email")
        password = request.form.get("password")

        # Email zaten var mı kontrolü
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return render_template("signup.html", message="This email is already registered.")

        user = User(fullname=fullname, email=email, password=password)
        db.session.add(user)
        db.session.commit()

        session["user_id"] = user.id
        return redirect(url_for("rate_movie"))

    return render_template("signup.html")

# ---------- SIGN IN ----------
@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and user.password == password:
            session["user_id"] = user.id
            return redirect(url_for("rate_movie"))

        # Hata durumunda mesajı sayfaya gönderiyoruz
        return render_template("signin.html", message="Invalid email or password")

    return render_template("signin.html")

# ---------- RATE MOVIE ----------
@app.route("/rate", methods=["GET", "POST"])
def rate_movie():
    user_id = session.get("user_id")

    if not user_id:
        return redirect(url_for("signin"))

    rating_count = Rating.query.filter_by(user_id=user_id).count()

    # Eğer 10 film oylandıysa direkt öneri sayfasına
    if rating_count >= 10:
        return redirect(url_for("recommend"))

    movies = Movie.query.order_by(Movie.id).limit(20).all()
    message = None

    if request.method == "POST":
        movie_id = request.form.get("movie_id")
        score = request.form.get("score")

        existing_rating = Rating.query.filter_by(user_id=user_id, movie_id=movie_id).first()

        if existing_rating:
            message = "You already rated this movie"
        else:
            rating = Rating(user_id=user_id, movie_id=movie_id, score=score)
            db.session.add(rating)
            db.session.commit()
            rating_count += 1
            message = f"Rating saved ({rating_count}/10)"

            if rating_count >= 10:
                return redirect(url_for("recommend"))

    return render_template("rate.html", movies=movies, message=message, rating_count=rating_count)

@app.route("/recommend")
def recommend():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("signin"))
    return render_template("recommend.html")

# Veritabanı tablolarını oluştur
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)