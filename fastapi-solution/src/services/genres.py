from functools import lru_cache
from typing import Optional

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from api.v1.utils import GenreParams
from db.elastic import get_elastic
from db.redis import get_redis
from models.genre import ESGenre
from services.mixins import ServiceMixin


class GenreService(ServiceMixin):
    index_name = "genres"
    model = ESGenre
    search_fields = []

    async def get_genres(self, params: GenreParams) -> Optional[list[ESGenre]]:
        body = self.es_request_body(params, self.search_fields)
        return await self.search_in_elastic(body=body, schema=self.model)


@lru_cache()
def get_genre_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic, index="genres")
