from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, Query
from sqlmodel import select

from app.api.common import (
    FilterParams,
    SessionDep,
    filter_items,
    filter_movies,
    has_default_filters,
)
from app.models.genres import Genre
from app.models.movies import Movie as MovieModel
from app.schemas.schemas import FilterParamsBasic, Item, Movie

router = APIRouter(prefix="/genres", tags=["genres"])


@router.get("/")
async def get_genres(
    session: SessionDep, filter_query: Annotated[FilterParamsBasic, Query()]
) -> list[Item]:
    query = select(Genre)
    return filter_items(query, session, filter_query)


@router.get("/{genre_id}")
async def get_genre(session: SessionDep, genre_id: Annotated[int, Path(ge=0)]) -> Item:
    genre = session.get(Genre, genre_id)
    if not genre:
        raise HTTPException(
            status_code=404, detail=f"No Genre found with id={genre_id}."
        )
    return genre


@router.get("/{genre_id}/movies")
async def get_genre_movies(
    session: SessionDep,
    genre_id: Annotated[int, Path(ge=0)],
    filter_query: Annotated[FilterParams, Query()],
) -> list[Movie]:
    genre = session.get(Genre, genre_id)
    if not genre:
        raise HTTPException(
            status_code=404, detail=f"No Genre found with id={genre_id}"
        )

    if has_default_filters(filter_query):
        return genre.movies

    query = select(MovieModel).join(MovieModel.genres).where(Genre.id == genre_id)
    return filter_movies(query, session, filter_query)
