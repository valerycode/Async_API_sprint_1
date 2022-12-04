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
    description: str = None


class ESFilmworkData(BaseModel):
    id: str
    imdb_rating: Optional[float]
    genres: list[str] = []
    title: str
    description: Optional[str]
    directors_names: list[str] = []
    actors_names: list[str] = []
    writers_names: list[str] = []
    directors: list[ESFilmPerson] = []
    actors: list[ESFilmPerson] = []
    writers: list[ESFilmPerson] = []
