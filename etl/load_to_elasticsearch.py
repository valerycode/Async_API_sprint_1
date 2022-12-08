import logging
from http import HTTPStatus
from typing import Union

from elasticsearch import (ConnectionError, ConnectionTimeout, Elasticsearch,
                           RequestError, SerializationError, TransportError)
from elasticsearch.helpers import bulk

from backoff import backoff
from config import es_settings
from indexes.genres import GENRES_INDEX_BODY
from indexes.movies import MOVIES_INDEX_BODY
from indexes.persons import PERSONS_INDEX_BODY
from models import ESFilmworkData, ESGenre, ESPerson

logger = logging.getLogger(__name__)

INDEX_CREATED = (
    "Index {name} is created. Response from Elasticsearch: {response}."
)
PING_MESSAGE = "Ping from Elasticsearch server: {message}."
INDEXES_BODY = {
    "movies": MOVIES_INDEX_BODY,
    "genres": GENRES_INDEX_BODY,
    "persons": PERSONS_INDEX_BODY,
}


class ElasticsearchLoader:
    """A class to get data and load in Elasticsearch."""

    def __init__(self) -> None:
        self.client = None

    @backoff(
        exceptions=(ConnectionError, TransportError, ConnectionTimeout),
        logger=logger,
    )
    def connect(self):
        self.client = Elasticsearch(**es_settings.dict())
        logging.info(PING_MESSAGE.format(message=self.client.ping()))

    @backoff(exceptions=(RequestError,), logger=logger)
    def create_index(self, index: str) -> None:
        if not self.client.indices.exists(index=index):
            response = self.client.indices.create(
                index=index,
                ignore=HTTPStatus.BAD_REQUEST.value,
                body=INDEXES_BODY[index],
            )
            logger.debug(INDEX_CREATED.format(name=index, response=response))

    @backoff(exceptions=(SerializationError,), logger=logger)
    def load_data_to_elastic(
        self, data: list[Union[ESFilmworkData, ESGenre, ESPerson]], index: str
    ) -> None:
        documents = [
            {"_index": index, "_id": row.id, "_source": row.dict()}
            for row in data
        ]
        bulk(self.client, documents)
