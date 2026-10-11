
"""Problem 5 - Recursion Practice.

Part A: Recursive leaf drawings
Part B: Base conversion
Part C: Binomial coefficient with memoization
Part D: Recursive list pairing
"""

import turtle
from testif import testif


# PART A - RECURSIVE LEAF

def add_flower() -> None:
    """Draw a small pink flower at the tip of a branch."""
    turtle.dot(9, "lightpink")
    turtle.dot(4, "deeppink")


def leaf_branch(level: int, length: float) -> None:
    """Draw a branching pattern and return to the starting position."""
    if level == 0:
        add_flower()
        return

    turtle.forward(length)

    turtle.left(35)
    leaf_branch(level - 1, length * 0.68)

    turtle.right(70)
    leaf_branch(level - 1, length * 0.68)

    turtle.left(35)
    turtle.backward(length)


def draw_leaf_straight(level: int, petiole: float) -> None:
    """Draw a vertical leaf with recursive branches and pink flowers."""
    turtle.reset()
    turtle.speed(0)
    turtle.hideturtle()
    turtle.pensize(2)
    turtle.color("deeppink")

    turtle.penup()
    turtle.goto(0, -250)
    turtle.setheading(90)
    turtle.pendown()

    turtle.forward(petiole)
    leaf_branch(level, 80)


# EXTRA CREDIT - CURVED LEAF

def add_butterfly() -> None:
    """Draw a small butterfly with pink wings and a yellow body."""
    x, y = turtle.position()
    heading = turtle.heading()

    turtle.penup()

    # Upper pink wings
    turtle.goto(x - 9, y + 5)
    turtle.dot(17, "hotpink")

    turtle.goto(x + 9, y + 5)
    turtle.dot(17, "hotpink")

    # Lower light-pink wings
    turtle.goto(x - 7, y - 6)
    turtle.dot(12, "lightpink")

    turtle.goto(x + 7, y - 6)
    turtle.dot(12, "lightpink")

    # Yellow butterfly body
    turtle.goto(x, y)
    turtle.dot(8, "yellow")

    # White details on the wings
    turtle.goto(x - 9, y + 5)
    turtle.dot(4, "white")

    turtle.goto(x + 9, y + 5)
    turtle.dot(4, "white")

    # Return to original position
    turtle.goto(x, y)
    turtle.setheading(heading)
    turtle.pendown()


def add_neon_flower() -> None:
    """Draw a neon-yellow flower with a hot-pink center."""
    x, y = turtle.position()

    turtle.penup()

    for dx, dy in [
        (0, 7),
        (7, 2),
        (4, -6),
        (-4, -6),
        (-7, 2)
    ]:
        turtle.goto(x + dx, y + dy)
        turtle.dot(9, "yellow")

    turtle.goto(x, y)
    turtle.dot(8, "hotpink")

    turtle.pendown()


def add_pink_leaves() -> None:
    """Draw two small pink leaves beside a branch."""
    x, y = turtle.position()
    heading = turtle.heading()

    turtle.penup()

    turtle.setheading(heading + 55)
    turtle.forward(8)
    turtle.dot(8, "lightpink")

    turtle.goto(x, y)
    turtle.setheading(heading - 55)
    turtle.forward(8)
    turtle.dot(8, "lightpink")

    turtle.goto(x, y)
    turtle.setheading(heading)
    turtle.pendown()


def add_heart() -> None:
    """Draw a tiny pink heart near a flower."""
    x, y = turtle.position()
    heading = turtle.heading()

    turtle.penup()
    turtle.goto(x + 10, y + 12)
    turtle.setheading(0)

    turtle.color("deeppink")
    turtle.begin_fill()

    turtle.left(140)
    turtle.forward(7)
    turtle.circle(-4, 200)
    turtle.left(120)
    turtle.circle(-4, 200)
    turtle.forward(7)

    turtle.end_fill()

    turtle.penup()
    turtle.goto(x, y)
    turtle.setheading(heading)
    turtle.color("hotpink")
    turtle.pendown()


def add_sparkles() -> None:
    """Add small yellow sparkles around a flower."""
    x, y = turtle.position()

    turtle.penup()

    for dx, dy in [
        (-14, 14),
        (14, 14),
        (-15, -8),
        (15, -8)
    ]:
        turtle.goto(x + dx, y + dy)
        turtle.dot(3, "gold")

    turtle.goto(x, y)
    turtle.pendown()


def curved_branch(level: int, length: float) -> None:
    """Draw recursively branching curved stems with decorations."""
    if level == 0:
        add_neon_flower()
        add_sparkles()
        add_heart()
        return

    for _ in range(5):
        turtle.forward(length / 5)
        turtle.right(3)

    if level >= 3:
        add_pink_leaves()

    # Add pink butterflies to the curved branches
    if level == 3:
        add_butterfly()

    turtle.left(45)
    curved_branch(level - 1, length * 0.65)

    turtle.right(85)
    curved_branch(level - 1, length * 0.65)

    turtle.left(40)

    for _ in range(5):
        turtle.left(3)
        turtle.backward(length / 5)


