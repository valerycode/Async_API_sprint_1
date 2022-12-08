from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from api.v1.models import Film, FilmDetail
from api.v1.utils import FilmParams, FilmSearchParams
from models.film import ESFilm
from services.film import FilmService, get_film_service

MOVIES_NOT_IN_DB = "Movies can not be taken from ElasticSearch."
FILM_NOT_FOUND = "Film with such uuid {uuid} was not found in Elasticsearch."
FILM_NOT_IN_SEARCH_RESULTS = "Can't find film with such query."

router = APIRouter()


@router.get(
    path="/",
    response_model=list[Film],
    summary="Главная страница кинопроизведений",
    description="Полный перечень кинопроизведений",
    response_description="Список из названий и рейтингов кинопроизведений",
)
async def film_list(
    params: FilmParams = Depends(),
    film_service: FilmService = Depends(get_film_service),
) -> list[Film]:
    es_films: list[ESFilm] = await film_service.get_films(params)
    if not es_films:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=MOVIES_NOT_IN_DB
        )
    films = [
        Film(uuid=film.uuid, title=film.title, imdb_rating=film.imdb_rating)
        for film in es_films
    ]
    return films


@router.get(
    path="/{film_uuid}",
    response_model=Optional[FilmDetail],
    summary="Поиск кинопроизведения по ID",
    description="Поиск кинопроизведения по ID",
    response_description="Полная информация о фильме",
)
async def film_details(
    film_uuid: str, film_service: FilmService = Depends(get_film_service)
) -> Optional[FilmDetail]:
    film = await film_service.get_by_id(target_id=film_uuid, schema=ESFilm)
    if not film:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=FILM_NOT_FOUND.format(uuid=film_uuid),
        )
    return FilmDetail(
        uuid=film.uuid,
        title=film.title,
        imdb_rating=film.imdb_rating,
        description=film.description,
        genres=film.genres,
        actors=film.actors,
        writers=film.writers,
        directors=film.directors,
    )


@router.get(
    path="/search/",
    response_model=list[FilmDetail],
    summary="Поиск кинопроизведений",
    description="Полнотекстовый поиск по кинопроизведениям",
    response_description="Список из названий и рейтингов кинопроизведений",
)
async def search_film(
    params: FilmSearchParams = Depends(),
    film_service: FilmService = Depends(get_film_service),
) -> list[FilmDetail]:
    es_films = await film_service.get_films(params)
    if not es_films:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=FILM_NOT_IN_SEARCH_RESULTS
        )
    films = [
        FilmDetail(
            uuid=film.uuid,
            title=film.title,
            imdb_rating=film.imdb_rating,
            description=film.description,
            genres=film.genres,
            actors=film.actors,
            writers=film.writers,
            directors=film.directors,
        )
        for film in es_films
    ]
    return films
