from enum import Enum

from app.core.config import settings


class RequiredMovieFields(str, Enum):
    Title = "Title"
    Plot = "Plot"
    Actors = "Actors"
    Year = "Year"
    Genre = "Genre"
    Director = "Director"


OMDB_BASE_URL = f"https://www.omdbapi.com/?apikey={settings.OMDB_API_KEY}"
DEFAULT_TIMEOUT = 60
