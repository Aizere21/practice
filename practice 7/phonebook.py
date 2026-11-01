import csv
from connect import connect


# 1. Add contact
def add_contact():
    name = input("Enter name: ")
    phone = input("Enter phone: ")

    conn = None
    cur = None

    try:
        conn = connect()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO contacts (first_name, phone) VALUES (%s, %s)",
            (name, phone)
        )

        conn.commit()

        print("Contact added successfully!")

    except Exception as error:
        if conn:
            conn.rollback()

        print("Error:", error)

    finally:
        if cur:
            cur.close()

        if conn:
            conn.close() 

# 2. Show all contacts
def show_contacts():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM contacts")
    contacts = cur.fetchall()

    if len(contacts) == 0:
        print("PhoneBook is empty!")
    else:
        for contact in contacts:
            print(contact)

    cur.close()
    conn.close()


# 3. Update name
def update_name():
    phone = input("Enter current phone: ")
    new_name = input("Enter new name: ")

    conn = None
    cur = None

    try:
        conn = connect()
        cur = conn.cursor()

        cur.execute(
            "UPDATE contacts SET first_name = %s WHERE phone = %s",
            (new_name, phone)
        )

        conn.commit()

        print("Updated contacts:", cur.rowcount)

    except Exception as error:
        if conn:
            conn.rollback()

        print("Error:", error)

    finally:
        if cur:
            cur.close()

        if conn:
            conn.close()  


# 4. Update phone
def update_phone():
    name = input("Enter name: ")
    new_phone = input("Enter new phone: ")

    conn = None
    cur = None

    try:
        conn = connect()
        cur = conn.cursor()

        cur.execute(
            "UPDATE contacts SET phone = %s WHERE first_name = %s",
            (new_phone, name)
        )

        conn.commit()

        print("Updated contacts:", cur.rowcount)

    except Exception as error:
        if conn:
            conn.rollback()

        print("Error:", error)

    finally:
        if cur:
            cur.close()

        if conn:
            conn.close() 


# 5. Search by name
def search_by_name():
    name = input("Enter name to search: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM contacts WHERE first_name ILIKE %s",
        (name + "%",)
    )

    contacts = cur.fetchall()

    if len(contacts) == 0:
        print("Contact not found!")
    else:
        for contact in contacts:
            print(contact)

    cur.close()
    conn.close()


# 6. Search by phone prefix
def search_by_phone():
    prefix = input("Enter phone prefix: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM contacts WHERE phone LIKE %s",
        (prefix + "%",)
    )

    contacts = cur.fetchall()

    if len(contacts) == 0:
        print("Contact not found!")
    else:
        for contact in contacts:
            print(contact)

    cur.close()
    conn.close()


# 7. Delete by name
def delete_by_name():
    name = input("Enter name: ")

    conn = None
    cur = None

    try:
        conn = connect()
        cur = conn.cursor()

        cur.execute(
            "DELETE FROM contacts WHERE first_name = %s",
            (name,)
        )

        conn.commit()

        print("Deleted contacts:", cur.rowcount)

    except Exception as error:
        if conn:
            conn.rollback()

        print("Error:", error)

    finally:
        if cur:
            cur.close()

        if conn:
            conn.close() 

# 8. Delete by phone
def delete_by_phone():
    phone = input("Enter phone: ")

    conn = None
    cur = None

    try:
        conn = connect()
        cur = conn.cursor()

        cur.execute(
            "DELETE FROM contacts WHERE phone = %s",
            (phone,)
        )

        conn.commit()

        print("Deleted contacts:", cur.rowcount)

    except Exception as error:
        if conn:
            conn.rollback()

        print("Error:", error)

    finally:
        if cur:
            cur.close()

        if conn:
            conn.close() 

# 9. Import from CSV
def import_from_csv():
    conn = None
    cur = None

    try:
        conn = connect()
        cur = conn.cursor()

        with open("contacts.csv", "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                cur.execute(
                    """
                    INSERT INTO contacts (first_name, phone)
                    VALUES (%s, %s)
                    ON CONFLICT (phone) DO NOTHING
                    """,
                    (row["first_name"].strip(), row["phone"].strip())
                )

        conn.commit()

        print("Contacts imported successfully!")

    except Exception as error:
        if conn:
            conn.rollback()

        print("Error:", error)

    finally:
        if cur:
            cur.close()

        if conn:
            conn.close() 
# 10. Main menu
def menu():
    while True:
        print("\n========== PHONEBOOK ==========")
        print("1. Add contact")
        print("2. Show contacts")
        print("3. Update name")
        print("4. Update phone")
        print("5. Search by name")
        print("6. Search by phone")
        print("7. Delete by name")
        print("8. Delete by phone")
        print("9. Import from CSV")
        print("0. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_contact()

        elif choice == "2":
            show_contacts()

        elif choice == "3":
            update_name()

        elif choice == "4":
            update_phone()

        elif choice == "5":
            search_by_name()

        elif choice == "6":
            search_by_phone()

        elif choice == "7":
            delete_by_name()

        elif choice == "8":
            delete_by_phone()

        elif choice == "9":
            import_from_csv()

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid option! Try again.")


# Start program
menu() 