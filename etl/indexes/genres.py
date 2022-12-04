from indexes.schema_template import TEMPLATE_INDEX_BODY

GENRES_INDEX_BODY: dict = {
    **TEMPLATE_INDEX_BODY,
    "mappings": {
        "dynamic": "strict",
        "properties": {
            "id": {"type": "keyword"},
            "name": {"type": "keyword"},
            "description": {"type": "text", "analyzer": "ru_en"},
        },
    },
}
