CREATE TABLE IF NOT EXISTS contacts (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100),
    phone VARCHAR(20)
);


CREATE TABLE IF NOT EXISTS groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);


ALTER TABLE contacts
ADD COLUMN IF NOT EXISTS email VARCHAR(100);

ALTER TABLE contacts
ADD COLUMN IF NOT EXISTS birthday DATE;

ALTER TABLE contacts
ADD COLUMN IF NOT EXISTS group_id INTEGER
REFERENCES groups(id);

ALTER TABLE contacts
ADD COLUMN IF NOT EXISTS created_at TIMESTAMP
DEFAULT CURRENT_TIMESTAMP;


INSERT INTO groups(name)
VALUES
    ('Family'),
    ('Work'),
    ('Friend'),
    ('Other')
ON CONFLICT (name) DO NOTHING;


CREATE TABLE IF NOT EXISTS phones (
    id SERIAL PRIMARY KEY,

    contact_id INTEGER
    REFERENCES contacts(id)
    ON DELETE CASCADE,

    phone VARCHAR(20) NOT NULL,

    type VARCHAR(10)
    CHECK (type IN ('home', 'work', 'mobile')),

    UNIQUE(contact_id, phone)
);


INSERT INTO phones(contact_id, phone, type)
SELECT id, phone, 'mobile'
FROM contacts
WHERE phone IS NOT NULL
AND TRIM(phone) <> ''
ON CONFLICT (contact_id, phone) DO NOTHING;