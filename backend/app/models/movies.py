from sqlmodel import SQLModel, Field, Relationship
from app.models.studios import Studio
from app.models.genres import Genre, MovieGenre
from app.models.actors import Actor, MovieActor
from app.models.directors import Director, MovieDirector

class Movie(SQLModel, table=True):
  id: int | None = Field(default=None, primary_key=True)
  title: str = Field(index=True)
  summary: str
  year: int
  genres: list[Genre] = Relationship(back_populates="movies", link_model=MovieGenre)
  actors: list[Actor] = Relationship(back_populates="movies", link_model=MovieActor)
  directors: list[Director] = Relationship(back_populates="movies", link_model=MovieDirector)
  studio_id: int | None = Field(default=None, foreign_key="studio.id")
  studio: Studio | None = Relationship(back_populates="movies")
