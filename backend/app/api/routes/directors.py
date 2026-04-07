from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, Query
from sqlmodel import select

from app.api.common import SessionDep, filter_items, filter_movies, has_default_filters
from app.models.directors import Director
from app.models.movies import Movie as MovieModel
from app.schemas.schemas import FilterParams, FilterParamsBasic, Item, Movie

router = APIRouter(prefix="/directors", tags=["directors"])


@router.get("/")
async def get_directors(
    session: SessionDep, filter_query: Annotated[FilterParamsBasic, Query()]
) -> list[Item]:
    query = select(Director)
    return filter_items(query, session, filter_query)


@router.get("/{director_id}")
async def get_director(
    session: SessionDep, director_id: Annotated[int, Path(ge=0)]
) -> Item:
    director = session.get(Director, director_id)
    if not director:
        raise HTTPException(
            status_code=404, detail=f"No Director found with id={director_id}."
        )
    return director


@router.get("/{director_id}/movies")
async def get_director_movies(
    session: SessionDep,
    director_id: Annotated[int, Path(ge=0)],
    filter_query: Annotated[FilterParams, Query()],
) -> list[Movie]:
    director = session.get(Director, director_id)
    if not director:
        raise HTTPException(
            status_code=404, detail=f"No Director found with id={director_id}"
        )

    if has_default_filters(filter_query):
        return director.movies

    query = (
        select(MovieModel).join(MovieModel.directors).where(Director.id == director_id)
    )
    return filter_movies(query, session, filter_query)
