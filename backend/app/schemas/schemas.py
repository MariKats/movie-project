from typing import Literal

from pydantic import BaseModel, Field, HttpUrl


class NameBase(BaseModel):
    name: str


class Item(NameBase):
    id: int


class StudioBase(NameBase):
    headquarters: str | None = None


class Studio(StudioBase):
    id: int


class MovieBase(BaseModel):
    title: str
    summary: str
    year: int
    poster: HttpUrl | None = None


class MovieCreate(MovieBase):
    genres: list[str]
    directors: list[str]
    actors: list[str]
    studio: StudioBase | None = None


class Movie(MovieBase):
    id: int
    genres: list[Item]
    directors: list[Item]
    actors: list[Item]
    studio: Studio | None


class FilterParamsBasic(BaseModel):
    model_config = {"extra": "forbid"}
    offset: int = Field(0, ge=0)
    limit: int | None = Field(None, ge=0)
    sort: Literal["asc", "desc"] = "asc"


class FilterParams(FilterParamsBasic):
    order_by: Literal["year", "title"] | None = None
