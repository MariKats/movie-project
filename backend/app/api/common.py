from enum import Enum
from typing import Annotated

from fastapi import Depends, Query
from sqlmodel import Session, col, select

from app.core.database import get_session
from app.models.actors import Actor
from app.models.directors import Director
from app.models.genres import Genre
from app.models.studios import Studio
from app.schemas.schemas import FilterParams, FilterParamsBasic, Item, Movie, NameBase

SessionDep = Annotated[Session, Depends(get_session)]


class CreateField(str, Enum):
    actor = "actor"
    genre = "genre"
    director = "director"
    studio = "studio"


MODEL_MAP = {
    "actor": Actor,
    "genre": Genre,
    "director": Director,
    "studio": Studio,
}


def sanitize_input(input: list[str]):
    return [item.strip().title() for item in input]


def find_or_create_item(
    session: Session, field: CreateField, base: NameBase
) -> Actor | Director | Genre | Studio:
    model = MODEL_MAP[field.value]
    item = session.exec(select(model).where(model.name == base.name)).first()
    if not item:
        item = model(**base.model_dump())
        session.add(item)
    return item


def find_or_create_items(
    session: Session, field: CreateField, input: list[str]
) -> list[Actor | Director | Genre]:
    model = MODEL_MAP[field.value]
    item_names = sanitize_input(input)
    found: list[Actor | Director | Genre] = session.exec(
        select(model).where(col(model.name).in_(item_names))
    ).all()
    found_names: str = [i.name for i in found]
    to_be_created = [
        item_name for item_name in item_names if item_name not in found_names
    ]
    items = found + [
        session.merge(model(name=item_name)) for item_name in to_be_created
    ]
    return items


def filter_items(
    query: select, session: Session, filter_query: Annotated[FilterParamsBasic, Query()]
) -> list[Item]:
    query = query.offset(filter_query.offset)
    if filter_query.limit is not None:
        query = query.limit(filter_query.limit)
    results = session.exec(query).all()
    if filter_query.sort == "desc":
        return sorted(results, key=lambda x: x.id, reverse=True)
    return results


def filter_movies(
    query: select, session: Session, filter_query: Annotated[FilterParams, Query()]
) -> list[Movie]:
    query = query.offset(filter_query.offset)
    if filter_query.limit is not None:
        query = query.limit(filter_query.limit)

    results = session.exec(query).all()
    if filter_query.order_by:
        if filter_query.order_by == "title":
            return sorted(
                results, key=lambda d: d.title, reverse=(filter_query.sort == "desc")
            )
        if filter_query.order_by == "year":
            return sorted(
                results, key=lambda d: d.year, reverse=(filter_query.sort == "desc")
            )
    if filter_query.sort == "desc":
        return sorted(results, key=lambda x: x.id, reverse=True)
    return results


def has_default_filters(filter_query: FilterParams) -> bool:
    return all(
        getattr(filter_query, name) == field.default
        for name, field in FilterParams.model_fields.items()
    )
