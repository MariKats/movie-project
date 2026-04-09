from unittest.mock import patch

from backend.app.seed_data import movies

from app.schemas.schemas import MovieCreate


def test_get_movies(test_client):
    response = test_client.get("/movies")
    assert response.status_code == 200
    assert response.json() == movies


def test_get_movie_not_found(test_client):
    response = test_client.get("/movies/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "No Movie found with id=999."


def test_get_movies_offset_limit(test_client):
    response = test_client.get("/movies?offset=5&limit=2")
    assert response.status_code == 200
    result = response.json()
    assert result == movies[5:7]
    assert len(result) == 2
    assert result[0].get("id") == 5
    assert result[1].get("id") == 6


def test_get_movies_offset_limit_sort_desc(test_client):
    response = test_client.get("/movies?offset=5&limit=2&sort=desc")
    assert response.status_code == 200
    result = response.json()
    assert len(result) == 2
    assert result[0].get("id") == 6
    assert result[1].get("id") == 5


def test_get_movies_limit(test_client):
    response = test_client.get("/movies?limit=2")
    assert response.status_code == 200
    result = response.json()
    assert result == movies[:2]
    assert len(result) == 2
    assert result[0].get("id") == 0
    assert result[1].get("id") == 1


def test_get_movies_offset(test_client):
    response = test_client.get("/movies?offset=50")
    assert response.status_code == 200
    result = response.json()
    assert result == movies[50:]
    assert len(result) == 2
    assert result[0].get("id") == 50
    assert result[1].get("id") == 51
    assert result[0].get("year") == 2021
    assert result[1].get("year") == 2020


def test_get_movies_offset_order_by_year(test_client):
    response = test_client.get("/movies?offset=50&order_by=year")
    assert response.status_code == 200
    result = response.json()
    assert len(result) == 2
    assert result[0].get("id") == 51
    assert result[1].get("id") == 50
    assert result[0].get("year") == 2020
    assert result[1].get("year") == 2021


def test_get_movie(test_client):
    response = test_client.get("/movies/1")
    assert response.status_code == 200
    assert response.json() == movies[1]


@patch("app.api.routes.movies.OMDBMovieService.get_movie_data")
def test_create_movie(mock_movie_data, test_client):
    title = "Anaconda"
    year = 2025
    poster = "https://example.com/anaconda.jpg"
    mock_movie_data.return_value = MovieCreate(
        **{
            "title": title,
            "year": year,
            "summary": "A group of old friends reunite to reboot the cult classic",
            "poster": poster,
            "genres": ["Comedy", "Adventure"],  # already in DB
            "directors": ["Tom Gormican"],
            "actors": ["Jack Black", "Paul Rudd"],
            "studio": {"name": "Columbia Pictures", "headquarters": "Culver City, USA"},
        }
    )

    assert len(test_client.get("/movies").json()) == 52
    assert len(test_client.get("/actors").json()) == 87
    assert len(test_client.get("/genres").json()) == 19
    assert len(test_client.get("/studios").json()) == 20
    assert len(test_client.get("/directors").json()) == 36

    response = test_client.post("/movies", params={"title": title, "year": year})
    assert response.status_code == 200
    response_all_movies = test_client.get("/movies")
    response_all_actors = test_client.get("/actors")
    response_all_genres = test_client.get("/genres")
    response_all_studios = test_client.get("/studios")
    response_all_directors = test_client.get("/directors")
    assert len(response_all_movies.json()) == 53
    assert len(response_all_actors.json()) == 89
    assert len(response_all_genres.json()) == 19
    assert len(response_all_directors.json()) == 37
    assert len(response_all_studios.json()) == 21
    assert response_all_movies.json()[-1].get("title") == "Anaconda"
    assert response_all_movies.json()[-1].get("poster") == poster
    assert [actor.get("name") for actor in response_all_actors.json()[-2:]] == [
        "Jack Black",
        "Paul Rudd",
    ]
    assert response_all_directors.json()[-1].get("name") == "Tom Gormican"
    assert response_all_studios.json()[-1].get("name") == "Columbia Pictures"


def test_create_movie_already_exists(test_client):
    title = "The Godfather"
    year = 1972
    response = test_client.post("/movies", params={"title": title, "year": year})
    assert response.status_code == 200
    assert response.json() == movies[1]


@patch("app.api.routes.movies.OMDBMovieService.get_movie_data")
def test_patch_movie_update_studio(mock_get, test_client):
    # add a movie without studio first
    title = "Pocahontas"
    year = 1995
    mock_get.return_value = MovieCreate(
        **{
            "title": title,
            "year": year,
            "summary": "An English soldier and the daughter of an Algonquin chief share a romance when English colonists invade seventeenth century Virginia.",  # noqa: E501
            "genres": ["Animation", "Drama", "Adventure"],
            "directors": ["Mike Gabriel, Eric Goldberg"],
            "actors": ["Mel Gibson", "Christian Bale", "Linda Hunt"],
            "studio": None,
        }
    )
    response = test_client.post("/movies", params={"title": "Pocahontas"})
    assert response.status_code == 200
    movie_id = response.json().get("id")

    response_get = test_client.get(f"/movies/{movie_id}")
    assert response_get.status_code == 200
    assert response_get.json().get("title") == "Pocahontas"
    assert response_get.json().get("studio") is None

    # update the movie with a studio
    studio_payload = {
        "update": {"studio": {"name": "Walt Disney Animation"}}
    }  # in DB already with id 9
    response = test_client.patch(
        f"/movies/{movie_id}",
        json=studio_payload,
    )
    assert response.status_code == 200
    assert response.json().get("studio").get("name") == "Walt Disney Animation"
    assert response.json().get("studio").get("headquarters") == "Burbank, USA"
    response_studio_movies = test_client.get("/studios/9/movies")
    assert response_studio_movies.status_code == 200
    assert movie_id in [movie["id"] for movie in response_studio_movies.json()]


def test_patch_movie_update_studio_not_found(test_client):
    studio_payload = {"update": {"studio": {"name": "Walt Disney Animation"}}}
    response = test_client.patch("/movies/9999", json=studio_payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "No Movie found with id=9999."


@patch("app.api.routes.movies.OMDBMovieService.get_movie_data")
def test_patch_movie_create_new_studio(mock_get, test_client):
    # add a movie without studio first
    title = "Mulan"
    year = 1998
    mock_get.return_value = MovieCreate(
        **{
            "title": title,
            "year": year,
            "summary": "A young Chinese woman disguises herself as a male warrior.",
            "genres": ["Animation", "Adventure"],
            "directors": ["Tony Bancroft"],
            "actors": ["Ming-Na Wen"],
            "studio": None,
        }
    )
    response = test_client.post("/movies", params={"title": title, "year": year})
    assert response.status_code == 200
    movie_id = response.json().get("id")
    assert response.json().get("studio") is None

    # update with a brand new studio not in DB
    studios_before = len(test_client.get("/studios").json())
    studio_payload = {
        "update": {
            "studio": {"name": "Brand New Studio", "headquarters": "New York, USA"}
        }
    }
    response = test_client.patch(f"/movies/{movie_id}", json=studio_payload)
    assert response.status_code == 200
    assert response.json().get("studio").get("name") == "Brand New Studio"
    studios_after = len(test_client.get("/studios").json())
    assert studios_after == studios_before + 1


@patch("app.api.routes.movies.OMDBMovieService.get_movie_data")
def test_patch_movie_replace_existing_studio(mock_get, test_client):
    # add a movie with a studio
    title = "Atlantis"
    year = 2001
    mock_get.return_value = MovieCreate(
        **{
            "title": title,
            "year": year,
            "summary": "A young adventurer named Milo Thatch joins an expedition.",
            "genres": ["Animation", "Adventure"],
            "directors": ["Gary Trousdale"],
            "actors": ["Michael J. Fox"],
            "studio": {"name": "Dreamworks Pictures"},
        }
    )
    response = test_client.post("/movies", params={"title": title, "year": year})
    assert response.status_code == 200
    movie_id = response.json().get("id")
    assert response.json().get("studio").get("name") == "Dreamworks Pictures"
    assert response.json().get("studio").get("headquarters") == "Glendale, USA"

    # replace with a different existing studio
    studio_payload = {
        "update": {"studio": {"name": "Walt Disney Animation"}}
    }  # in DB already with id 9
    response = test_client.patch(f"/movies/{movie_id}", json=studio_payload)
    assert response.status_code == 200
    assert response.json().get("studio").get("name") == "Walt Disney Animation"
    assert response.json().get("studio").get("headquarters") == "Burbank, USA"
