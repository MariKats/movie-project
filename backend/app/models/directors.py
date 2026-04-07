from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.movies import Movie

class MovieDirector(SQLModel, table=True):
  movie_id: int | None = Field(default=None, primary_key=True, foreign_key="movie.id")
  director_id: int | None = Field(default=None, primary_key=True, foreign_key="director.id")

class Director(SQLModel, table=True):
  id: int | None = Field(default=None, primary_key=True)
  name: str = Field(index=True)
  movies: list["Movie"] = Relationship(back_populates="directors", link_model=MovieDirector)
