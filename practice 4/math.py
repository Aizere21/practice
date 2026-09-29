import math


def degrees_to_radians(degrees):
    return math.radians(degrees)


def trapezoid_area(height, base1, base2):
    return (base1 + base2) * height / 2


def regular_polygon_area(number_of_sides, side_length):
    if number_of_sides < 3:
        raise ValueError("A polygon must have at least 3 sides.")
    return number_of_sides * side_length**2 / (4 * math.tan(math.pi / number_of_sides))


def parallelogram_area(base, height):
    return base * height


def main():
    degrees = float(input("Input degree: "))
    print("Output radian:", degrees_to_radians(degrees))

    height = float(input("Height: "))
    base1 = float(input("Base, first value: "))
    base2 = float(input("Base, second value: "))
    print("Trapezoid area:", trapezoid_area(height, base1, base2))

    sides = int(input("Input number of sides: "))
    side_length = float(input("Input the length of a side: "))
    print("The area of the polygon is:", regular_polygon_area(sides, side_length))

    base = float(input("Length of base: "))
    parallelogram_height = float(input("Height of parallelogram: "))
    print("Parallelogram area:", parallelogram_area(base, parallelogram_height))


if __name__ == "__main__":
    main()