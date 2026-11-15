import json
import csv

from connect import connect



def search_contact():

    pattern = input("Enter name, surname, email or phone: ")

    conn = None
    cur = None

    try:
        conn = connect()
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM search_contacts(%s)",
            (pattern,)
        )

        rows = cur.fetchall()

        if rows:
            print("\nSearch results:")

            for row in rows:
                print(row)

        else:
            print("No contacts found.")

    except Exception as e:
        print("Error:", e)

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()




def upsert_contact():

    name = input("Enter first name: ")
    last_name = input("Enter surname: ")
    phone = input("Enter phone: ")

    email = input("Enter email: ")
    birthday = input("Enter birthday (YYYY-MM-DD) or leave empty: ")
    group_name = input("Enter group or leave empty: ")

    conn = None
    cur = None

    try:
        conn = connect()
        cur = conn.cursor()

        cur.execute(
            "CALL upsert_contact(%s, %s, %s)",
            (name, last_name, phone)
        )

        cur.execute(
            """
            UPDATE contacts
            SET email = %s,
                birthday = %s
            WHERE first_name = %s
            AND COALESCE(last_name, '') = %s
            """,
            (
                email or None,
                birthday or None,
                name,
                last_name
            )
        )

        if group_name:

            cur.execute(
                """
                INSERT INTO groups(name)
                VALUES (%s)
                ON CONFLICT (name) DO NOTHING
                """,
                (group_name,)
            )

            cur.execute(
                """
                UPDATE contacts
                SET group_id = (
                    SELECT id
                    FROM groups
                    WHERE name = %s
                )
                WHERE first_name = %s
                AND COALESCE(last_name, '') = %s
                """,
                (group_name, name, last_name)
            )

        conn.commit()

        print("Contact saved successfully!")

    except Exception as e:

        if conn:
            conn.rollback()

        print("Error:", e)

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()




def add_phone():

    contact_name = input("Enter contact full name: ").strip()

    if not contact_name:
        print("Name cannot be empty.")
        return

    phone = input("Enter new phone: ").strip()
    phone_type = input("Enter type (home/work/mobile): ").lower()

    conn = None
    cur = None

    try:
        conn = connect()
        cur = conn.cursor()

        cur.execute(
            "CALL add_phone(%s, %s, %s)",
            (contact_name, phone, phone_type)
        )

        conn.commit()

        print("Phone added successfully!")

    except Exception as e:

        if conn:
            conn.rollback()

        print("Error:", e)

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def move_to_group():

    contact_name = input("Enter contact full name: ").strip()

    if not contact_name:
        print("Name cannot be empty.")
        return

    group_name = input("Enter group name: ").strip()

    conn = None
    cur = None

    try:
        conn = connect()
        cur = conn.cursor()

        cur.execute(
            "CALL move_to_group(%s, %s)",
            (contact_name, group_name)
        )

        conn.commit()

        print("Contact moved successfully!")

    except Exception as e:

        if conn:
            conn.rollback()

        print("Error:", e)

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()



def filter_by_group():

    group_name = input("Enter group name: ")

    conn = None
    cur = None

    try:
        conn = connect()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT
                c.id,
                c.first_name,
                c.last_name,
                c.email,
                g.name
            FROM contacts c
            LEFT JOIN groups g
            ON c.group_id = g.id
            WHERE g.name ILIKE %s
            ORDER BY c.first_name
            """,
            (group_name,)
        )

        rows = cur.fetchall()

        if rows:
            for row in rows:
                print(row)
        else:
            print("No contacts found.")

    except Exception as e:
        print("Error:", e)

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()




def search_by_email():

    email = input("Enter email: ")

    conn = None
    cur = None

    try:
        conn = connect()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT id, first_name, last_name, email
            FROM contacts
            WHERE email ILIKE %s
            """,
            ('%' + email + '%',)
        )

        rows = cur.fetchall()

        if rows:
            for row in rows:
                print(row)
        else:
            print("No contacts found.")

    except Exception as e:
        print("Error:", e)

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()



