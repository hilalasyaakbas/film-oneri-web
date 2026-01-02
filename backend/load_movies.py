import csv
import os
from app import app
from models import db, Movie

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
CSV_PATH = os.path.join(BASE_DIR, "movies.csv")

with app.app_context():
    with open(CSV_PATH, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            movie = Movie(
                title=row["title"],
                genre=row["genres"],
                year=None
            )
            db.session.add(movie)

        db.session.commit()

    print("MOVIES LOADED INTO DATABASE")
