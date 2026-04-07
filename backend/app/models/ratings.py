# from sqlmodel import SQLModel, Field, Relationship

# class RatingSource(SQLModel, table=True):
#   id: int | None = Field(default=None, primary_key=True)
#   name: str
#   max_score: float = Field(ge=0)

# class Rating(SQLModel, table=True):
#   id: int | None = Field(default=None, primary_key=True)
#   source_id: int = Field(foreign_key="source.id")
#   source: RatingSource = Relationship(back_populates="ratings")
#   score: float = Field(le=source.max_score, ge=0)

# class MovieRating(SQLModel, table=True):
#   movie_id: int | None = Field(default=None, primary_key=True, foreign_key="movie.id")
#   rating_id: int | None = Field(default=None, 
#     primary_key=True, foreign_key="ratingsource.id")