def sort_contacts():

    print("\nSort by:")
    print("1. Name")
    print("2. Birthday")
    print("3. Date added")

    choice = input("Choose: ")

    if choice == "1":
        order = "first_name"

    elif choice == "2":
        order = "birthday NULLS LAST"

    elif choice == "3":
        order = "created_at DESC"

    else:
        print("Invalid choice.")
        return

    conn = None
    cur = None

    try:
        conn = connect()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT
                id,
                first_name,
                last_name,
                email,
                birthday,
                created_at
            FROM contacts
            ORDER BY
            """ + order
        )

        for row in cur.fetchall():
            print(row)

    except Exception as e:
        print("Error:", e)

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()




def show_paginated():

    try:
        limit = int(input("Contacts per page: "))

        if limit <= 0:
            print("Enter a number greater than zero.")
            return

        page = 1

        while True:

            offset = (page - 1) * limit

            conn = connect()
            cur = conn.cursor()

            cur.execute(
                "SELECT * FROM get_contacts_paginated(%s, %s)",
                (limit, offset)
            )

            rows = cur.fetchall()

            cur.close()
            conn.close()

            print("\nPage:", page)

            for row in rows:
                print(row)

            if not rows:
                print("No contacts on this page.")

            command = input(
                "\nnext - next page\n"
                "prev - previous page\n"
                "quit - return to menu\n"
            ).lower()

            if command == "next":

                if rows:
                    page += 1
                else:
                    print("No next page.")

            elif command == "prev":

                if page > 1:
                    page -= 1

            elif command == "quit":
                break

            else:
                print("Invalid command.")

    except ValueError:
        print("Enter a valid number.")

    except Exception as e:
        print("Error:", e)




def export_json():

    conn = None
    cur = None

    try:
        conn = connect()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT
                c.id,
                c.first_name,
                c.last_name,
                c.email,
                c.birthday,
                g.name
            FROM contacts c
            LEFT JOIN groups g
            ON c.group_id = g.id
            ORDER BY c.id
            """
        )

        contacts = cur.fetchall()

        result = []

        for contact in contacts:

            cur.execute(
                """
                SELECT phone, type
                FROM phones
                WHERE contact_id = %s
                """,
                (contact[0],)
            )

            phones = cur.fetchall()

            result.append({
                "first_name": contact[1],
                "last_name": contact[2],
                "email": contact[3],
                "birthday": (
                    contact[4].isoformat()
                    if contact[4] else None
                ),
                "group": contact[5],
                "phones": [
                    {
                        "phone": p[0],
                        "type": p[1]
                    }
                    for p in phones
                ]
            })

        with open("contacts.json", "w", encoding="utf-8") as file:
            json.dump(result, file, ensure_ascii=False, indent=4)

        print("Export completed!")

    except Exception as e:
        print("Error:", e)

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()




def import_json():

    try:
        with open("contacts.json", "r", encoding="utf-8") as file:
            contacts = json.load(file)

        if not isinstance(contacts, list):
            print("JSON must contain a list.")
            return

    except FileNotFoundError:
        print("contacts.json not found.")
        return

    except json.JSONDecodeError:
        print("Invalid JSON.")
        return

    print("\nChoose import mode:")
    print("1. Skip existing contacts")
    print("2. Overwrite existing contacts")

    choice = input("Choose: ")

    if choice == "1":
        mode = "skip"

    elif choice == "2":
        mode = "overwrite"

    else:
        print("Invalid choice.")
        return

    conn = None
    cur = None

    try:
        conn = connect()
        cur = conn.cursor()

        cur.execute(
            "CALL bulk_insert_contacts(%s::jsonb, %s, %s::jsonb)",
            (json.dumps(contacts), mode, '[]')
        )

        invalid = cur.fetchone()

        conn.commit()

        print("JSON import completed!")
        print("Invalid contacts:", invalid[0] if invalid else [])

    except Exception as e:

        if conn:
            conn.rollback()

        print("Error:", e)

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()



