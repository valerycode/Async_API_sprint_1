from typing import Optional
from uuid import UUID

from api.v1.model_mixin import BaseModelMixin


class Person(BaseModelMixin):
    """Schema for Person list"""

    full_name: str


class PersonDetail(Person):
    """Schema for Person detail"""

    roles: Optional[list[str]] = []
    film_ids: Optional[list[UUID]] = []


class Film(BaseModelMixin):
    """Schema for Film work list"""

    title: str
    imdb_rating: Optional[float] = None


class Genre(BaseModelMixin):
    """Schema for Genre detail"""

    name: str


class FilmDetail(Film):
    """Schema for Film work detail"""

    description: Optional[str] = None
    genres: Optional[list[Genre]] = []
    actors: Optional[list[Person]] = []
    writers: Optional[list[Person]] = []
    directors: Optional[list[Person]] = []
