

CREATE OR REPLACE FUNCTION search_contacts(
    p_query TEXT
)

RETURNS TABLE(
    id INTEGER,
    first_name VARCHAR,
    last_name VARCHAR,
    email VARCHAR,
    birthday DATE,
    group_name VARCHAR,
    phones TEXT
)

LANGUAGE plpgsql
AS $$
BEGIN

    RETURN QUERY

    SELECT
        c.id,
        c.first_name,
        c.last_name,
        c.email,
        c.birthday,
        g.name::VARCHAR,

        COALESCE(
            STRING_AGG(
                p.phone || ' (' || p.type || ')',
                ', '
            ),
            ''
        )::TEXT

    FROM contacts c

    LEFT JOIN groups g
        ON c.group_id = g.id

    LEFT JOIN phones p
        ON c.id = p.contact_id

    WHERE
        c.first_name ILIKE '%' || p_query || '%'
        OR c.last_name ILIKE '%' || p_query || '%'
        OR c.email ILIKE '%' || p_query || '%'
        OR p.phone ILIKE '%' || p_query || '%'

    GROUP BY
        c.id,
        c.first_name,
        c.last_name,
        c.email,
        c.birthday,
        g.name

    ORDER BY c.id;

END;
$$;




CREATE OR REPLACE FUNCTION get_contacts_paginated(
    p_limit INTEGER,
    p_offset INTEGER
)

RETURNS TABLE(
    id INTEGER,
    first_name VARCHAR,
    last_name VARCHAR,
    email VARCHAR,
    birthday DATE,
    group_name VARCHAR,
    phones TEXT
)

LANGUAGE plpgsql
AS $$
BEGIN

    IF p_limit <= 0 OR p_offset < 0 THEN
        RAISE EXCEPTION 'Invalid pagination parameters';
    END IF;

    RETURN QUERY

    SELECT
        c.id,
        c.first_name,
        c.last_name,
        c.email,
        c.birthday,
        g.name::VARCHAR,

        COALESCE(
            STRING_AGG(
                p.phone || ' (' || p.type || ')',
                ', '
            ),
            ''
        )::TEXT

    FROM contacts c

    LEFT JOIN groups g
        ON c.group_id = g.id

    LEFT JOIN phones p
        ON c.id = p.contact_id

    GROUP BY
        c.id,
        c.first_name,
        c.last_name,
        c.email,
        c.birthday,
        g.name

    ORDER BY c.id

    LIMIT p_limit
    OFFSET p_offset;

END;
$$;