from sqlalchemy import select
from sqlmodel import Session

from app.api.common import (
    CreateField,
    find_or_create_item,
    find_or_create_items,
    has_default_filters,
    sanitize_input,
)
from app.models.actors import Actor
from app.schemas.schemas import FilterParams, NameBase


def test_sanitize_input():
    input = ["  actor1 ", "actor2", " ACTOR3 "]
    expected_output = ["Actor1", "Actor2", "Actor3"]
    assert sanitize_input(input) == expected_output


def test_sanitize_input_empty():
    input = []
    expected_output = []
    assert sanitize_input(input) == expected_output


def test_find_or_create_item(session: Session):
    session.exec(select(Actor).where(Actor.name == "Test Actor")).first() is None
    base = NameBase(name="Test Actor")
    item = find_or_create_item(session, CreateField.actor, base)
    assert item.name == "Test Actor"
    found_item = find_or_create_item(session, CreateField.actor, base)
    assert found_item.id == item.id


def test_find_or_create_items(session: Session):
    input = ["  actor1 ", "actor2", " ACTOR3 "]
    expected_names = ["Actor1", "Actor2", "Actor3"]
    for name in expected_names:
        session.exec(select(Actor).where(Actor.name == name)).first() is None
    items = find_or_create_items(session, CreateField.actor, input)
    assert len(items) == 3
    for item, expected_name in zip(items, expected_names):
        assert item.name == expected_name
    found_items = find_or_create_items(session, CreateField.actor, input)
    assert len(found_items) == 3
    for found_item, item in zip(found_items, items):
        assert found_item.id == item.id


def test_has_default_filters():
    assert has_default_filters(FilterParams())
    assert has_default_filters(FilterParams(offset=0))
    assert has_default_filters(FilterParams(limit=None, offset=0, sort="asc"))
    assert not has_default_filters(FilterParams(limit=5, sort="desc"))
    assert not has_default_filters(FilterParams(limit=5, offset=0, sort="asc"))
