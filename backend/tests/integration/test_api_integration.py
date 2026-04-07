def test_get_movies_integration(test_client):
    response = test_client.get("/movies")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 52
    assert data[0]["id"] == 0
    assert data[0]["title"] == "The Shawshank Redemption"


def test_get_genre_movies_integration(test_client):
    response = test_client.get("/genres/0/movies")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert {movie["title"] for movie in data} == {"The Lion King", "Inside Out 2"}


def test_get_actor_movies_integration(test_client):
    response = test_client.get("/actors/4/movies")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["title"] == "The Godfather"
    assert data[1]["title"] == "The Godfather Part II"


def test_get_studio_movies_integration(test_client):
    response = test_client.get("/studios/6/movies")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["title"] == "The Avengers"
    assert data[1]["title"] == "Deadpool & Wolverine"
