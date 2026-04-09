from backend.app.seed_data import genres


def test_get_genres(test_client):
    response = test_client.get("/genres")
    assert response.status_code == 200
    assert response.json() == genres


def test_get_genres_offset_limit(test_client):
    response = test_client.get("/genres?offset=5&limit=2")
    assert response.status_code == 200
    result = response.json()
    assert result == genres[5:7]
    assert len(result) == 2
    assert result[0].get("id") == 5
    assert result[1].get("id") == 6


def test_get_genres_offset_limit_sort_desc(test_client):
    response = test_client.get("/genres?offset=5&limit=2&sort=desc")
    assert response.status_code == 200
    result = response.json()
    assert len(result) == 2
    assert result[0].get("id") == 6
    assert result[1].get("id") == 5


def test_get_genres_limit(test_client):
    response = test_client.get("/genres?limit=2")
    assert response.status_code == 200
    result = response.json()
    assert result == genres[:2]
    assert len(result) == 2
    assert result[0].get("id") == 0
    assert result[1].get("id") == 1


def test_get_genres_offset(test_client):
    response = test_client.get("/genres?offset=16")
    assert response.status_code == 200
    result = response.json()
    assert result == genres[16:]
    assert len(result) == 3
    assert result[0].get("id") == 16
    assert result[1].get("id") == 17
    assert result[2].get("id") == 18


def test_get_genre(test_client):
    response = test_client.get("/genres/1")
    assert response.status_code == 200
    assert response.json() == genres[1]


def test_get_genre_movies(test_client):
    response = test_client.get("/genres/0/movies")
    assert response.status_code == 200
    result = response.json()
    assert len(result) == 2
    assert result[0].get("title") == "The Lion King"
    assert result[1].get("title") == "Inside Out 2"


def test_get_genre_movies_sort_desc(test_client):
    response = test_client.get("/genres/0/movies?sort=desc")
    assert response.status_code == 200
    result = response.json()
    assert len(result) == 2
    assert result[0].get("title") == "Inside Out 2"
    assert result[1].get("title") == "The Lion King"


def test_get_genre_movies_order_by_title(test_client):
    response = test_client.get("/genres/0/movies?order_by=title")
    assert response.status_code == 200
    result = response.json()
    assert len(result) == 2
    assert result[0].get("title") == "Inside Out 2"
    assert result[1].get("title") == "The Lion King"


def test_get_genre_not_found(test_client):
    response = test_client.get("/genres/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "No Genre found with id=999."


def test_get_genre_movies_not_found(test_client):
    response = test_client.get("/genres/999/movies")
    assert response.status_code == 404
    assert response.json()["detail"] == "No Genre found with id=999"
