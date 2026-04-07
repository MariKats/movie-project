from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.movies import Movie


class MovieActor(SQLModel, table=True):
    movie_id: int | None = Field(default=None, primary_key=True, foreign_key="movie.id")
    actor_id: int | None = Field(default=None, primary_key=True, foreign_key="actor.id")


class Actor(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    movies: list["Movie"] = Relationship(back_populates="actors", link_model=MovieActor)
