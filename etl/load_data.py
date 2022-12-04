import logging
from datetime import datetime
from time import sleep

from config import etl_settings
from extract_from_postgres import PostgresExtractor
from load_to_elasticsearch import ElasticsearchLoader
from queries.films import FILMWORKS_QUERY
from queries.genres import GENRE_QUERY
from queries.persons import PERSON_QUERY
from state import JsonFileStorage, State
from transform_data import DataTransform

logging.basicConfig(
    level=etl_settings.LOGGING_LEVEL,
    filename=etl_settings.FILENAME,
    format="%(asctime)s, %(levelname)s, %(message)s, %(name)s",
    filemode=etl_settings.FILEMODE,
)

logger = logging.getLogger(__name__)

LOAD_MESSAGE = "Load in Elasticsearch {number} documents."
ERROR_MESSAGE = "ETL process failed. Error occurs: {error}."
INDEXES_QUERIES = {
    "movies": FILMWORKS_QUERY,
    "genres": GENRE_QUERY,
    "persons": PERSON_QUERY,
}


class ETL:
    def __init__(self):
        self.postgres = PostgresExtractor()
        self.elastic = ElasticsearchLoader()
        self.transform = DataTransform()
        self.state = State(JsonFileStorage(etl_settings.STATE_FILE_NAME))

    def load_data_from_postgres_to_elastic(self, index: str):
        """Load data from Postgres to Elasticsearch"""
        last_modified = self.state.get_state(f"{index}_modified")
        date_last_modified = last_modified if last_modified else datetime.min
        objects_number = 0
        for data in self.postgres.extract_data_from_pg(
            date_last_modified, index
        ):
            self.state.set_state(
                f"{index}_modified", datetime.now().isoformat()
            )
            es_data = self.transform.transform_and_validate_data(data, index)
            self.elastic.load_data_to_elastic(es_data, index)
            objects_number += len(es_data)
            logger.debug(LOAD_MESSAGE.format(number=objects_number))


def main():
    while True:
        etl = ETL()
        try:
            etl.postgres.connect_to_postgres()
            etl.elastic.connect()
            for index_name in INDEXES_QUERIES:
                etl.elastic.create_index(index_name)
                etl.load_data_from_postgres_to_elastic(index_name)
        except Exception as error:
            logger.error(ERROR_MESSAGE.format(error=error))
        finally:
            etl.postgres.connection.close()
            sleep(etl_settings.TIME_INTERVAL)


if __name__ == "__main__":
    main()
