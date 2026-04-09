from typing import Any, Dict

import requests
from fastapi import HTTPException
from requests.exceptions import ConnectionError, HTTPError, RequestException, Timeout

import app.services.constants as constants
from app.schemas.schemas import MovieCreate


class MovieService:
    def __init__(
        self,
        base_url: str,
        search_params: Dict[str, str],
        headers: Dict[str, Any] = None,
        timeout: int = constants.DEFAULT_TIMEOUT,
    ):
        self.base_url = base_url
        self.headers = headers
        self.timeout = timeout
        self.search_params = search_params or {}

    def _transform_movie_object(self, movie_data: Dict[str, Any]) -> MovieCreate:
        print(f"Transforming movie data: {movie_data}")
        pass

    def _create_endpoint(self) -> str:
        params = {k: v for k, v in self.search_params.items() if v is not None}
        return f"{self.base_url}&{'&'.join(f'{k}={v}' for k, v in params.items())}"

    def get_movie_data(self) -> MovieCreate:
        endpoint = self._create_endpoint()
        try:
            response = (
                requests.get(endpoint, timeout=self.timeout)
                if not self.headers
                else requests.get(endpoint, headers=self.headers, timeout=self.timeout)
            )
            response.raise_for_status()

            result = response.json()

            if result.get("Response") == "False":
                raise HTTPException(
                    status_code=404, detail=result.get("Error", "Movie not found")
                )

            return self._transform_movie_object(result)

        except HTTPException:
            raise

        except HTTPError as e:
            raise HTTPException(status_code=502, detail=f"OMDb HTTP error: {str(e)}")

        except ConnectionError:
            raise HTTPException(status_code=503, detail="Failed to connect to OMDb API")

        except Timeout:
            raise HTTPException(
                status_code=504,
                detail=f"Request timed out after {self.timeout} seconds",
            )

        except RequestException as e:
            raise HTTPException(status_code=500, detail=f"Request error: {str(e)}")


class OMDBMovieService(MovieService):
    def __init__(
        self,
        title: str,
        year: int | None = None,
        timeout: int = constants.DEFAULT_TIMEOUT,
    ):
        search_params = {"t": title}
        if year is not None:
            search_params["y"] = str(year)

        super().__init__(
            base_url=constants.OMDB_BASE_URL,
            search_params=search_params,
            timeout=timeout,
        )

    def _transform_movie_object(self, movie_data: Dict[str, Any]) -> MovieCreate:
        for field in constants.RequiredMovieFields._member_names_:
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
            "genres": [
                g.strip().title() for g in movie_data.get("Genre").split(",") if g
            ],
            "directors": [
                d.strip().title() for d in movie_data.get("Director").split(",") if d
            ],
            "actors": [
                a.strip().title() for a in movie_data.get("Actors").split(",") if a
            ],
        }
        if movie_data.get("Production") not in [None, "N/A"]:
            new_movie.update({"studio": {"name": movie_data.get("Production")}})
        if movie_data.get("Poster") not in [None, "N/A"]:
            new_movie.update({"poster": movie_data.get("Poster")})

        return MovieCreate(**new_movie)
