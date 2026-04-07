from fastapi import APIRouter, Path, Query, HTTPException
from typing import Annotated
from app.schemas.schemas import FilterParamsBasic, Studio, Movie, FilterParams
from app.api.common import filter_items, SessionDep, has_default_filters, filter_movies
from sqlmodel import select
from app.models.studios import Studio
from app.models.movies import Movie as MovieModel

router = APIRouter(prefix="/studios", tags=["studios"])

@router.get("/")
async def get_studios(session: SessionDep, filter_query: Annotated[FilterParamsBasic, Query()]) -> list[Studio]:
  query = select(Studio)
  return filter_items(query, session, filter_query)

@router.get("/{studio_id}")
async def get_studio(session: SessionDep, studio_id: Annotated[int, Path(ge=0)]) -> Studio: 
  studio = session.get(Studio, studio_id)
  if not studio:
      raise HTTPException(status_code=404, detail=f"No Studio found with id={studio_id}.")
  return studio

@router.get("/{studio_id}/movies")
async def get_studio_movies(
    session: SessionDep, 
    studio_id: Annotated[int, Path(ge=0)], 
    filter_query: Annotated[FilterParams, Query()]
  ) -> list[Movie]:
  studio = session.get(Studio, studio_id)
  if not studio:
    raise HTTPException(status_code=404, detail=f"No Studio found with id={studio_id}")

  if has_default_filters(filter_query):
    return studio.movies
  query = select(MovieModel).where(MovieModel.studio_id == studio_id)
  return filter_movies(query, session, filter_query)