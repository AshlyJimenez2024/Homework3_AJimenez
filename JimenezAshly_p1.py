
"""Problem 1: An N-dimensional vector class."""

from __future__ import annotations
from numbers import Real
from typing import Sequence

Number = int | float


def testif(condition: bool, testname: str,
           msgOK: str = "", msgFailed: str = "") -> bool:
    """Print the result of a test."""
    if condition:
        print("Success: " + testname + "; " + msgOK)
    else:
        print("Failed: " + testname + "; " + msgFailed)
    return condition


class NVector:
    """Represent a vector of real numbers."""

    def __init__(self, *values: Number | Sequence[Number]) -> None:
        """Create a vector from a sequence or multiple numbers."""
        if len(values) == 1:
            self.elements = list(values[0])
        elif len(values) >= 2:
            self.elements = list(values)
        else:
            raise TypeError("Provide a sequence or multiple numbers")

        if not all(isinstance(v, Real) for v in self.elements):
            raise TypeError("Vector elements must be real numbers")

    def __len__(self) -> int:
        """Return the number of elements."""
        return len(self.elements)

    def __getitem__(self, index: int) -> Number:
        """Get an element using its index."""
        return self.elements[index]

    def __setitem__(self, index: int, value: Number) -> None:
        """Change an element at the given index."""
        if not isinstance(value, Real):
            raise TypeError("Value must be a real number")
        self.elements[index] = value

    def __str__(self) -> str:
        """Return a readable vector."""
        return f"NVector({self.elements})"

    def __eq__(self, other: object) -> bool:
        """Compare two vectors for equality."""
        return isinstance(other, NVector) and self.elements == other.elements

    def __ne__(self, other: object) -> bool:
        """Compare two vectors for inequality."""
        return not self == other

    def __add__(self, other: NVector | Number) -> NVector:
        """Add another vector or a number."""
        if isinstance(other, NVector):
            if len(self) != len(other):
                raise ValueError("Vectors must have the same dimension")
            return NVector([a + b for a, b in
                            zip(self.elements, other.elements)])

        if isinstance(other, Real):
            return NVector([a + other for a in self.elements])

        return NotImplemented

    def __radd__(self, other: Number) -> NVector:
        """Add a number from the left."""
        return self + other

    def __mul__(self, other: NVector | Number) -> Number:
        """Calculate a dot product or scalar product sum."""
        if isinstance(other, NVector):
            if len(self) != len(other):
                raise ValueError("Vectors must have the same dimension")
            return sum(a * b for a, b in
                       zip(self.elements, other.elements))

        if isinstance(other, Real):
            return sum(a * other for a in self.elements)

        return NotImplemented

    def __rmul__(self, other: Number) -> Number:
        """Multiply with a number on the left."""
        return self * other

    @classmethod
    def zeros(cls, n: int) -> NVector:
        """Create a vector containing n zeros."""
        if not isinstance(n, int):
            raise TypeError("Dimension must be an integer")
        if n < 0:
            raise ValueError("Dimension cannot be negative")
        return cls([0] * n)


def main() -> None:
    """Run examples and unit tests."""
    print("Problem 1 - NVector - Ashly Jimenez")
    print("FAU Student ID: Z23814804")

    source = [3, 0, 1, -1]
    vector = NVector(source)

    source = [3, 0, 1, -1]
    vector = NVector(source)
    source[0] = 99

    testif(vector[0] == 3, "checking original list")
    testif(NVector(3, 0, 1, -1) == vector, "testing vector creation")
    testif(len(vector) == 4, "length")
    testif(vector[1] == 0 and vector[-2] == 1, "indexing")

    vector[2] = 5
    testif(vector[2] == 5, "updating vector value")
    vector[2] = 1

    testif(str(vector) == "NVector([3, 0, 1, -1])", "string")
    testif(vector != NVector(1, 2, 3, 4), "comparing different vectors")

    testif(vector + NVector(1, 2, 3, 4) ==
           NVector(4, 2, 4, 3), "adding two vectors")

    testif(vector + 10 ==
           NVector(13, 10, 11, 9), "adding a number")

    testif(10 + vector ==
           NVector(13, 10, 11, 9), "reflected addition test ")

    testif(vector * NVector(1, 2, 3, 4) == 2,
           "dot product")

    testif(vector * 2 == 6 and 2 * vector == 6,
           "scalar multiplication")

    testif(NVector.zeros(4) ==
           NVector([0, 0, 0, 0]), "creating zero vector")

    try:
        vector[99] = 3
    except IndexError:
        testif(True, "invalid index")
    else:
        testif(False, "invalid index")

    print("Example:", vector)


if __name__ == "__main__":
    main()
