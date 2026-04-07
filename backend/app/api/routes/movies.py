from fastapi import APIRouter, Path, Query, HTTPException
from sqlmodel import select
from typing import Annotated
from app.schemas.schemas import FilterParams, Movie, MovieCreate
from app.api.common import filter_movies, SessionDep, find_or_create_item, find_or_create_items, CreateField
from app.models.movies import Movie as MovieModel


router = APIRouter(prefix="/movies", tags=["movies"])

@router.get("/")
async def get_movies(session: SessionDep, filter_query: Annotated[FilterParams, Query()]) -> list[Movie]:
  query = select(MovieModel)
  return filter_movies(query, session, filter_query)

@router.get("/{movie_id}")
async def get_movie(session: SessionDep, movie_id: Annotated[int, Path(ge=0)]) -> Movie: 
  movie = session.get(MovieModel, movie_id)
  if not movie:
      raise HTTPException(status_code=404, detail=f"No Movie found with id={movie_id}.")
  return movie

@router.post("/")
async def create_movie(session: SessionDep, movie: MovieCreate) -> Movie:
  query = select(MovieModel).where(MovieModel.title == movie.title.strip().title()).where(MovieModel.year == movie.year)
  existing = session.exec(query).first()
  if existing:
    return existing
  
  actors = find_or_create_items(session, CreateField.actor, movie.actors)
  genres = find_or_create_items(session, CreateField.genre, movie.genres)
  directors = find_or_create_items(session, CreateField.director, movie.directors)
  studio = find_or_create_item(session, CreateField.studio, movie.studio)

  new_movie = MovieModel(
    title=movie.title,
    year=movie.year,
    summary=movie.summary, 
    actors=actors, 
    genres=genres, 
    directors=directors,
    studio=studio
  )
  
  session.add(new_movie)
  session.commit()
  return new_movie