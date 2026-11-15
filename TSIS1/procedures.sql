DROP PROCEDURE IF EXISTS add_phone(INTEGER, VARCHAR, VARCHAR);
DROP PROCEDURE IF EXISTS add_phone(VARCHAR, VARCHAR, VARCHAR);

CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone VARCHAR,
    p_type VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contact_id INTEGER;
    v_count INTEGER;
BEGIN
    IF p_contact_name IS NULL OR TRIM(p_contact_name) = '' THEN
        RAISE EXCEPTION 'Contact name cannot be empty';
    END IF;

    IF p_phone IS NULL OR TRIM(p_phone) = '' THEN
        RAISE EXCEPTION 'Phone cannot be empty';
    END IF;

    IF LOWER(p_type) NOT IN ('home', 'work', 'mobile') THEN
        RAISE EXCEPTION 'Invalid phone type';
    END IF;

    SELECT COUNT(*)
    INTO v_count
    FROM contacts c
    WHERE LOWER(TRIM(CONCAT_WS(' ', c.first_name, c.last_name)))
          = LOWER(TRIM(p_contact_name))
       OR LOWER(TRIM(c.first_name)) = LOWER(TRIM(p_contact_name));

    IF v_count = 0 THEN
        RAISE EXCEPTION 'Contact not found';
    END IF;

    IF v_count > 1 THEN
        RAISE EXCEPTION 'More than one contact found. Enter full name';
    END IF;

    SELECT c.id
    INTO v_contact_id
    FROM contacts c
    WHERE LOWER(TRIM(CONCAT_WS(' ', c.first_name, c.last_name)))
          = LOWER(TRIM(p_contact_name))
       OR LOWER(TRIM(c.first_name)) = LOWER(TRIM(p_contact_name))
    LIMIT 1;

    INSERT INTO phones(contact_id, phone, type)
    VALUES (v_contact_id, TRIM(p_phone), LOWER(p_type))
    ON CONFLICT (contact_id, phone)
    DO UPDATE SET type = EXCLUDED.type;
END;
$$;



DROP PROCEDURE IF EXISTS move_to_group(INTEGER, VARCHAR);
DROP PROCEDURE IF EXISTS move_to_group(VARCHAR, VARCHAR);

CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contact_id INTEGER;
    v_group_id INTEGER;
    v_count INTEGER;
BEGIN
    IF p_contact_name IS NULL OR TRIM(p_contact_name) = '' THEN
        RAISE EXCEPTION 'Contact name cannot be empty';
    END IF;

    IF p_group_name IS NULL OR TRIM(p_group_name) = '' THEN
        RAISE EXCEPTION 'Group name cannot be empty';
    END IF;

    SELECT COUNT(*)
    INTO v_count
    FROM contacts c
    WHERE LOWER(TRIM(CONCAT_WS(' ', c.first_name, c.last_name)))
          = LOWER(TRIM(p_contact_name))
       OR LOWER(TRIM(c.first_name)) = LOWER(TRIM(p_contact_name));

    IF v_count = 0 THEN
        RAISE EXCEPTION 'Contact not found';
    END IF;

    IF v_count > 1 THEN
        RAISE EXCEPTION 'More than one contact found. Enter full name';
    END IF;

    SELECT c.id
    INTO v_contact_id
    FROM contacts c
    WHERE LOWER(TRIM(CONCAT_WS(' ', c.first_name, c.last_name)))
          = LOWER(TRIM(p_contact_name))
       OR LOWER(TRIM(c.first_name)) = LOWER(TRIM(p_contact_name))
    LIMIT 1;

    INSERT INTO groups(name)
    VALUES (TRIM(p_group_name))
    ON CONFLICT (name) DO NOTHING;

    SELECT id
    INTO v_group_id
    FROM groups
    WHERE LOWER(name) = LOWER(TRIM(p_group_name))
    LIMIT 1;

    UPDATE contacts
    SET group_id = v_group_id
    WHERE id = v_contact_id;
END;
$$;



DROP FUNCTION IF EXISTS search_contacts(TEXT);

