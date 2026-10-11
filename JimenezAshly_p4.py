
"""Problem 4 - Non-Interactive Text Editor.

This program reads, searches, replaces, and adds text to files.
"""

from pathlib import Path
from testif import testif


def ed_read(filename: str, from_: int = 0, to: int = -1) -> str:
    """Read part of a UTF-8 text file.

    Preconditions:
        The file must exist and be readable.
        from_ must be a nonnegative integer.
        to must be -1 or greater than or equal to from_.

    Postconditions:
        Returns the requested text without changing the file.

    Raises:
        TypeError or ValueError for invalid positions.
        IndexError if to exceeds the file length.
        File I/O errors are passed to the caller.
    """
    if not isinstance(from_, int) or not isinstance(to, int):
        raise TypeError("Positions must be integers")

    if from_ < 0 or (to != -1 and to < from_):
        raise ValueError("Invalid reading positions")

    with open(filename, "r", encoding="utf-8") as file:
        content = file.read()

    if to > len(content):
        raise IndexError("Ending position is past the file length")

    if to == -1:
        return content[from_:]

    return content[from_:to]


def ed_find(filename: str, search_str: str) -> list[int]:
    """Find all starting positions of a string in a file.

    Preconditions:
        The file must exist and be readable.
        search_str must be a nonempty string.

    Postconditions:
        Returns a list of positions, or [] if not found.
        Does not change the file.

    Raises:
        TypeError or ValueError for invalid search text.
        File I/O errors are passed to the caller.
    """
    if not isinstance(search_str, str):
        raise TypeError("Search text must be a string")

    if search_str == "":
        raise ValueError("Search text cannot be empty")

    with open(filename, "r", encoding="utf-8") as file:
        content = file.read()

    positions = []
    start = 0

    while True:
        index = content.find(search_str, start)

        if index == -1:
            break

        positions.append(index)
        start = index + 1

    return positions


def ed_replace(filename: str, search_str: str,
               replace_with: str, occurrence: int = -1) -> int:
    """Replace one or all occurrences of text in a file.

    Preconditions:
        The file must exist and be readable and writable.
        search_str must be a nonempty string.
        replace_with must be a string.
        occurrence must be -1 or a nonnegative integer.

    Postconditions:
        -1 replaces all occurrences.
        A nonnegative index replaces one selected occurrence.
        Returns the number of replacements.
        Leaves the file unchanged if no match is selected.

    Raises:
        TypeError or ValueError for invalid arguments.
        File I/O errors are passed to the caller.
    """
    if not isinstance(search_str, str):
        raise TypeError("Search text must be a string")

    if not isinstance(replace_with, str):
        raise TypeError("Replacement must be a string")

    if search_str == "":
        raise ValueError("Search text cannot be empty")

    if not isinstance(occurrence, int):
        raise TypeError("Occurrence must be an integer")

    if occurrence < -1:
        raise ValueError("Occurrence cannot be less than -1")

    with open(filename, "r", encoding="utf-8") as file:
        content = file.read()

    if occurrence == -1:
        count = content.count(search_str)

        if count == 0:
            return 0

        updated = content.replace(search_str, replace_with)

    else:
        positions = []
        start = 0

        while True:
            index = content.find(search_str, start)

            if index == -1:
                break

            positions.append(index)
            start = index + len(search_str)

        if occurrence >= len(positions):
            return 0

        index = positions[occurrence]

        updated = (
            content[:index]
            + replace_with
            + content[index + len(search_str):]
        )

        count = 1

    with open(filename, "w", encoding="utf-8") as file:
        file.write(updated)

    return count


def ed_append(filename: str, string: str) -> int:
    """Add text to the end of a UTF-8 file.

    Preconditions:
        filename must be a valid writable path.
        string must be a string.

    Postconditions:
        Adds text without removing existing content.
        Creates the file if it does not exist.
        Returns the number of characters written.

    Raises:
        TypeError for invalid text.
        File I/O errors are passed to the caller.
    """
    if not isinstance(string, str):
        raise TypeError("Text must be a string")

    with open(filename, "a", encoding="utf-8") as file:
        return file.write(string)


def test_ed_find() -> None:
    """Check repeated, single, and missing search results."""
    filename = "test_find.txt"

    Path(filename).write_text(
        "Java Python Java SQL Java", encoding="utf-8"
    )

    testif(
        ed_find(filename, "Java") == [0, 12, 21],
        "Find Java multiple times"
    )

    testif(
        ed_find(filename, "Python") == [5],
        "Find Python once"
    )

    testif(
        ed_find(filename, "Swift") == [],
        "Find a word not in the file"
    )

    Path(filename).unlink()


def test_ed_replace() -> None:
    """Check replacing all, one, and missing occurrences."""
    filename = "test_replace.txt"

    Path(filename).write_text(
        "Python Java Python", encoding="utf-8"
    )

    count = ed_replace(filename, "Python", "Swift")

    testif(
        count == 2
        and ed_read(filename) == "Swift Java Swift",
        "Replace both Python words"
    )

    Path(filename).write_text(
        "Python Java Python", encoding="utf-8"
    )

    count = ed_replace(filename, "Python", "Swift", 1)

    testif(
        count == 1
        and ed_read(filename) == "Python Java Swift",
        "Replace only the second Python"
    )

    count = ed_replace(filename, "HTML", "CSS")

    testif(
        count == 0
        and ed_read(filename) == "Python Java Swift",
        "No replacement for missing word"
    )

    Path(filename).unlink()


def main() -> None:
    """Demonstrate all four editing functions and run tests."""
    filename = "ashly_notes.txt"

    print("Problem 4 - Non-Interactive Text Editor")
    print("FAU Student ID: Z23814804")
    print()

    # Create a fresh file for the example.
    Path(filename).write_text("", encoding="utf-8")

    print("PART A AND C - FILE EDITING EXAMPLES")

    print("Characters added:", ed_append(filename, "0123456789"))
    print("Characters added:", ed_append(filename, "0123456789"))

    print("Text inside my file:", ed_read(filename))
    print("Reading positions 3 to 9:", ed_read(filename, 3, 9))
    print("Reading from position 3:", ed_read(filename, 3))

    print("Searching for 345:", ed_find(filename, "345"))
    print("Searching for 356:", ed_find(filename, "356"))

    print(
        "Replacing the second 345:",
        ed_replace(filename, "345", "ABCDE", 1)
    )

    print("File after one replacement:", ed_read(filename))

    # Restore the text before replacing all matches.
    Path(filename).write_text(
        "01234567890123456789", encoding="utf-8"
    )

    print(
        "Replacing every 345:",
        ed_replace(filename, "345", "ABCDE")
    )

    print("File after all replacements:", ed_read(filename))

    print()
    print("PART B - TEST RESULTS")

    test_ed_find()
    test_ed_replace()

    print()
    print("All file editing functions finished.")


if __name__ == "__main__":
    main()
