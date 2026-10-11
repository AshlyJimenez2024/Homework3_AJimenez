
"""Problem 6: University file storage using inheritance and recursion."""

from __future__ import annotations

import sys
import unittest


STUDENT_NAME = "Ashly Jimenez"
STUDENT_ID = "Z23814804"


class Entry:
    """Represent a named storage entry with an optional parent."""

    def __init__(self, name: str, parent: Entry | None = None) -> None:
        """Initialize the name and parent; a root has no parent."""
        self.name = name
        self._parent = parent

    def parent(self) -> Entry | None:
        """Return this entry's parent, or None for a root."""
        return self._parent

    def size(self) -> int:
        """Require subclasses to provide their storage size in bytes."""
        raise NotImplementedError("Subclasses must implement size().")

    def absolute_path(self) -> list[Entry]:
        """Recursively return entries from this entry up to the root."""
        if self._parent is None:
            return [self]
        return [self] + self._parent.absolute_path()


class File(Entry):
    """Represent a file with a nonnegative byte count."""

    def __init__(
        self, name: str, bytes_used: int, parent: Entry | None = None
    ) -> None:
        """Initialize a file, rejecting negative storage sizes."""
        super().__init__(name, parent)
        if bytes_used < 0:
            raise ValueError("bytes_used must be nonnegative.")
        self.bytes_used = bytes_used

    def size(self) -> int:
        """Return the number of bytes used by this file."""
        return self.bytes_used


class Folder(Entry):
    """Represent a folder containing files and other folders."""

    def __init__(self, name: str, parent: Entry | None = None) -> None:
        """Initialize an empty folder with an optional parent."""
        super().__init__(name, parent)
        self._children: list[Entry] = []

    def add(self, entry: Entry) -> None:
        """Append a child and set its parent to this folder."""
        self._children.append(entry)
        entry._parent = self

    def children(self) -> tuple[Entry, ...]:
        """Return the immediate children as an immutable tuple."""
        return tuple(self._children)

    def size(self) -> int:
        """Total all child sizes using their shared Entry interface."""
        return sum(child.size() for child in self._children)


def find_large_files(entry: Entry, minimum_size: int) -> list[File]:
    """Recursively find files using at least minimum_size bytes.

    For a file, return that file in a list if it qualifies, otherwise [].
    For a folder, search every child and combine the results. An empty
    folder or a plain Entry yields no files. Equality meets the threshold.
    """
    if isinstance(entry, File):
        return [entry] if entry.size() >= minimum_size else []

    matches: list[File] = []
    if isinstance(entry, Folder):
        for child in entry.children():
            matches.extend(find_large_files(child, minimum_size))
    return matches


class EntryTests(unittest.TestCase):
    """Check recursive searches, paths, and folder storage totals."""

    def setUp(self) -> None:
        """Build a three-level folder hierarchy for each test."""
        self.root = Folder("university")
        self.course = Folder("course")
        self.projects = Folder("projects")
        self.small = File("notes.txt", 100)
        self.medium = File("homework.pdf", 500)
        self.large = File("presentation.mp4", 1500)

        self.root.add(self.small)
        self.root.add(self.course)
        self.course.add(self.medium)
        self.course.add(self.projects)
        self.projects.add(self.large)

    def test_file_threshold(self) -> None:
        """A file qualifies at equality and is excluded above its size."""
        self.assertEqual(find_large_files(self.medium, 500), [self.medium])
        self.assertEqual(find_large_files(self.medium, 501), [])

    def test_nested_search_two_thresholds(self) -> None:
        """Search nested folders at two different thresholds."""
        self.assertEqual(
            find_large_files(self.root, 500), [self.medium, self.large]
        )
        self.assertEqual(find_large_files(self.root, 1000), [self.large])

    def test_empty_and_no_matches(self) -> None:
        """Empty folders and thresholds above all sizes return no files."""
        self.assertEqual(find_large_files(Folder("empty"), 0), [])
        self.assertEqual(find_large_files(self.root, 2000), [])

    def test_zero_size(self) -> None:
        """A zero-byte file qualifies at a zero-byte threshold."""
        empty_file = File("empty.txt", 0)
        self.assertEqual(find_large_files(empty_file, 0), [empty_file])

    def test_root_path(self) -> None:
        """The root's path contains only the root object."""
        self.assertEqual(self.root.absolute_path(), [self.root])
        self.assertIsNone(self.root.parent())

    def test_nested_file_path(self) -> None:
        """The path holds actual objects ordered from file to root."""
        self.assertEqual(
            self.large.absolute_path(),
            [self.large, self.projects, self.course, self.root],
        )

    def test_folder_path(self) -> None:
        """Nested folders also inherit the recursive path method."""
        self.assertEqual(
            self.projects.absolute_path(),
            [self.projects, self.course, self.root],
        )

    def test_polymorphic_size_and_children(self) -> None:
        """A folder totals files and folders through the size interface."""
        self.assertEqual(self.root.size(), 2100)
        self.assertEqual(self.root.children(), (self.small, self.course))
        self.assertIs(self.small.parent(), self.root)

    def test_negative_file_size(self) -> None:
        """The constructor rejects a negative file size."""
        with self.assertRaises(ValueError):
            File("invalid.txt", -1)


def demonstrate() -> None:
    """Demonstrate parts f and g with personalized example data."""
    print(f"Student: {STUDENT_NAME}")
    print(f"FAU student ID: {STUDENT_ID}")
    print("Problem 6: University storage\n")

    root = Folder("Ashly's_ComputerScienceFiles")
    course = Folder("Python_programming_class")
    projects = Folder("projects")
    notes = File("homework_notes.txt", 100)
    homework = File("homework.pdf", 500)
    video = File("presentation.mp4", 1500)

    root.add(notes)
    root.add(course)
    course.add(homework)
    course.add(projects)
    projects.add(video)

    print("Folder levels: Ashly's_ComputerScienceFiles -> Python_programming_class -> projects")
    print(f"Total storage from one root.size() call: {root.size()} bytes")

    for threshold in (500, 1000):
        matches = find_large_files(root, threshold)
        print(f"Files at least {threshold} bytes: {[file.name for file in matches]}")

    print("Absolute path (current entry -> root):")
    print(" -> ".join(entry.name for entry in video.absolute_path()))


def main() -> None:
    """Run the demonstration and standard-library unit tests."""
    demonstrate()
    print("\nUnit tests:")
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(EntryTests)
    result = unittest.TextTestRunner(stream=sys.stdout, verbosity=2).run(suite)
    if not result.wasSuccessful():
        sys.exit(1)


if __name__ == "__main__":
    main()
