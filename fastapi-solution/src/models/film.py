from datetime import date
from typing import Optional

from pydantic.fields import Field

from models.genre import ESGenreBase
from models.person import ESPersonBase
from v1.model_mixin import BaseModelMixin


class ESFilm(BaseModelMixin):
    uuid: str = Field(..., alias="id")
    imdb_rating: Optional[float] = 0.0
    type: str
    age_limit: Optional[int] = 0
    creation_date: Optional[date] = None
    genres: list[ESGenreBase] = []
    title: str
    file_path: Optional[str] = None
    description: Optional[str] = None
    directors_names: list[str] = []
    actors_names: list[str] = []
    writers_names: list[str] = []
    directors: list[ESPersonBase] = []
    actors: list[ESPersonBase] = []
    writers: list[ESPersonBase] = []
