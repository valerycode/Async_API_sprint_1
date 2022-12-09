from typing import Optional

from pydantic import BaseModel
from pydantic.fields import Field


class ESPersonBase(BaseModel):
    uuid: str = Field(..., alias="id")
    full_name: str


class ESPerson(ESPersonBase):
    roles: Optional[list[str]] = []
    film_ids: Optional[list[str]] = []
