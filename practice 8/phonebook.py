import json
from connect import connect


def search_contact():
    pattern = input("Enter name, surname or phone: ")

    conn = None
    cur = None

    try:
        conn = connect()
        cur = conn.cursor()

        cur.execute("SELECT * FROM search_contacts(%s)", (pattern,))
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
    name = input("Enter name: ")
    last_name = input("Enter surname: ")
    phone = input("Enter phone: ")

    conn = None
    cur = None

    try:
        conn = connect()
        cur = conn.cursor()

        cur.execute(
            "CALL upsert_contact(%s, %s, %s)",
            (name, last_name, phone)
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


def bulk_insert():
    contacts = []

    try:
        count = int(input("How many contacts do you want to add? "))

        if count <= 0:
            print("Enter a number greater than 0.")
            return

        for i in range(count):
            print("\nContact", i + 1)

            name = input("Enter name: ")
            last_name = input("Enter surname: ")
            phone = input("Enter phone: ")

            contacts.append({
                "name": name,
                "last_name": last_name,
                "phone": phone
            })

        conn = None
        cur = None

        try:
            conn = connect()
            cur = conn.cursor()

            cur.execute(
                "CALL bulk_insert_contacts(%s::jsonb, NULL::jsonb)",
                (json.dumps(contacts),)
            )

            result = cur.fetchone()
            conn.commit()

            if result and result[0]:
                print("\nIncorrect contacts:")
                print(result[0])
            else:
                print("\nAll contacts were added successfully!")

        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    except ValueError:
        print("Please enter a valid number.")

    except Exception as e:
        print("Error:", e)


def show_paginated():
    conn = None
    cur = None

    try:
        limit = int(input("How many contacts per page? "))
        page = int(input("Enter page number: "))

        if limit <= 0 or page <= 0:
            print("Limit and page must be greater than 0.")
            return

        offset = (page - 1) * limit

        conn = connect()
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM get_contacts_paginated(%s, %s)",
            (limit, offset)
        )

        rows = cur.fetchall()

        if rows:
            print("\nContacts - Page", page)

            for row in rows:
                print(row)
        else:
            print("No contacts on this page.")

    except ValueError:
        print("Please enter valid numbers.")

    except Exception as e:
        print("Error:", e)

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def delete_contact():
    value = input("Enter name or phone: ")
    delete_type = input("Enter type (name/phone): ").lower()

    if delete_type not in ("name", "phone"):
        print("Invalid type! Choose name or phone.")
        return

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
        print("Delete operation completed!")

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
        print("\n========== PHONEBOOK ==========")
        print("1. Search contact")
        print("2. Add or update contact")
        print("3. Bulk insert contacts")
        print("4. Show contacts by pages")
        print("5. Delete contact")
        print("0. Exit")

        choice = input("\nChoose an option: ")

        if choice == "1":
            search_contact()

        elif choice == "2":
            upsert_contact()

        elif choice == "3":
            bulk_insert()

        elif choice == "4":
            show_paginated()

        elif choice == "5":
            delete_contact()

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid choice! Try again.")


if __name__ == "__main__":
    menu()