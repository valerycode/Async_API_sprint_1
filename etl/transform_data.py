import logging
from typing import Iterator, Union

from backoff import backoff
from models import ESFilmworkData, ESPerson, ESGenre
from pydantic import ValidationError

logger = logging.getLogger(__name__)


class DataTransform:
    """A class to validate and transform postgres data with pydantic model."""

    def __init__(self):
        self.roles = ["director", "actor", "writer"]

    def extract_names_and_ids_by_role(self, persons: list[dict]) -> dict:
        persons_by_role = {}
        for role in self.roles:
            names_and_ids = [
                {"id": field["person_id"],
                 "full_name": field["person_name"]}
                for field in persons
                if field["person_role"] == role
            ]
            names = [name["full_name"] for name in names_and_ids]
            persons_by_role[role] = (names_and_ids, names)
        return persons_by_role

    @backoff((ValidationError,), logger=logger)
    def transform_and_validate_data(self, data: Iterator, index: str) -> \
            list[Union[ESFilmworkData, ESGenre, ESPerson]]:
        es_objects = []
        if index == 'movies':
            for film in data:
                film_persons = self.extract_names_and_ids_by_role(
                    film["persons"])
                es_filmwork = ESFilmworkData(
                    id=film["id"],
                    imdb_rating=film["imdb_rating"],
                    genre=film["genres"],
                    title=film["title"],
                    description=film["description"],
                    directors_names=film_persons["director"][1],
                    actors_names=film_persons["actor"][1],
                    writers_names=film_persons["writer"][1],
                    directors=film_persons["director"][0],
                    actors=film_persons["actor"][0],
                    writers=film_persons["writer"][0],
                )
                es_objects.append(es_filmwork)
        elif index == 'genres':
            for genre in data:
                es_genre = ESGenre(
                    id=genre["id"],
                    name=genre["name"],
                    description=genre["description"]
                )
                es_objects.append(es_genre)
        else:
            for person in data:
                es_person = ESPerson(
                    id=person["id"],
                    full_name=person["full_name"],
                    roles=person["roles"],
                    film_ids=[film["fw_id"] for film in person["films"]]
                )
                es_objects.append(es_person)
        return es_objects
