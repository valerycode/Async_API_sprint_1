FILMWORKS_QUERY = """
        SELECT
           fw.id,
           fw.title,
           fw.description,
           fw.rating as imdb_rating,
           fw.type,
           fw.created,
           fw.modified,
           fw.creation_date,
           fw.file_path,
           fw.age_limit,
           COALESCE (
               json_agg(
                   DISTINCT jsonb_build_object(
                       'person_role', pfw.role,
                       'person_id', p.id,
                       'person_name', p.full_name
                   )
               ) FILTER (WHERE p.id is not null),
               '[]'
           ) as persons,
           COALESCE (
                json_agg(
                    DISTINCT jsonb_build_object(
                        'g_id', g.id,
                        'g_name', g.name,
                        'g_description', g.description
                        )
                        ) FILTER (WHERE g.id is not null),
                        '[]'
                        ) as genres
        FROM content.film_work fw
        LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
        LEFT JOIN content.person p ON p.id = pfw.person_id
        LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
        LEFT JOIN content.genre g ON g.id = gfw.genre_id
        WHERE fw.modified > %s
        GROUP BY fw.id
        ORDER BY fw.modified DESC;
"""
