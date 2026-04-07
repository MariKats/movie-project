def assert_validation_error(response, expected_keyword: str):
    assert response.status_code == 422
    detail = response.json()["detail"]
    assert isinstance(detail, list)
    assert any(expected_keyword in item["msg"] for item in detail)


def test_movies_negative_offset_validation(test_client):
    response = test_client.get("/movies?offset=-1")
    assert_validation_error(response, "greater than or equal to 0")


def test_movies_limit_too_high_validation(test_client):
    response = test_client.get("/movies?limit=20")
    assert_validation_error(response, "less than or equal to 10")


def test_movies_invalid_sort_validation(test_client):
    response = test_client.get("/movies?sort=invalid")
    assert_validation_error(response, "Input should be")


def test_movies_invalid_order_by_validation(test_client):
    response = test_client.get("/movies?order_by=rating")
    assert_validation_error(response, "Input should be")


def test_movie_id_negative_validation(test_client):
    response = test_client.get("/movies/-1")
    assert_validation_error(response, "greater than or equal to 0")
