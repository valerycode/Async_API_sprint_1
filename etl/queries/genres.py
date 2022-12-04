GENRE_QUERY = '''
    SELECT
        g.id,
        g.name,
        g.description,
        g.modified 
    FROM content.genre g
    WHERE g.modified > %s;
'''