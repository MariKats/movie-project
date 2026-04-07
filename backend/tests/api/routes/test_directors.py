from app.fake_data import directors


def test_get_directors(test_client):
    response = test_client.get("/directors")
    assert response.status_code == 200
    assert response.json() == directors


def test_get_directors_offset_limit(test_client):
    response = test_client.get("/directors?offset=5&limit=2")
    assert response.status_code == 200
    result = response.json()
    assert result == directors[5:7]
    assert len(result) == 2
    assert result[0].get("id") == 5
    assert result[1].get("id") == 6


def test_get_directors_offset_limit_sort_desc(test_client):
    response = test_client.get("/directors?offset=5&limit=2&sort=desc")
    assert response.status_code == 200
    result = response.json()
    assert len(result) == 2
    assert result[0].get("id") == 6
    assert result[1].get("id") == 5


def test_get_directors_limit(test_client):
    response = test_client.get("/directors?limit=2")
    assert response.status_code == 200
    result = response.json()
    assert result == directors[:2]
    assert len(result) == 2
    assert result[0].get("id") == 0
    assert result[1].get("id") == 1


def test_get_directors_offset(test_client):
    response = test_client.get("/directors?offset=33")
    assert response.status_code == 200
    result = response.json()
    assert result == directors[33:]
    assert len(result) == 3
    assert result[0].get("id") == 33
    assert result[1].get("id") == 34
    assert result[2].get("id") == 35


def test_get_director(test_client):
    response = test_client.get("/directors/6")
    assert response.status_code == 200
    result = response.json()
    assert result == directors[6]
    assert result.get("name") == "Martin Scorsese"


def test_get_director_movies(test_client):
    response = test_client.get("/directors/6/movies")
    assert response.status_code == 200
    result = response.json()
    assert len(result) == 3
    assert result[0].get("title") == "Goodfellas"
    assert result[0].get("year") == 1990
    assert result[1].get("title") == "The Departed"
    assert result[1].get("year") == 2006
    assert result[2].get("title") == "Killers of the Flower Moon"
    assert result[2].get("year") == 2023


def test_get_director_movies_sort_desc(test_client):
    response = test_client.get("/directors/6/movies?sort=desc")
    assert response.status_code == 200
    result = response.json()
    assert len(result) == 3
    assert result[0].get("title") == "Killers of the Flower Moon"
    assert result[1].get("title") == "The Departed"
    assert result[2].get("title") == "Goodfellas"


def test_get_director_movies_order_by_year_sort_desc(test_client):
    response = test_client.get("/directors/6/movies?order_by=year&sort=desc")
    assert response.status_code == 200
    result = response.json()
    assert len(result) == 3
    assert result[0].get("title") == "Killers of the Flower Moon"
    assert result[1].get("title") == "The Departed"
    assert result[2].get("title") == "Goodfellas"


def test_get_director_not_found(test_client):
    response = test_client.get("/directors/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "No Director found with id=999."


def test_get_director_movies_not_found(test_client):
    response = test_client.get("/directors/999/movies")
    assert response.status_code == 404
    assert response.json()["detail"] == "No Director found with id=999"
