import logging
from datetime import datetime
from typing import Iterator

import psycopg2
from psycopg2 import DatabaseError, OperationalError, ProgrammingError
from psycopg2.extras import RealDictCursor

from backoff import backoff
from config import etl_settings, pg_settings
from queries.films import FILMWORKS_QUERY
from queries.genres import GENRE_QUERY
from queries.persons import PERSON_QUERY

INDEXES_QUERIES = {
    "movies": FILMWORKS_QUERY,
    "genres": GENRE_QUERY,
    "persons": PERSON_QUERY,
}

logger = logging.getLogger(__name__)

CONNECT_TO_POSTGRES = "Connect to Postgres..."
POSTGRES_CONNECTION = "Connection to Postgres succeeded."
DATA_EXTRACTED = "Data of {objects} extracted."


class PostgresExtractor:
    """A class to extract Postgres data and transform it to pydantic format."""

    def __init__(self) -> None:
        self.connection = None
        self.cursor = None

    @backoff(exceptions=(OperationalError,), logger=logger)
    def connect_to_postgres(self) -> None:
        logger.info(CONNECT_TO_POSTGRES)
        self.connection = psycopg2.connect(
            **pg_settings.dict(), cursor_factory=RealDictCursor
        )
        self.cursor = self.connection.cursor()
        logger.info(POSTGRES_CONNECTION)

    @backoff(exceptions=(DatabaseError, ProgrammingError), logger=logger)
    def extract_data_from_pg(
        self, date_last_modified: datetime, index: str
    ) -> Iterator:
        """Extract data from Postgres"""
        self.cursor.execute(INDEXES_QUERIES[index], (date_last_modified,))
        while rows := self.cursor.fetchmany(etl_settings.BATCH_SIZE):
            logger.info(DATA_EXTRACTED.format(objects=index))
            yield rows
