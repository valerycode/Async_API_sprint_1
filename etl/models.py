from datetime import date
from typing import Optional

from pydantic import BaseModel


class ESFilmPerson(BaseModel):
    id: str
    full_name: str


class ESPerson(ESFilmPerson):
    roles: list[str] = []
    film_ids: list[str]


class ESGenre(BaseModel):
    id: str
    name: str
    description: Optional[str] = None


class ESFilmworkData(BaseModel):
    id: str
    imdb_rating: Optional[float] = 0.0
    type: str
    age_limit: Optional[int] = 0
    creation_date: Optional[date]
    genres: list[ESGenre] = []
    title: str
    file_path: Optional[str] = None
    description: Optional[str] = None
    directors_names: list[str] = []
    actors_names: list[str] = []
    writers_names: list[str] = []
    directors: list[ESFilmPerson] = []
    actors: list[ESFilmPerson] = []
    writers: list[ESFilmPerson] = []
