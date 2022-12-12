from pydantic.fields import Field

from api.v1.model_mixin import BaseModelMixin


class ESGenreBase(BaseModelMixin):
    uuid: str = Field(..., alias="id")
    name: str


class ESGenre(ESGenreBase):
    description: str = None
