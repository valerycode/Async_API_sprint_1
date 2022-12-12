from typing import Optional

from pydantic.fields import Field

from api.v1.model_mixin import BaseModelMixin


class ESPersonBase(BaseModelMixin):
    uuid: str = Field(..., alias="id")
    full_name: str


class ESPerson(ESPersonBase):
    roles: Optional[list[str]] = []
    film_ids: Optional[list[str]] = []
