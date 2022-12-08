from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from api.v1.models import Film, PersonDetail
from api.v1.utils import PersonSearchParam
from models.person import ESPerson
from services.film import FilmService, get_film_service
from services.person import PersonService, get_person_service

PERSON_NOT_FOUND = (
    "Person with such uuid {uuid}" " was not found in Elasticsearch."
)
NO_PERSONS = "Can not get persons from Elasticsearch."
NO_PERSON_WITH_THIS_NAME = "Person with such name {name} is not in database."

router = APIRouter()


@router.get(
    "/{person_uuid}",
    response_model=PersonDetail,
    summary="Поиск персоны по UUID",
    description="Поиск персоны по UUID",
    response_description="Имя, роль и фильмография персоны",
)
async def person_details(
    uuid: str, person_service: PersonService = Depends(get_person_service)
) -> PersonDetail:
    es_person = await person_service.get_by_id(uuid, schema=ESPerson)
    if not es_person:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=PERSON_NOT_FOUND
        )
    return PersonDetail(
        uuid=es_person.uuid,
        full_name=es_person.full_name,
        roles=es_person.roles,
        film_ids=es_person.film_ids,
    )


@router.get(
    "/{person_uuid}/film",
    response_model=list[Film],
    summary="Поиск фильмов по UUID персоны",
    description="Поиск фильмов по UUID персоны",
    response_description="Название и рейтинг фильмов с участием персоны",
)
async def person_films(
    uuid: str,
    person_service: PersonService = Depends(get_person_service),
    film_service: FilmService = Depends(get_film_service),
) -> list[Film]:
    es_person = await person_service.get_by_id(uuid, schema=ESPerson)
    person_films = await film_service.get_person_films(es_person.film_ids)
    return [
        Film(uuid=film.uuid, title=film.title, imdb_rating=film.imdb_rating)
        for film in person_films
    ]


@router.get(
    "/search/",
    response_model=list[PersonDetail],
    description="Поиск персоны по имени",
    summary="Поиск персоны по имени",
    response_description="Фильмы и роли персоны",
)
async def person_search(
    params: PersonSearchParam = Depends(),
    person_service: PersonService = Depends(get_person_service),
) -> Optional[list[PersonDetail]]:
    es_persons = await person_service.get_persons(params)
    if not es_persons:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=NO_PERSON_WITH_THIS_NAME.format(name=params.query),
        )
    persons = [
        PersonDetail(
            uuid=person.uuid,
            full_name=person.full_name,
            roles=person.roles,
            film_ids=person.film_ids,
        )
        for person in es_persons
    ]
    return persons
