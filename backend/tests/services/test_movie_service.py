from unittest.mock import Mock, patch

import pytest
from fastapi import HTTPException

from app.services.movie_service import get_movie_data

VALID_RESPONSE = {
    "Response": "True",
    "Title": "The Godfather",
    "Year": "1972",
    "Plot": "Mafia story",
    "Genre": "Crime, Drama",
    "Director": "Francis Ford Coppola",
    "Actors": "Al Pacino, Marlon Brando",
    "Production": "Paramount Pictures",
}


NOT_FOUND_RESPONSE = {
    "Response": "False",
    "Error": "Movie not found!",
}


@patch("app.services.movie_service.requests.get")
def test_get_movie_data_success(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = VALID_RESPONSE
    mock_response.raise_for_status.return_value = None

    mock_get.return_value = mock_response

    result = get_movie_data("The Godfather")

    assert result.title == "The Godfather"
    assert result.year == 1972
    assert "Crime" in result.genres
    assert "Al Pacino" in result.actors


@patch("app.services.movie_service.requests.get")
def test_get_movie_data_not_found(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = NOT_FOUND_RESPONSE
    mock_response.raise_for_status.return_value = None

    mock_get.return_value = mock_response

    with pytest.raises(HTTPException) as exc:
        get_movie_data("Unknown Movie")

    assert exc.value.status_code == 404
    assert "Movie not found" in exc.value.detail


@patch("app.services.movie_service.requests.get")
def test_get_movie_data_http_error(mock_get):
    from requests.exceptions import HTTPError

    mock_get.side_effect = HTTPError()

    with pytest.raises(HTTPException) as exc:
        get_movie_data("Test")

    assert exc.value.status_code == 502


@patch("app.services.movie_service.requests.get")
def test_get_movie_data_timeout(mock_get):
    from requests.exceptions import Timeout

    mock_get.side_effect = Timeout()

    with pytest.raises(HTTPException) as exc:
        get_movie_data("Test")

    assert exc.value.status_code == 504


@patch("app.services.movie_service.requests.get")
def test_get_movie_data_invalid_data(mock_get):
    bad_response = VALID_RESPONSE.copy()
    bad_response["Title"] = "N/A"

    mock_response = Mock()
    mock_response.json.return_value = bad_response
    mock_response.raise_for_status.return_value = None

    mock_get.return_value = mock_response

    with pytest.raises(HTTPException) as exc:
        get_movie_data("Bad Movie")

    assert exc.value.status_code == 422
