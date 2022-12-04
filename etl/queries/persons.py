PERSON_QUERY = """
SELECT
    p.id,
    p.full_name,
    p.modified,
   COALESCE (
       json_agg(
           DISTINCT jsonb_build_object(
               'fw_id', fw.id,
               'fw_title', fw.title,
               'fw_rating', fw.rating,
               'fw_type', fw.type
           )
       ) FILTER (WHERE fw.id is not null),
       '[]'
   ) as films,
   array_agg(DISTINCT pfw.role) as roles
FROM content.person p
LEFT JOIN content.person_film_work pfw ON pfw.person_id = p.id
LEFT JOIN content.film_work fw ON fw.id = pfw.film_work_id
WHERE p.modified > %s
GROUP BY p.id
ORDER BY p.modified"""
