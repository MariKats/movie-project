from app.fake_data import actors


def test_get_actors(test_client):
    response = test_client.get("/actors")
    assert response.status_code == 200
    assert response.json() == actors


def test_get_actors_offset_limit(test_client):
    response = test_client.get("/actors?offset=5&limit=2")
    assert response.status_code == 200
    result = response.json()
    assert result == actors[5:7]
    assert len(result) == 2
    assert result[0].get("id") == 5
    assert result[1].get("id") == 6


def test_get_actors_offset_limit_sort_desc(test_client):
    response = test_client.get("/actors?offset=5&limit=2&sort=desc")
    assert response.status_code == 200
    result = response.json()
    assert len(result) == 2
    assert result[0].get("id") == 6
    assert result[1].get("id") == 5


def test_get_actors_limit(test_client):
    response = test_client.get("/actors?limit=2")
    assert response.status_code == 200
    result = response.json()
    assert result == actors[:2]
    assert len(result) == 2
    assert result[0].get("id") == 0
    assert result[1].get("id") == 1


def test_get_actors_offset(test_client):
    response = test_client.get("/actors?offset=84")
    assert response.status_code == 200
    result = response.json()
    assert result == actors[84:]
    assert len(result) == 3
    assert result[0].get("id") == 84
    assert result[1].get("id") == 85
    assert result[2].get("id") == 86


def test_get_actor(test_client):
    response = test_client.get("/actors/4")
    assert response.status_code == 200
    result = response.json()
    assert result == actors[4]
    assert result.get("name") == "Al Pacino"


def test_get_actor_movies(test_client):
    response = test_client.get("/actors/4/movies")
    assert response.status_code == 200
    result = response.json()
    assert len(result) == 2
    assert result[0].get("title") == "The Godfather"
    assert result[0].get("year") == 1972
    assert result[1].get("title") == "The Godfather Part II"
    assert result[1].get("year") == 1974


def test_get_actor_movies_sort_desc(test_client):
    response = test_client.get("/actors/4/movies?sort=desc")
    assert response.status_code == 200
    result = response.json()
    assert len(result) == 2
    assert result[0].get("title") == "The Godfather Part II"
    assert result[1].get("title") == "The Godfather"


def test_get_actor_movies_order_by_year_sort_desc(test_client):
    response = test_client.get("/actors/4/movies?order_by=year&sort=desc")
    assert response.status_code == 200
    result = response.json()
    assert len(result) == 2
    assert result[0].get("title") == "The Godfather Part II"
    assert result[1].get("title") == "The Godfather"


def test_get_actor_not_found(test_client):
    response = test_client.get("/actors/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "No Actor found with id=999."


def test_get_actor_movies_not_found(test_client):
    response = test_client.get("/actors/999/movies")
    assert response.status_code == 404
    assert response.json()["detail"] == "No Actor found with id=999."
