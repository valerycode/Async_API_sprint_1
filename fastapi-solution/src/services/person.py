from functools import lru_cache
from typing import Optional, Union

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from api.v1.utils import PersonParam, PersonSearchParam
from db.elastic import get_elastic
from db.redis import get_redis
from models.person import ESPerson
from services.mixins import ServiceMixin


class PersonService(ServiceMixin):
    index_name = "persons"
    model = ESPerson
    search_fields = ["full_name"]

    async def get_persons(
        self, params: Union[PersonParam, PersonSearchParam]
    ) -> Optional[list[ESPerson]]:
        body = self.es_request_body(params, self.search_fields)
        return await self.search_in_elastic(body=body, schema=self.model)


@lru_cache()
def get_person_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(redis=redis, elastic=elastic, index="persons")
