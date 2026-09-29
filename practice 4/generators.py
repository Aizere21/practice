def squares_up_to(n):
    """Yield squares for integers from 0 through n."""
    for number in range(n + 1):
        yield number**2


def even_numbers(n):
    """Yield even integers from 0 through n."""
    for number in range(0, n + 1, 2):
        yield number


def divisible_by_3_and_4(n):
    """Yield numbers from 0 through n divisible by both 3 and 4."""
    for number in range(n + 1):
        if number % 3 == 0 and number % 4 == 0:
            yield number


def squares(a, b):
    """Yield squares of integers from a through b, inclusive."""
    for number in range(a, b + 1):
        yield number**2


def countdown(n):
    """Yield integers from n down to 0."""
    for number in range(n, -1, -1):
        yield number


def main():
    print("Squares up to N:", list(squares_up_to(5)))

    n = int(input("Enter n for even numbers: "))
    print(",".join(str(number) for number in even_numbers(n)))

    print("Divisible by both 3 and 4:", list(divisible_by_3_and_4(50)))

    print("Squares from a to b:")
    for value in squares(2, 6):
        print(value)

    print("Countdown:", list(countdown(5)))


if __name__ == "__main__":
    main()