def draw_leaf_curved(level: int, petiole: float) -> None:
    """Draw a decorative curved leaf with hot-pink branches."""
    turtle.reset()
    turtle.speed(0)

    # Draw everything faster
    turtle.tracer(0, 0)

    turtle.hideturtle()
    turtle.pensize(3)
    turtle.color("hotpink")

    turtle.penup()
    turtle.goto(0, -250)
    turtle.setheading(90)
    turtle.pendown()

    turtle.forward(petiole)
    curved_branch(level, 80)

    # Display the completed drawing
    turtle.update()


# PART B - BASE CONVERSION

def strB(n: int, base: int = 10) -> str:
    """Convert a nonnegative integer to a given base recursively.

    Preconditions:
        n is a nonnegative integer.
        base is an integer between 2 and 26.

    Returns:
        A string representation of n in the selected base.
    """
    if not isinstance(n, int) or n < 0:
        raise ValueError("n must be a nonnegative integer")

    if not isinstance(base, int) or not 2 <= base <= 26:
        raise ValueError("base must be between 2 and 26")

    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    if n < base:
        return digits[n]

    return strB(n // base, base) + digits[n % base]


def test_strB() -> None:
    """Run four unit tests for base conversion."""
    testif(strB(25, 2) == "11001", "Binary conversion")
    testif(strB(75, 8) == "113", "Octal conversion")
    testif(strB(255, 16) == "FF", "Hexadecimal conversion")
    testif(strB(50, 10) == "50", "Decimal conversion")


# PART C - MEMOIZED BINOMIAL COEFFICIENT

def Cnk_m(n: int, k: int) -> int:
    """Calculate n choose k recursively using a memo dictionary.

    Preconditions:
        n and k are integers with 0 <= k <= n.

    Returns:
        The binomial coefficient C(n, k).
    """
    if not isinstance(n, int) or not isinstance(k, int):
        raise TypeError("n and k must be integers")

    if n < 0 or k < 0 or k > n:
        raise ValueError("Use 0 <= k <= n")

    memo = {}

    def calculate(a: int, b: int) -> int:
        """Recursively calculate and save repeated results."""
        if b == 0 or b == a:
            return 1

        if (a, b) in memo:
            return memo[(a, b)]

        result = calculate(a - 1, b - 1) + calculate(a - 1, b)
        memo[(a, b)] = result
        return result

    return calculate(n, k)


def test_Cnk_m() -> None:
    """Run four unit tests for the binomial coefficient."""
    testif(Cnk_m(5, 2) == 10, "Choose 5 and 2")
    testif(Cnk_m(6, 3) == 20, "Choose 6 and 3")
    testif(Cnk_m(8, 0) == 1, "Choose 8 and 0")
    testif(Cnk_m(10, 4) == 210, "Choose 10 and 4")


def run_Cnk() -> None:
    """Display several binomial coefficient examples."""
    print("C(7, 3) =", Cnk_m(7, 3))
    print("C(12, 5) =", Cnk_m(12, 5))
    print("C(20, 10) =", Cnk_m(20, 10))
    print("C(30, 15) =", Cnk_m(30, 15))


# PART D - MAKING PAIRS

def make_pairs(seq1: list, seq2: list,
               index: int = 0, result: list | None = None) -> list:
    """Pair matching positions recursively using an accumulator.

    Stops when the shorter sequence ends.
    """
    if result is None:
        result = []

    if index >= len(seq1) or index >= len(seq2):
        return result

    result.append((seq1[index], seq2[index]))

    return make_pairs(seq1, seq2, index + 1, result)


def test_make_pairs() -> None:
    """Run five unit tests, including empty-list cases."""
    testif(
        make_pairs([1, 2, 3], [4, 5, 6])
        == [(1, 4), (2, 5), (3, 6)],
        "Equal-length lists"
    )

    testif(
        make_pairs(["A", "B"], [10, 20, 30])
        == [("A", 10), ("B", 20)],
        "First list is shorter"
    )

    testif(
        make_pairs([1, 2, 3], [9])
        == [(1, 9)],
        "Second list is shorter"
    )

    testif(
        make_pairs([], [1, 2]) == [],
        "First list is empty"
    )

    testif(
        make_pairs([1, 2], []) == [],
        "Second list is empty"
    )


# MAIN PROGRAM

def main() -> None:
    """Demonstrate the recursive functions and run unit tests."""
    print("Problem 5 - Recursive Functions")
    print("FAU Student ID: Z23814804")

    print("\nPART B - BASE CONVERSION")
    print("25 in base 2:", strB(25, 2))
    print("75 in base 8:", strB(75, 8))
    print("255 in base 16:", strB(255, 16))
    test_strB()

    print("\nPART C - BINOMIAL COEFFICIENT")
    run_Cnk()
    test_Cnk_m()

    print("\nPART D - MAKING PAIRS")
    print(make_pairs(["Python", "Java"], [1, 2]))
    test_make_pairs()

    print("\nAll tests completed.")


if __name__ == "__main__":
    main()
