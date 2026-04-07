from fastapi import FastAPI

from app.api.routes import actors, directors, genres, movies, studios

app = FastAPI()

app.include_router(genres.router)
app.include_router(movies.router)
app.include_router(actors.router)
app.include_router(directors.router)
app.include_router(studios.router)
