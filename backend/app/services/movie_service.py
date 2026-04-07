from typing import Any, Dict

import requests
from fastapi import HTTPException
from requests.exceptions import ConnectionError, HTTPError, RequestException, Timeout

from app.core.config import settings
from app.schemas.schemas import MovieCreate
from app.services.constants import RequiredMovieFields

BASE_URL = f"https://www.omdbapi.com/?apikey={settings.OMDB_API_KEY}"
DEFAULT_TIMEOUT = 60


def _transform_movie_object(movie_data: Dict[str, Any]) -> MovieCreate:
    for field in RequiredMovieFields._member_names_:
        value = movie_data.get(field)
        if not value or value == "N/A":
            raise HTTPException(
                status_code=422, detail=f"Missing required field: {field}"
            )

        if not isinstance(value, str):
            raise HTTPException(
                status_code=422, detail=f"Invalid type for field: {field}"
            )

    new_movie = {
        "title": movie_data.get("Title"),
        "summary": movie_data.get("Plot"),
        "year": int(movie_data.get("Year")),
        "genres": [g.strip().title() for g in movie_data.get("Genre").split(",") if g],
        "directors": [
            d.strip().title() for d in movie_data.get("Director").split(",") if d
        ],
        "actors": [a.strip().title() for a in movie_data.get("Actors").split(",") if a],
        "studio": (
            {"name": movie_data.get("Production"), "headquarters": "N/A"}
            if movie_data.get("Production") not in [None, "N/A"]
            else None
        ),
    }

    return MovieCreate(**new_movie)


def get_movie_data(
    title: str, year: int | None = None, timeout: int = DEFAULT_TIMEOUT
) -> MovieCreate:

    endpoint = f"{BASE_URL}&t={title}"
    if year is not None:
        endpoint += f"&y={year}"

    try:
        response = requests.get(endpoint, timeout=timeout)
        response.raise_for_status()

        result = response.json()

        if result.get("Response") == "False":
            raise HTTPException(
                status_code=404, detail=result.get("Error", "Movie not found")
            )

        return _transform_movie_object(result)

    except HTTPException:
        raise

    except HTTPError as e:
        raise HTTPException(status_code=502, detail=f"OMDb HTTP error: {str(e)}")

    except ConnectionError:
        raise HTTPException(status_code=503, detail="Failed to connect to OMDb API")

    except Timeout:
        raise HTTPException(
            status_code=504, detail=f"Request timed out after {timeout}s"
        )

    except RequestException as e:
        raise HTTPException(status_code=500, detail=f"Request error: {str(e)}")
