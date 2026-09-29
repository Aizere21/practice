"""Practice JSON strings, conversion, file I/O, and sample-data parsing."""

from pathlib import Path
import sys



script_folder = str(Path(__file__).resolve().parent)
sys.path = [
    entry
    for entry in sys.path
    if str(Path(entry or ".").resolve()) != script_folder
]

import json


def demonstrate_json_string():
    """Показать разбор JSON-строки и создание JSON-строки."""

    
    json_text = '{"name": "Ethernet", "enabled": true, "speed": null}'

   
    python_data = json.loads(json_text)
    print("Parsed Python data:", python_data)

    
    converted_text = json.dumps(python_data, indent=4)
    print("Converted back to JSON text:")
    print(converted_text)


def write_json_file(filename="created-data.json"):
    """Записать Python-словарь в файл с помощью json.dump()."""

    python_data = {
        "course": "Python",
        "topic": "JSON",
        "completed": True,
        "topics": ["loads", "dumps", "load", "dump"],
    }

    output_path = Path(__file__).resolve().parent / filename

    
    with output_path.open("w", encoding="utf-8") as file:
        json.dump(python_data, file, indent=4)

    return output_path


def read_interfaces(filename="sample-data.json"):
    """Прочитать интерфейсы из sample-data.json с помощью json.load()."""

    data_path = Path(__file__).resolve().parent / filename

    
    with data_path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    interfaces = []

    
    for item in data.get("imdata", []):
        attributes = item.get("l1PhysIf", {}).get("attributes", {})
        interfaces.append(attributes)

    return interfaces


def print_interface_table(interfaces):
    """Напечатать поля DN, Description, Speed и MTU в виде таблицы."""

    columns = ("DN", "Description", "Speed", "MTU")

    rows = [
        (
            interface.get("dn", ""),
            interface.get("descr") or "",
            interface.get("speed", ""),
            interface.get("mtu", ""),
        )
        for interface in interfaces
    ]

    
    widths = [
        max(len(columns[i]), *(len(str(row[i])) for row in rows))
        for i in range(len(columns))
    ]

    print("Interface Status")
    print()
    print(
        f"{columns[0]:<{widths[0]}}  "
        f"{columns[1]:<{widths[1]}}  "
        f"{columns[2]:<{widths[2]}}  "
        f"{columns[3]}"
    )
    print(
        f"{'-' * widths[0]}  "
        f"{'-' * widths[1]}  "
        f"{'-' * widths[2]}  "
        f"{'-' * widths[3]}"
    )

    for row in rows:
        print(
            f"{row[0]:<{widths[0]}}  "
            f"{row[1]:<{widths[1]}}  "
            f"{row[2]:<{widths[2]}}  "
            f"{row[3]}"
        )


if __name__ == "__main__":
    demonstrate_json_string()
    print()

    created_file = write_json_file()
    print("JSON file written:", created_file.name)
    print()

    interfaces = read_interfaces()
    print_interface_table(interfaces)