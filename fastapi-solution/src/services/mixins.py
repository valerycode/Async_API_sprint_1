from typing import Optional, Union

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError

from api.v1.utils import (FilmParams, FilmSearchParams, GenreParams,
                          PersonParam, PersonSearchParam)
from core.config import CACHE_EXPIRE_IN_SECONDS
from models.film import ESFilm
from models.genre import ESGenre
from models.person import ESPerson

Schemas: tuple = (ESFilm, ESGenre, ESPerson)
ES_schemas = Union[Schemas]


class ServiceMixin:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch, index: str):
        self.redis = redis
        self.elastic = elastic
        self.index = index

    async def search_in_elastic(
        self, body: dict, schema: Schemas
    ) -> Optional[ES_schemas]:
        try:
            docs = await self.elastic.search(index=self.index, body=body)
            return [schema(**row["_source"]) for row in docs["hits"]["hits"]]
        except NotFoundError:
            return None

    async def get_by_id(
        self, target_id: str, schema: Schemas
    ) -> Optional[ES_schemas]:
        instance = await self._get_result_from_cache(key=target_id)
        if not instance:
            instance = await self._get_data_from_elastic_by_id(
                target_id=target_id, schema=schema
            )
            if not instance:
                return None
            await self._put_data_to_cache(
                key=instance.uuid, instance=instance.json()
            )
            return instance
        return schema.parse_raw(instance)

    async def _get_data_from_elastic_by_id(
        self, target_id: str, schema: Schemas
    ) -> Optional[ES_schemas]:
        try:
            doc = await self.elastic.get(index=self.index, id=target_id)
            return schema(**doc["_source"])
        except NotFoundError:
            return None

    async def _get_result_from_cache(self, key: str) -> Optional[bytes]:
        data = await self.redis.get(key=key)
        return data or None

    async def _put_data_to_cache(
        self, key: str, instance: Union[bytes, str]
    ) -> None:
        await self.redis.set(
            key=key, value=instance, expire=CACHE_EXPIRE_IN_SECONDS
        )

    def es_request_body(
        self,
        params: Union[
            FilmParams,
            PersonSearchParam,
            FilmSearchParams,
            GenreParams,
            PersonParam,
        ],
        search_fields: Optional[list[str]],
    ) -> dict:
        sort = {}
        if isinstance(params, FilmParams) or isinstance(params, GenreParams):
            order = "desc" if params.sort.startswith("-") else "asc"
            sort_field = f"{params.sort.removeprefix('-')}"
            sort = {sort_field: {"order": order}}
        if isinstance(params, FilmParams):
            if params.filter_genre_id:
                return {
                    "size": params.size,
                    "from": (params.number - 1) * params.size,
                    "query": {
                        "nested": {
                            "path": "genres",
                            "query": {
                                "match": {"genres.id": params.filter_genre_id}
                            },
                        }
                    },
                    "sort": sort,
                }
            else:
                return {
                    "size": params.size,
                    "from": (params.number - 1) * params.size,
                    "query": {"match_all": {}},
                    "sort": sort,
                }
        elif isinstance(params, PersonSearchParam) or isinstance(
            params, FilmSearchParams
        ):
            return {
                "size": params.size,
                "from": (params.number - 1) * params.size,
                "query": {
                    "multi_match": {
                        "query": params.query,
                        "fuzziness": "auto",
                        "fields": search_fields,
                    }
                },
            }
        else:
            return {
                "size": params.size,
                "from": (params.number - 1) * params.size,
                "query": {"match_all": {}},
                "sort": sort,
            }