CREATE FUNCTION search_contacts(
    p_pattern TEXT
)
RETURNS TABLE (
    id INTEGER,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    phone TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT
        c.id,
        c.first_name::TEXT,
        c.last_name::TEXT,
        c.email::TEXT,
        COALESCE(p.phone, c.phone)::TEXT
    FROM contacts c
    LEFT JOIN phones p ON p.contact_id = c.id
    WHERE
        c.first_name ILIKE '%' || p_pattern || '%'
        OR COALESCE(c.last_name, '') ILIKE '%' || p_pattern || '%'
        OR COALESCE(c.email, '') ILIKE '%' || p_pattern || '%'
        OR COALESCE(c.phone, '') ILIKE '%' || p_pattern || '%'
        OR COALESCE(p.phone, '') ILIKE '%' || p_pattern || '%'
    ORDER BY c.id;
END;
$$;


DROP FUNCTION IF EXISTS get_contacts_paginated(INTEGER, INTEGER);

CREATE FUNCTION get_contacts_paginated(
    p_limit INTEGER,
    p_offset INTEGER
)
RETURNS TABLE (
    id INTEGER,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    phone TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.id,
        c.first_name::TEXT,
        c.last_name::TEXT,
        c.email::TEXT,
        c.phone::TEXT
    FROM contacts c
    ORDER BY c.id
    LIMIT p_limit
    OFFSET p_offset;
END;
$$;



CREATE OR REPLACE PROCEDURE upsert_contact(
    p_name VARCHAR,
    p_last_name VARCHAR,
    p_phone VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contact_id INTEGER;
BEGIN
    IF p_name IS NULL OR TRIM(p_name) = '' THEN
        RAISE EXCEPTION 'First name cannot be empty';
    END IF;

    IF p_phone IS NULL OR TRIM(p_phone) = '' THEN
        RAISE EXCEPTION 'Phone cannot be empty';
    END IF;

    SELECT id
    INTO v_contact_id
    FROM contacts
    WHERE LOWER(TRIM(first_name)) = LOWER(TRIM(p_name))
      AND LOWER(TRIM(COALESCE(last_name, ''))) =
          LOWER(TRIM(COALESCE(p_last_name, '')))
    LIMIT 1;

    IF v_contact_id IS NULL THEN

        INSERT INTO contacts(first_name, last_name, phone)
        VALUES (TRIM(p_name), NULLIF(TRIM(p_last_name), ''), TRIM(p_phone))
        RETURNING id INTO v_contact_id;

    ELSE

        UPDATE contacts
        SET phone = TRIM(p_phone)
        WHERE id = v_contact_id;

    END IF;

    INSERT INTO phones(contact_id, phone, type)
    VALUES (v_contact_id, TRIM(p_phone), 'mobile')
    ON CONFLICT (contact_id, phone)
    DO NOTHING;
END;
$$;




DROP PROCEDURE IF EXISTS bulk_insert_contacts(JSONB, JSONB);
DROP PROCEDURE IF EXISTS bulk_insert_contacts(JSONB, VARCHAR, JSONB);

CREATE OR REPLACE PROCEDURE bulk_insert_contacts(
    IN p_contacts JSONB,
    IN p_mode VARCHAR DEFAULT 'overwrite',
    INOUT p_invalid JSONB DEFAULT '[]'::JSONB
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contact JSONB;
    v_phone JSONB;

    v_contact_id INTEGER;
    v_group_id INTEGER;

    v_first_name VARCHAR;
    v_last_name VARCHAR;
    v_email VARCHAR;
    v_birthday DATE;
    v_group_name VARCHAR;

    v_phone_number VARCHAR;
    v_phone_type VARCHAR;

    v_existing BOOLEAN;
    v_first_phone VARCHAR;
BEGIN
    IF jsonb_typeof(p_contacts) <> 'array' THEN
        RAISE EXCEPTION 'Input must be a JSON array';
    END IF;

    IF LOWER(p_mode) NOT IN ('skip', 'overwrite') THEN
        RAISE EXCEPTION 'Mode must be skip or overwrite';
    END IF;

    IF p_invalid IS NULL THEN
        p_invalid := '[]'::JSONB;
    END IF;

    FOR v_contact IN
        SELECT value
        FROM jsonb_array_elements(p_contacts)
    LOOP

        BEGIN
            v_first_name := COALESCE(
                v_contact->>'first_name',
                v_contact->>'name'
            );

            v_last_name := v_contact->>'last_name';
            v_email := v_contact->>'email';
            v_group_name := v_contact->>'group';

            IF v_first_name IS NULL OR TRIM(v_first_name) = '' THEN
                RAISE EXCEPTION 'First name is missing';
            END IF;

            IF v_contact->>'birthday' IS NOT NULL
               AND TRIM(v_contact->>'birthday') <> '' THEN
                v_birthday := (v_contact->>'birthday')::DATE;
            ELSE
                v_birthday := NULL;
            END IF;

            SELECT id
            INTO v_contact_id
            FROM contacts
            WHERE LOWER(TRIM(first_name)) = LOWER(TRIM(v_first_name))
              AND LOWER(TRIM(COALESCE(last_name, ''))) =
                  LOWER(TRIM(COALESCE(v_last_name, '')))
            LIMIT 1;

            v_existing := v_contact_id IS NOT NULL;

            IF v_existing AND LOWER(p_mode) = 'skip' THEN
                CONTINUE;
            END IF;

            IF NOT v_existing THEN

                INSERT INTO contacts(
                    first_name,
                    last_name,
                    email,
                    birthday
                )
                VALUES (
                    TRIM(v_first_name),
                    NULLIF(TRIM(v_last_name), ''),
                    v_email,
                    v_birthday
                )
                RETURNING id INTO v_contact_id;

            ELSE

                UPDATE contacts
                SET
                    email = v_email,
                    birthday = v_birthday
                WHERE id = v_contact_id;

                DELETE FROM phones
                WHERE contact_id = v_contact_id;

            END IF;

            v_first_phone := NULL;

            IF jsonb_typeof(v_contact->'phones') = 'array' THEN

                FOR v_phone IN
                    SELECT value
                    FROM jsonb_array_elements(v_contact->'phones')
                LOOP
                    v_phone_number := v_phone->>'phone';
                    v_phone_type := LOWER(
                        COALESCE(v_phone->>'type', 'mobile')
                    );

                    IF v_phone_number IS NULL
                       OR TRIM(v_phone_number) = '' THEN
                        CONTINUE;
                    END IF;

                    IF v_phone_type NOT IN ('home', 'work', 'mobile') THEN
                        RAISE EXCEPTION 'Invalid phone type: %', v_phone_type;
                    END IF;

                    IF v_first_phone IS NULL THEN
                        v_first_phone := TRIM(v_phone_number);
                    END IF;

                    INSERT INTO phones(contact_id, phone, type)
                    VALUES (
                        v_contact_id,
                        TRIM(v_phone_number),
                        v_phone_type
                    )
                    ON CONFLICT (contact_id, phone)
                    DO UPDATE SET type = EXCLUDED.type;
                END LOOP;

            ELSIF v_contact->>'phone' IS NOT NULL
                  AND TRIM(v_contact->>'phone') <> '' THEN

                v_first_phone := TRIM(v_contact->>'phone');

                v_phone_type := LOWER(
                    COALESCE(v_contact->>'phone_type', 'mobile')
                );

                IF v_phone_type NOT IN ('home', 'work', 'mobile') THEN
                    RAISE EXCEPTION 'Invalid phone type: %', v_phone_type;
                END IF;

                INSERT INTO phones(contact_id, phone, type)
                VALUES (
                    v_contact_id,
                    v_first_phone,
                    v_phone_type
                )
                ON CONFLICT (contact_id, phone)
                DO UPDATE SET type = EXCLUDED.type;

            END IF;

            IF v_first_phone IS NOT NULL THEN
                UPDATE contacts
                SET phone = v_first_phone
                WHERE id = v_contact_id;
            END IF;

            IF v_group_name IS NOT NULL
               AND TRIM(v_group_name) <> '' THEN

                INSERT INTO groups(name)
                VALUES (TRIM(v_group_name))
                ON CONFLICT (name) DO NOTHING;

                SELECT id
                INTO v_group_id
                FROM groups
                WHERE LOWER(name) = LOWER(TRIM(v_group_name))
                LIMIT 1;

                UPDATE contacts
                SET group_id = v_group_id
                WHERE id = v_contact_id;

            END IF;

        EXCEPTION WHEN OTHERS THEN
            p_invalid := p_invalid ||
                jsonb_build_array(
                    jsonb_build_object(
                        'contact', v_contact,
                        'error', SQLERRM
                    )
                );
        END;

    END LOOP;
END;
$$;




CREATE OR REPLACE PROCEDURE delete_contact(
    p_value VARCHAR,
    p_type VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contact_id INTEGER;
BEGIN
    IF LOWER(p_type) = 'id' THEN

        v_contact_id := p_value::INTEGER;

    ELSIF LOWER(p_type) = 'phone' THEN

        SELECT id
        INTO v_contact_id
        FROM contacts
        WHERE phone = p_value
        LIMIT 1;

        IF v_contact_id IS NULL THEN
            SELECT contact_id
            INTO v_contact_id
            FROM phones
            WHERE phone = p_value
            LIMIT 1;
        END IF;

    ELSIF LOWER(p_type) = 'name' THEN

        SELECT id
        INTO v_contact_id
        FROM contacts
        WHERE LOWER(TRIM(first_name)) = LOWER(TRIM(p_value))
           OR LOWER(TRIM(CONCAT_WS(' ', first_name, last_name))) =
              LOWER(TRIM(p_value))
        LIMIT 1;

    ELSE
        RAISE EXCEPTION 'Type must be id, phone or name';
    END IF;

    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact not found';
    END IF;

    DELETE FROM phones
    WHERE contact_id = v_contact_id;

    DELETE FROM contacts
    WHERE id = v_contact_id;
END;
$$;