from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, Query
from sqlmodel import select

from app.api.common import SessionDep, filter_items, filter_movies, has_default_filters
from app.models.actors import Actor
from app.models.movies import Movie as MovieModel
from app.schemas.schemas import FilterParams, FilterParamsBasic, Item, Movie

router = APIRouter(prefix="/actors", tags=["actors"])


@router.get("/")
async def get_actors(
    session: SessionDep, filter_query: Annotated[FilterParamsBasic, Query()]
) -> list[Item]:
    query = select(Actor)
    return filter_items(query, session, filter_query)


@router.get("/{actor_id}")
async def get_actor(session: SessionDep, actor_id: Annotated[int, Path(ge=0)]) -> Item:
    actor = session.get(Actor, actor_id)
    if not actor:
        raise HTTPException(
            status_code=404, detail=f"No Actor found with id={actor_id}."
        )
    return actor


@router.get("/{actor_id}/movies")
async def get_actor_movies(
    session: SessionDep,
    actor_id: Annotated[int, Path(ge=0)],
    filter_query: Annotated[FilterParams, Query()],
) -> list[Movie]:
    actor = session.get(Actor, actor_id)
    if not actor:
        raise HTTPException(
            status_code=404, detail=f"No Actor found with id={actor_id}"
        )

    if has_default_filters(filter_query):
        return actor.movies

    query = select(MovieModel).join(MovieModel.actors).where(Actor.id == actor_id)
    return filter_movies(query, session, filter_query)
