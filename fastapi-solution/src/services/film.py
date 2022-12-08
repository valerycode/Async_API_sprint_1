from functools import lru_cache
from typing import Optional, Union

import elasticsearch.exceptions
from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from api.v1.utils import FilmParams, FilmSearchParams
from db.elastic import get_elastic
from db.redis import get_redis
from models.film import ESFilm
from services.mixins import ServiceMixin


class FilmService(ServiceMixin):
    index_name = "movies"
    model = ESFilm
    search_fields = [
        "title^5",
        "description^4",
        "genres_titles^3",
        "actors_names^3",
        "writers_names^2",
        "directors_names",
    ]

    async def get_films(
        self, params: Union[FilmParams, FilmSearchParams]
    ) -> Optional[list[ESFilm]]:
        body = self.es_request_body(params, self.search_fields)
        return await self.search_in_elastic(body=body, schema=self.model)

    async def get_person_films(self, ids: list[str]):
        try:
            res = await self.elastic.mget(
                body={"ids": ids}, index=self.index_name
            )
        except elasticsearch.exceptions.NotFoundError:
            return []
        return [self.model(**doc["_source"]) for doc in res["docs"]]


@lru_cache()
def get_film_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis=redis, elastic=elastic, index="movies")
