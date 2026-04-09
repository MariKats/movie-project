from backend.app.seed_data import studios


def test_get_studios(test_client):
    response = test_client.get("/studios")
    assert response.status_code == 200
    assert response.json() == studios


def test_get_studios_offset_limit(test_client):
    response = test_client.get("/studios?offset=5&limit=2")
    assert response.status_code == 200
    result = response.json()
    assert result == studios[5:7]
    assert len(result) == 2
    assert result[0].get("id") == 5
    assert result[1].get("id") == 6


def test_get_studios_offset_limit_sort_desc(test_client):
    response = test_client.get("/studios?offset=5&limit=2&sort=desc")
    assert response.status_code == 200
    result = response.json()
    assert len(result) == 2
    assert result[0].get("id") == 6
    assert result[1].get("id") == 5


def test_get_studios_limit(test_client):
    response = test_client.get("/studios?limit=2")
    assert response.status_code == 200
    result = response.json()
    assert result == studios[:2]
    assert len(result) == 2
    assert result[0].get("id") == 0
    assert result[1].get("id") == 1


def test_get_studios_offset(test_client):
    response = test_client.get("/studios?offset=17")
    assert response.status_code == 200
    result = response.json()
    assert result == studios[17:]
    assert len(result) == 3
    assert result[0].get("id") == 17
    assert result[1].get("id") == 18
    assert result[2].get("id") == 19


def test_get_studio(test_client):
    response = test_client.get("/studios/6")
    assert response.status_code == 200
    result = response.json()
    assert result == studios[6]
    assert result.get("name") == "Marvel Studios"


def test_get_studio_not_found(test_client):
    response = test_client.get("/studios/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "No Studio found with id=999."


def test_get_studio_movies_not_found(test_client):
    response = test_client.get("/studios/999/movies")
    assert response.status_code == 404
    assert response.json()["detail"] == "No Studio found with id=999"


def test_get_studio_movies(test_client):
    response = test_client.get("/studios/6/movies")
    assert response.status_code == 200
    result = response.json()
    assert len(result) == 2
    assert result[0].get("title") == "The Avengers"
    assert result[0].get("year") == 2012
    assert result[1].get("title") == "Deadpool & Wolverine"
    assert result[1].get("year") == 2024


def test_get_studio_movies_sort_desc(test_client):
    response = test_client.get("/studios/6/movies?sort=desc")
    assert response.status_code == 200
    result = response.json()
    assert len(result) == 2
    assert result[0].get("title") == "Deadpool & Wolverine"
    assert result[1].get("title") == "The Avengers"


def test_get_studio_movies_order_by_year_sort_desc(test_client):
    response = test_client.get("/studios/6/movies?order_by=year&sort=desc")
    assert response.status_code == 200
    result = response.json()
    assert len(result) == 2
    assert result[0].get("title") == "Deadpool & Wolverine"
    assert result[1].get("title") == "The Avengers"
