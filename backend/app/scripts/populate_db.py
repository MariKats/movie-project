"""
Seed the database from app.fake_data.
Run from the project root with:
    python app/scripts/populate_db.py
"""

from sqlmodel import Session, SQLModel
from app.fake_data import (
    actors as actors_data,
    directors as directors_data,
    genres as genres_data,
    movies as movies_data,
    studios as studios_data,
)

from app.models.movies import Movie, Actor, Studio, Genre, Director
from app.core.database import SessionLocal, create_db_and_tables


def seed_reference_data(session: Session) -> None:
    for genre in genres_data:
        session.merge(Genre(**genre))

    for director in directors_data:
        session.merge(Director(**director))

    for actor in actors_data:
        session.merge(Actor(**actor))

    for studio in studios_data:
        session.merge(Studio(**studio))

    session.commit()


def seed_movies(session: Session) -> None:
    for movie_data in movies_data:
        existing_movie = session.get(Movie, movie_data["id"])
        if existing_movie:
            continue

        movie = Movie(
            id=movie_data["id"],
            title=movie_data["title"],
            summary=movie_data["summary"],
            year=movie_data["year"],
            studio_id=movie_data["studio"]["id"],
        )
        
        session.add(movie)

        movie.genres = [session.get(Genre, genre["id"]) for genre in movie_data["genres"]]
        movie.directors = [
            session.get(Director, director["id"]) for director in movie_data["directors"]
        ]
        movie.actors = [session.get(Actor, actor["id"]) for actor in movie_data["actors"]]


    session.commit()


def main() -> None:
    create_db_and_tables()
    with SessionLocal() as session:
        seed_reference_data(session)
        seed_movies(session)

    print("Database seeded successfully.")


if __name__ == "__main__":
    main()
