from enum import Enum


class RequiredMovieFields(str, Enum):
    Title = "Title"
    Plot = "Plot"
    Actors = "Actors"
    Year = "Year"
    Genre = "Genre"
    Director = "Director"
