

from functools import reduce

numbers = [1, 2, 3, 4, 5, 6]

print("Numbers:", numbers)
print("Length:", len(numbers))
print("Sum:", sum(numbers))
print("Minimum:", min(numbers))
print("Maximum:", max(numbers))
print("Sorted:", sorted(numbers))
print("Sorted descending:", sorted(numbers, reverse=True))


doubled = list(map(lambda number: number * 2, numbers))
print("Doubled:", doubled)


even_numbers = list(filter(lambda number: number % 2 == 0, numbers))
print("Even numbers:", even_numbers)


total = reduce(lambda first, second: first + second, numbers)
print("Reduce sum:", total)


text_number = "25"
integer_number = int(text_number)
decimal_number = float("3.14")
number_text = str(100)

print(type(text_number))
print(type(integer_number))
print(type(decimal_number))
print(type(number_text))
print("Integer:", integer_number)
print("Float:", decimal_number)
print("String:", number_text)
print("Boolean examples:", bool(1), bool(0))
print("List from string:", list("Python"))