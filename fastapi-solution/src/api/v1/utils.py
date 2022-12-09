from typing import Optional

from fastapi import Query


class FilmSearchParams:
    """
    Класс задает параметры для поиска по фильму
    """

    def __init__(
        self,
        query: Optional[str] = Query(
            None,
            alias="query",
            title="Запрос",
            description="Осуществляет поиск по названию фильма",
        ),
        number: Optional[int] = Query(
            1,
            alias="page[number]",
            title="страница",
            description="Порядковый номер страницы результатов",
        ),
        size: Optional[int] = Query(
            50,
            alias="page[size]",
            title="размер страницы",
            description="Количество документов на странице",
        ),
    ) -> None:
        self.number = number
        self.size = size
        self.query = query


class FilmParams:
    """
    Класс задает параметры для вывода всех популярных фильмов.
    """

    def __init__(
        self,
        sort: Optional[str] = Query(
            "-imdb_rating",
            alias="sort",
            title="Сортировка по рейтингу",
            description=(
                "Сортирует по возрастанию и убыванию,"
                " -field если нужна сортировка"
                " по убыванию или field,"
                " если нужна сортировка по возрастанию."
                " По умолчанию сортирует по"
                " полю imdb_rating по убыванию."
            ),
            regex="-?imdb_rating",
        ),
        filter_genre_id: Optional[str] = Query(
            None,
            alias="filter[genre]",
            title="Фильтр жанров",
            description="Фильтрует фильмы по жанрам",
        ),
        number: Optional[int] = Query(
            1,
            alias="page[number]",
            title="страница",
            description="Порядковый номер страницы результатов",
        ),
        size: Optional[int] = Query(
            50,
            alias="page[size]",
            title="размер страницы",
            description="Количество документов на странице",
        ),
    ) -> None:
        self.sort = sort
        self.filter_genre_id = filter_genre_id
        self.number = number
        self.size = size


class GenreParams:
    """
    Класс задает параметры для вывода всех жанров.
    """

    def __init__(
        self,
        sort: Optional[str] = Query(
            "name",
            alias="sort",
            title="Сортировка по наименованию жанра",
            description=(
                "Сортирует по возрастанию и убыванию,"
                " -field если нужна сортировка"
                " по убыванию или field,"
                " если нужна сортировка по возрастанию."
                " По умолчанию сортирует по"
                " полю name в алфавитном порядке."
            ),
        ),
        number: Optional[int] = Query(
            1,
            alias="page[number]",
            title="страница",
            description="Порядковый номер страницы результатов",
        ),
        size: Optional[int] = Query(
            50,
            alias="page[size]",
            title="размер страницы",
            description="Количество документов на странице",
        ),
    ) -> None:
        self.sort = sort
        self.number = number
        self.size = size


class PersonParam:
    def __init__(
        self,
        number: Optional[int] = Query(
            1,
            alias="page[number]",
            title="страница",
            description="Порядковый номер страницы результатов",
        ),
        size: Optional[int] = Query(
            50,
            alias="page[size]",
            title="размер страницы",
            description="Количество документов на странице",
        ),
    ) -> None:
        self.size = size
        self.number = number


class PersonSearchParam:
    """
    Класс задает параметры для поиска персоны по имени
    """

    def __init__(
        self,
        query: Optional[str] = Query(
            None,
            title="Запрос",
            description="Осуществляет поиск по имени персоны",
        ),
        number: Optional[int] = Query(
            1,
            alias="page[number]",
            title="страница",
            description="Порядковый номер страницы результатов",
        ),
        size: Optional[int] = Query(
            50,
            alias="page[size]",
            title="размер страницы",
            description="Количество документов на странице",
        ),
    ) -> None:
        self.query = query
        self.size = size
        self.number = number
