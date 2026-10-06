import json
import re
import html
from decimal import Decimal
from pathlib import Path


def to_money(number_text):
   
    number_text = number_text.replace(" ", "")  
    number_text = number_text.replace(",", ".")  
    return Decimal(number_text)


def parse_receipt(receipt_text):
    
    receipt_text = html.unescape(receipt_text)
    receipt_text = re.sub(r"(?<=\d)\\(?=\.)", "", receipt_text)
    products = []

   
    item_pattern = re.compile(
        r"(?ms)^\s*(\d+)\\?\.\s*\n([^\n]+)\n"
        r"\s*(\d+[,.]\d+)\s*x\s*([\d ]+[,.]\d{2})\s*\n"
        r"\s*[\d ]+[,.]\d{2}\s*\nСтоимость\s*\n\s*([\d ]+[,.]\d{2})"
    )

    for match in re.finditer(item_pattern, receipt_text):
        number, name, quantity, unit_price, item_price = match.groups()
        product = {
            "number": int(number),
            "name": name.strip(),
            "quantity": quantity.replace(",", "."),
            "unit_price": str(to_money(unit_price)),
            "price": str(to_money(item_price)),
        }
        products.append(product)

    
    date_time = re.search(
        r"Время:\s*(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2}:\d{2})",
        receipt_text,
    )

    
    total_match = re.search(r"ИТОГО:\s*([\d ]+[,.]\d{2})", receipt_text)

    
    payment_match = re.search(r"Банковская карта|Наличными", receipt_text, re.IGNORECASE)

    
    products_total = sum(
        (Decimal(product["price"]) for product in products),
        Decimal("0.00"),
    )

    return {
        "prices": [product["price"] for product in products],
        "products": products,
        "calculated_products_total": str(products_total),
        "total": str(to_money(total_match.group(1))) if total_match else None,
        "date": date_time.group(1) if date_time else None,
        "time": date_time.group(2) if date_time else None,
        "payment_method": payment_match.group(0) if payment_match else None,
    }



receipt_file = Path(__file__).with_name("raw.txt")

if not receipt_file.exists():
    print("Не найден raw.txt. Положите файл рядом с receipt_parser.py.")
else:
    receipt_text = receipt_file.read_text(encoding="utf-8")
    result = parse_receipt(receipt_text)
    print(json.dumps(result, ensure_ascii=False, indent=2))