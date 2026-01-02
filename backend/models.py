from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# 1️⃣ USER TABLE
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<User {self.email}>"


# 2️⃣ MOVIE TABLE
class Movie(db.Model):
    __tablename__ = "movies"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    genre = db.Column(db.String(200))
    year = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"<Movie {self.title}>"


# 3️⃣ RATING TABLE (USER ↔ MOVIE)
class Rating(db.Model):
    __tablename__ = "ratings"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    movie_id = db.Column(
        db.Integer,
        db.ForeignKey("movies.id"),
        nullable=False
    )

    score = db.Column(db.Integer, nullable=False)

    user = db.relationship("User", backref="ratings")
    movie = db.relationship("Movie", backref="ratings")

    def __repr__(self):
        return f"<Rating user={self.user_id} movie={self.movie_id} score={self.score}>"
