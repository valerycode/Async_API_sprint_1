import logging
from http import HTTPStatus

from backoff import backoff
from config import es_settings
from elasticsearch import (
    ConnectionError,
    ConnectionTimeout,
    Elasticsearch,
    RequestError,
    SerializationError,
    TransportError,
)
from elasticsearch.helpers import bulk
from etl.indexes.movies import MOVIES_INDEX
from etl.indexes.genres import GENRES_INDEX

from etl.models import ESFilmworkData

logger = logging.getLogger(__name__)

INDEX_CREATED = (
    "Index {name} is created." " Response from Elasticsearch: {response}."
)
PING_MESSAGE = "Ping from Elasticsearch server: {message}."
INDEXES = {'movies': MOVIES_INDEX, 'genres': GENRES_INDEX}


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
    def create_indexes(self) -> None:
        for index in INDEXES:
            if not self.client.indices.exists(index=index):
                response = self.client.indices.create(
                    index=index,
                    ignore=HTTPStatus.BAD_REQUEST.value,
                    body=INDEXES[index],
                )
                logger.debug(
                    INDEX_CREATED.format(name=index, response=response)
                )

    @backoff(exceptions=(SerializationError,), logger=logger)
    def load_films_to_elastic(self, data: list[ESFilmworkData]) -> None:
        documents = [
            {"_index": "movies", "_id": row.id, "_source": row.dict()}
            for row in data
        ]
        bulk(self.client, documents)

    def load_genres_to_elastic(self):
        pass

    def load_persons_to_elastic(self):
        pass