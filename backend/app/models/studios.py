from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.movies import Movie
    
class Studio(SQLModel, table=True):
  id: int | None = Field(default=None, primary_key=True)
  name: str = Field(index=True)
  headquarters: str | None = Field(default=None)
  movies: list["Movie"] = Relationship(back_populates="studio")