def import_csv():

    conn = None
    cur = None

    try:
        with open("contacts.csv", "r", encoding="utf-8") as file:

            reader = csv.DictReader(file)

            conn = connect()
            cur = conn.cursor()

            added = 0
            skipped = 0

            for row in reader:

                name = row["first_name"].strip()
                last_name = row.get("last_name", "").strip()
                phone = row["phone"].strip()

                phone_type = row.get("phone_type", "mobile").strip().lower()

                if phone_type not in ("home", "work", "mobile"):
                    print("Invalid phone type:", phone_type)
                    skipped += 1
                    continue

                if not name or not phone:
                    print("Skipped: name or phone is empty.")
                    skipped += 1
                    continue

                cur.execute(
                    """
                    SELECT c.id, c.first_name, c.last_name
                    FROM contacts c
                    WHERE c.phone = %s

                    UNION

                    SELECT c.id, c.first_name, c.last_name
                    FROM contacts c
                    JOIN phones p ON c.id = p.contact_id
                    WHERE p.phone = %s
                    """,
                    (phone, phone)
                )

                existing = cur.fetchone()

                if existing:

                    if (
                        existing[1].lower() != name.lower()
                        or (existing[2] or "").lower() != last_name.lower()
                    ):
                        print(
                            "Skipped:", name,
                            "- this phone belongs to another contact."
                        )
                        skipped += 1
                        continue

                    contact_id = existing[0]

                    print("Already exists:", name, last_name)

                else:

                    cur.execute(
                        "CALL upsert_contact(%s, %s, %s)",
                        (name, last_name, phone)
                    )

                    cur.execute(
                        """
                        SELECT id
                        FROM contacts
                        WHERE first_name = %s
                        AND COALESCE(last_name, '') = %s
                        LIMIT 1
                        """,
                        (name, last_name)
                    )

                    contact_id = cur.fetchone()[0]

                    added += 1

                
                cur.execute(
                    """
                    INSERT INTO phones(contact_id, phone, type)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (contact_id, phone)
                    DO UPDATE SET type = EXCLUDED.type
                    """,
                    (contact_id, phone, phone_type)
                )

                
                cur.execute(
                    """
                    UPDATE contacts
                    SET email = %s,
                        birthday = %s
                    WHERE id = %s
                    """,
                    (
                        row.get("email") or None,
                        row.get("birthday") or None,
                        contact_id
                    )
                )

                
                group_name = row.get("group", "").strip()

                if group_name:

                    cur.execute(
                        """
                        INSERT INTO groups(name)
                        VALUES (%s)
                        ON CONFLICT (name) DO NOTHING
                        """,
                        (group_name,)
                    )

                    cur.execute(
                        "SELECT id FROM groups WHERE name = %s",
                        (group_name,)
                    )

                    group_id = cur.fetchone()[0]

                    cur.execute(
                        """
                        UPDATE contacts
                        SET group_id = %s
                        WHERE id = %s
                        """,
                        (group_id, contact_id)
                    )

            conn.commit()

            print("\nCSV import completed!")
            print("New contacts:", added)
            print("Skipped contacts:", skipped)

    except Exception as e:

        if conn:
            conn.rollback()

        print("Error:", e)

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()



def delete_contact():

    value = input("Enter contact ID or phone: ")
    delete_type = input("Enter type (id/phone): ").lower()

    conn = None
    cur = None

    try:
        conn = connect()
        cur = conn.cursor()

        cur.execute(
            "CALL delete_contact(%s, %s)",
            (value, delete_type)
        )

        conn.commit()

        print("Delete completed!")

    except Exception as e:

        if conn:
            conn.rollback()

        print("Error:", e)

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()




def bulk_insert():

    conn = None
    cur = None

    try:
        filename = input("Enter JSON filename: ").strip()

        if not filename:
            print("Filename cannot be empty.")
            return

        with open(filename, "r", encoding="utf-8") as file:
            contacts = json.load(file)

        if not isinstance(contacts, list):
            print("JSON must contain a list.")
            return

        conn = connect()
        cur = conn.cursor()

        cur.execute(
            "CALL bulk_insert_contacts(%s::jsonb, %s::jsonb)",
            (json.dumps(contacts), '[]')
        )

        invalid = cur.fetchone()

        conn.commit()

        print("Bulk insert completed!")
        print("Invalid contacts:", invalid[0] if invalid else [])

    except Exception as e:

        if conn:
            conn.rollback()

        print("Error:", e)

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()




def menu():

    while True:

        print("\n========== PHONEBOOK TSIS 1 ==========")

        print("1. Search contact")
        print("2. Add or update contact")
        print("3. Add another phone")
        print("4. Move contact to group")
        print("5. Filter by group")
        print("6. Search by email")
        print("7. Sort contacts")
        print("8. Show contacts by pages")
        print("9. Export JSON")
        print("10. Import JSON")
        print("11. Import CSV")
        print("12. Delete contact")
        print("13. Bulk insert")
        print("0. Exit")

        choice = input("\nChoose an option: ")

        if choice == "1":
            search_contact()

        elif choice == "2":
            upsert_contact()

        elif choice == "3":
            add_phone()

        elif choice == "4":
            move_to_group()

        elif choice == "5":
            filter_by_group()

        elif choice == "6":
            search_by_email()

        elif choice == "7":
            sort_contacts()

        elif choice == "8":
            show_paginated()

        elif choice == "9":
            export_json()

        elif choice == "10":
            import_json()

        elif choice == "11":
            import_csv()

        elif choice == "12":
            delete_contact()

        elif choice == "13":
            bulk_insert()

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid choice!")


if __name__ == "__main__":
    menu()