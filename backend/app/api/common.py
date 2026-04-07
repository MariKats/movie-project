from typing import Annotated
from fastapi import Query, Depends
from sqlmodel import Session, select
from app.core.database import get_session
from app.schemas.schemas import FilterParamsBasic, FilterParams, Item, Movie, NameBase, StudioBase
from app.models.actors import Actor
from app.models.directors import Director
from app.models.genres import Genre
from app.models.studios import Studio

SessionDep = Annotated[Session, Depends(get_session)]

from enum import Enum

class CreateField(str, Enum):
  actor = "actor"
  genre = "genre"
  director = "director"
  studio = "studio" 

field_to_model = {
  "actor": Actor,
  "director": Director,
  "genre": Genre,
  "studio": Studio
}

def sanitize_input(input: list[str]):
  return [item.strip().title() for item in input]

def find_or_create_item(session: Session, field: CreateField, base: NameBase | StudioBase) -> Actor | Director | Genre | Studio:
  model = field_to_model[field.value]
  item = session.exec(select(model).where(model.name == base.name)).first()
  if not item:
    item = model(name=base.name, headquarters=base.headquarters) if isinstance(base, StudioBase) else model(name=base.name)
    session.add(item)
  return item

def find_or_create_items(session: Session, field: CreateField, input: list[str]) -> list[Actor] | list[Director | list[Genre]]:
  return [find_or_create_item(session, field, NameBase(name=item_name)) for item_name in sanitize_input(input)]

def filter_items(query: select, session: Session, filter_query: Annotated[FilterParamsBasic, Query()]) -> list[Item]:
  query = query.offset(filter_query.offset)
  if filter_query.limit is not None:
    query = query.limit(filter_query.limit)
  results = session.exec(query).all()
  if filter_query.sort == "desc":
    return sorted(results, key=lambda x: x.id, reverse=True)
  return results

def filter_movies(query: select, session: Session, filter_query: Annotated[FilterParams, Query()]) -> list[Movie]:
  query = query.offset(filter_query.offset)
  if filter_query.limit is not None:
    query = query.limit(filter_query.limit)

  results = session.exec(query).all()
  if filter_query.order_by:
    if filter_query.order_by == "title":
      return sorted(results, key=lambda d: d.title, reverse=(filter_query.sort=="desc"))
    if filter_query.order_by == "year":
      return sorted(results, key=lambda d: d.year, reverse=(filter_query.sort=="desc"))
  if filter_query.sort == "desc":
    return sorted(results, key=lambda x: x.id, reverse=True)
  return results

def has_default_filters(filter_query: FilterParams) -> bool:
  return all(
      getattr(filter_query, name) == field.default 
      for name, field in FilterParams.model_fields.items()
  )
