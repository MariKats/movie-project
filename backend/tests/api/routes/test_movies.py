from app.fake_data import movies

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

def test_create_movie(test_client):
  assert len(test_client.get("/movies").json()) == 52
  assert len(test_client.get("/actors").json()) == 87
  assert len(test_client.get("/genres").json()) == 19
  assert len(test_client.get("/studios").json()) == 20
  assert len(test_client.get("/directors").json()) == 36

  movie = {
    "title":"Anaconda",
    "summary":"A group of old friends reunite to reboot the cult classic - Anaconda",
    "year":2025,
    "genres":["Comedy","Adventure"], # already in DB
    "directors":["Tom Gormican"],
    "actors":["Jack Black", "Paul Rudd"],
    "studio":{"name":"Columbia Pictures","headquarters":"Culver City, USA"}
  }

  response = test_client.post("/movies", json=movie)
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
  assert [actor.get("name") for actor in response_all_actors.json()[-2:]] == ["Jack Black", "Paul Rudd"]
  assert response_all_directors.json()[-1].get("name") == "Tom Gormican"
  assert response_all_studios.json()[-1].get("name") == "Columbia Pictures"
