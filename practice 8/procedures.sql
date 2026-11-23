CREATE OR REPLACE PROCEDURE upsert_contact(
    p_name VARCHAR,
    p_last_name VARCHAR,
    p_phone VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN

    IF EXISTS (
        SELECT 1
        FROM contacts
        WHERE first_name = p_name
        AND last_name = p_last_name
    ) THEN

        UPDATE contacts
        SET phone = p_phone
        WHERE first_name = p_name
        AND last_name = p_last_name;

    ELSE

        INSERT INTO contacts(first_name, last_name, phone)
        VALUES (p_name, p_last_name, p_phone);

    END IF;

END;
$$;


CREATE OR REPLACE PROCEDURE bulk_insert_contacts(
    IN p_contacts JSONB,
    INOUT p_invalid JSONB DEFAULT '[]'::JSONB
)
LANGUAGE plpgsql
AS $$
DECLARE
    item JSONB;
    v_name VARCHAR;
    v_last_name VARCHAR;
    v_phone VARCHAR;

BEGIN

    p_invalid := '[]'::JSONB;

    FOR item IN
        SELECT value
        FROM jsonb_array_elements(p_contacts)
    LOOP

        v_name := item->>'name';
        v_last_name := item->>'last_name';
        v_phone := item->>'phone';

        IF v_name IS NULL
           OR TRIM(v_name) = ''
           OR v_last_name IS NULL
           OR TRIM(v_last_name) = ''
           OR v_phone IS NULL
           OR v_phone !~ '^\+?[0-9]{10,15}$'
        THEN

            p_invalid := p_invalid || jsonb_build_array(item);

        ELSE

            IF EXISTS (
                SELECT 1
                FROM contacts
                WHERE first_name = v_name
                AND last_name = v_last_name
            ) THEN

                UPDATE contacts
                SET phone = v_phone
                WHERE first_name = v_name
                AND last_name = v_last_name;

            ELSIF EXISTS (
                SELECT 1
                FROM contacts
                WHERE phone = v_phone
            ) THEN

                p_invalid := p_invalid || jsonb_build_array(item);

            ELSE

                INSERT INTO contacts(first_name, last_name, phone)
                VALUES (v_name, v_last_name, v_phone);

            END IF;

        END IF;

    END LOOP;

END;
$$;


CREATE OR REPLACE PROCEDURE delete_contact(
    p_value VARCHAR,
    p_type VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN

    IF p_type = 'name' THEN

        DELETE FROM contacts
        WHERE first_name = p_value;

    ELSIF p_type = 'phone' THEN

        DELETE FROM contacts
        WHERE phone = p_value;

    ELSE

        RAISE EXCEPTION 'Invalid delete type';

    END IF;

END;
$$;  