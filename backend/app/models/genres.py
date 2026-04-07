from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.movies import Movie


class MovieGenre(SQLModel, table=True):
    movie_id: int | None = Field(default=None, primary_key=True, foreign_key="movie.id")
    genre_id: int | None = Field(default=None, primary_key=True, foreign_key="genre.id")


class Genre(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    movies: list["Movie"] = Relationship(back_populates="genres", link_model=MovieGenre)  # type: ignore
