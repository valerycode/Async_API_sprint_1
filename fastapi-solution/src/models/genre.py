from pydantic import BaseModel
from pydantic.fields import Field


class ESGenreBase(BaseModel):
    uuid: str = Field(..., alias="id")
    name: str


class ESGenre(ESGenreBase):
    description: str = None
