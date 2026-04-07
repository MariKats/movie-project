from pydantic import BaseModel, Field
from typing import Literal

class NameBase(BaseModel):
  name: str

class Item(NameBase):
  id: int

class StudioBase(NameBase):
  headquarters: str

class Studio(StudioBase):
  id: int

class MovieBase(BaseModel):
  title: str
  summary: str
  year: int

class MovieCreate(MovieBase):
  genres: list[str]
  directors: list[str]
  actors: list[str]
  studio: StudioBase

class Movie(MovieBase):
  id: int
  genres: list[Item]
  directors: list[Item]
  actors: list[Item]
  studio: Studio

class FilterParamsBasic(BaseModel):
  model_config = {"extra": "forbid"}
  offset: int = Field(0, ge=0) 
  limit: int| None = Field(None, ge=0, le=10)
  sort: Literal["asc", "desc"] = "asc"

class FilterParams(FilterParamsBasic):
  order_by: Literal["year", "title"] | None = None
