from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, Path, Query
from sqlmodel import select

from app.api.common import (
    CreateField,
    SessionDep,
    filter_movies,
    find_or_create_item,
    find_or_create_items,
)
from app.models.movies import Movie as MovieModel
from app.schemas.schemas import FilterParams, Movie, MovieCreate, StudioBase
from app.services.movie_service import get_movie_data

router = APIRouter(prefix="/movies", tags=["movies"])


@router.get("/")
async def get_movies(
    session: SessionDep, filter_query: Annotated[FilterParams, Query()]
) -> list[Movie]:
    query = select(MovieModel)
    return filter_movies(query, session, filter_query)


@router.get("/{movie_id}")
async def get_movie(session: SessionDep, movie_id: Annotated[int, Path(ge=0)]) -> Movie:
    movie = session.get(MovieModel, movie_id)
    if not movie:
        raise HTTPException(
            status_code=404, detail=f"No Movie found with id={movie_id}."
        )
    return movie


@router.post("/")
async def create_movie(
    session: SessionDep, title: str, year: int | None = None
) -> Movie:
    query = select(MovieModel).where(MovieModel.title == title.strip().title())
    if year is not None:
        query.where(MovieModel.year == year)

    existing = session.exec(query).first()
    if existing:
        return existing

    try:
        movie: MovieCreate = get_movie_data(title, year)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="External service error")

    new_movie = MovieModel(
        title=movie.title,
        year=movie.year,
        summary=movie.summary,
        actors=find_or_create_items(session, CreateField.actor, movie.actors),
        genres=find_or_create_items(session, CreateField.genre, movie.genres),
        directors=find_or_create_items(session, CreateField.director, movie.directors),
        studio=(
            find_or_create_item(session, CreateField.studio, movie.studio)
            if movie.studio
            else None
        ),
    )

    session.add(new_movie)
    session.commit()
    session.refresh(new_movie)
    return new_movie


@router.patch("/{movie_id}/update-studio")
async def update_movie_studio(
    session: SessionDep,
    movie_id: Annotated[int, Path(ge=0)],
    studio: Annotated[StudioBase, Body(embed=True)],
) -> Movie:
    movie = session.get(MovieModel, movie_id)
    if not movie:
        raise HTTPException(
            status_code=404, detail=f"No Movie found with id={movie_id}."
        )

    print(f"Updating movie {movie_id} with studio {studio.name}")
    studio = find_or_create_item(session, CreateField.studio, studio)
    print(f"Found or created studio: {studio}")
    movie.studio = studio

    session.add(movie)
    session.commit()
    session.refresh(movie)
    return movie
