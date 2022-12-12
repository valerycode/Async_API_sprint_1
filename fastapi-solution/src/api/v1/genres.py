from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from api.v1.models import Genre
from api.v1.utils import GenreParams
from models.genre import ESGenre
from services.genres import GenreService, get_genre_service

NO_GENRES = "Can not get genres from Elasticsearch."
GENRE_NOT_FOUND = "Genre with such uuid {uuid} was not found in Elasticsearch."

router = APIRouter()


@router.get(
    path="/",
    response_model=list[Genre],
    summary="Главная страница жанров",
    description="Полный перечень жанров",
    response_description="Список с полной информацией о жанрах",
)
async def get_genres(
    params: GenreParams = Depends(),
    genre_service: GenreService = Depends(get_genre_service),
) -> list[Genre]:
    es_genres = await genre_service.get_genres(params)
    if not es_genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=NO_GENRES)
    genres = [Genre(uuid=genre.uuid, name=genre.name) for genre in es_genres]
    return genres


@router.get(
    "/{uuid}",
    response_model=Optional[Genre],
    summary="Поиск жанра по UUID",
    description="Поиск жанра по UUID",
    response_description="Полная информация о жанре",
)
async def genre_details(
    uuid: str, genre_service: GenreService = Depends(get_genre_service)
) -> Optional[Genre]:
    es_genre = await genre_service.get_by_id(uuid, schema=ESGenre)
    if not es_genre:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=GENRE_NOT_FOUND.format(uuid=uuid),
        )
    return Genre(uuid=es_genre.uuid, name=es_genre.name)
