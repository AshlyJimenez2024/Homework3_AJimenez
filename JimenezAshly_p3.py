
# Copyright 2017, 2013, 2011 Pearson Education, Inc.
# W.F. Punch & R.J. Enbody
# Problem 3 - Predator, Prey, and Human Simulation

from __future__ import annotations

import random
import time
import matplotlib.pyplot as plt


class Island(object):
    """An n by n grid where animals live and empty cells contain 0."""

    def __init__(self, n: int, prey_count: int = 0,
                 predator_count: int = 0,
                 count_humans: int = 0) -> None:
        """Create the island and add the starting populations."""
        if n <= 0:
            raise ValueError("Island size must be positive.")

        if min(prey_count, predator_count, count_humans) < 0:
            raise ValueError("Population counts cannot be negative.")

        if prey_count + predator_count + count_humans > n * n:
            raise ValueError("Too many animals for this island.")

        self.grid_size = n
        self.grid = []

        for i in range(n):
            row = [0] * n
            self.grid.append(row)

        self.init_animals(prey_count, predator_count, count_humans)

    def init_animals(self, prey_count: int, predator_count: int,
                     count_humans: int) -> None:
        """Place prey, predators, and humans randomly on the island."""

        count = 0
        while count < prey_count:
            x = random.randint(0, self.grid_size - 1)
            y = random.randint(0, self.grid_size - 1)

            if not self.animal(x, y):
                new_prey = Prey(island=self, x=x, y=y)
                count += 1
                self.register(new_prey)

        count = 0
        while count < predator_count:
            x = random.randint(0, self.grid_size - 1)
            y = random.randint(0, self.grid_size - 1)

            if not self.animal(x, y):
                new_predator = Predator(island=self, x=x, y=y)
                count += 1
                self.register(new_predator)

        # NEW: Randomly place humans in empty cells.
        count = 0
        while count < count_humans:
            x = random.randint(0, self.grid_size - 1)
            y = random.randint(0, self.grid_size - 1)

            if not self.animal(x, y):
                new_human = Human(island=self, x=x, y=y)
                count += 1
                self.register(new_human)

    def clear_all_moved_flags(self) -> None:
        """Allow each animal to move during the next tick."""
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if self.grid[x][y]:
                    self.grid[x][y].clear_moved_flag()

    def size(self) -> int:
        """Return one dimension of the island."""
        return self.grid_size

    def register(self, animal: Animal) -> None:
        """Place an animal at its coordinates."""
        x = animal.x
        y = animal.y
        self.grid[x][y] = animal

    def remove(self, animal: Animal) -> None:
        """Remove an animal if it still occupies its location."""
        x = animal.x
        y = animal.y

        if self.grid[x][y] is animal:
            self.grid[x][y] = 0

    def animal(self, x: int, y: int) -> Animal | int:
        """Return the animal at a position or -1 outside the grid."""
        if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
            return self.grid[x][y]
        else:
            return -1

    def __str__(self) -> str:
        """Display the island with O for prey, X for predators,
        H for humans, and dots for empty spaces.
        """
        s = ""

        for j in range(self.grid_size - 1, -1, -1):
            for i in range(self.grid_size):
                if not self.grid[i][j]:
                    s += "{:<2s}".format("." + "  ")
                else:
                    s += "{:<2s}".format(
                        str(self.grid[i][j]) + "  "
                    )
            s += "\n"

        return s

    def count_prey(self) -> int:
        """Count all prey currently on the island."""
        count = 0

        for x in range(self.grid_size):
            for y in range(self.grid_size):
                animal = self.animal(x, y)
                if isinstance(animal, Prey):
                    count += 1

        return count

    def count_predators(self) -> int:
        """Count all predators currently on the island."""
        count = 0

        for x in range(self.grid_size):
            for y in range(self.grid_size):
                animal = self.animal(x, y)
                if isinstance(animal, Predator):
                    count += 1

        return count

    # NEW: Count the human population.
    def count_humans(self) -> int:
        """Count all humans currently on the island."""
        count = 0

        for x in range(self.grid_size):
            for y in range(self.grid_size):
                animal = self.animal(x, y)
                if isinstance(animal, Human):
                    count += 1

        return count


class Animal(object):
    """Base class for animals that move and breed on the island."""

    def __init__(self, island: Island, x: int = 0,
                 y: int = 0, s: str = "A") -> None:
        """Initialize an animal and its position."""
        self.island = island
        self.name = s
        self.x = x
        self.y = y
        self.moved = False

    def position(self) -> tuple[int, int]:
        """Return the animal's current coordinates."""
        return self.x, self.y

    def __str__(self) -> str:
        """Return the animal's display symbol."""
        return self.name

    def check_grid(self, type_looking_for: type = int
                   ) -> tuple[int, int] | int:
        """Check eight neighboring cells for a requested type.

        Return the first matching coordinates or 0 if none exist.
        """
        offset = [
            (-1, 1), (0, 1), (1, 1),
            (-1, 0), (1, 0),
            (-1, -1), (0, -1), (1, -1)
        ]

        result = 0

        for i in range(len(offset)):
            x = self.x + offset[i][0]
            y = self.y + offset[i][1]

            if not 0 <= x < self.island.size() or \
               not 0 <= y < self.island.size():
                continue

            if type(self.island.animal(x, y)) == type_looking_for:
                result = (x, y)
                break

        return result

    def move(self) -> None:
        """Move into an empty neighboring cell if possible."""
        if not self.moved:
            location = self.check_grid(int)

            if location:
                self.island.remove(self)
                self.x = location[0]
                self.y = location[1]
                self.island.register(self)
                self.moved = True

    def breed(self) -> None:
        """Create an animal of the same class in an empty cell."""
        if self.breed_clock <= 0:
            location = self.check_grid(int)

            if location:
                self.breed_clock = self.breed_time
                the_class = self.__class__

                new_animal = the_class(
                    self.island,
                    x=location[0],
                    y=location[1]
                )

                self.island.register(new_animal)

    def clear_moved_flag(self) -> None:
        """Reset the movement flag."""
        self.moved = False


class Prey(Animal):
    """Prey animals move and breed but do not hunt."""

    breed_time: int = 3

    def __init__(self, island: Island, x: int = 0,
                 y: int = 0, s: str = "O") -> None:
        """Create a prey animal and set its breeding clock."""
        Animal.__init__(self, island, x, y, s)
        self.breed_clock = self.breed_time

    def clock_tick(self) -> None:
        """Decrease the prey's breeding clock by one."""
        self.breed_clock -= 1


class Predator(Animal):
    """Predators eat prey, breed, move, and may starve."""

    breed_time: int = 6
    starve_time: int = 3

    def __init__(self, island: Island, x: int = 0,
                 y: int = 0, s: str = "X") -> None:
        """Create a predator with breeding and starvation clocks."""
        Animal.__init__(self, island, x, y, s)
        self.starve_clock = self.starve_time
        self.breed_clock = self.breed_time

    def clock_tick(self) -> None:
        """Decrease breeding and starvation clocks."""
        self.breed_clock -= 1
        self.starve_clock -= 1

        if self.starve_clock <= 0:
            self.island.remove(self)

    def eat(self) -> None:
        """Eat neighboring prey and move into its position."""
        if not self.moved:
            location = self.check_grid(Prey)

            if location:
                prey = self.island.animal(
                    location[0], location[1]
                )

                self.island.remove(prey)
                self.island.remove(self)

                self.x = location[0]
                self.y = location[1]

                self.island.register(self)
                self.starve_clock = self.starve_time
                self.moved = True


# NEW CLASS REQUIRED BY THE PROFESSOR
class Human(Animal):
    """Humans hunt predators, move, breed, and can starve.

    Humans do not hunt or eat prey.
    """

    breed_time: int = 8
    starve_time: int = 6
    hunt_time: int = 2

    def __init__(self, island: Island, x: int = 0,
                 y: int = 0, s: str = "H") -> None:
        """Create a human with breeding, hunting, and hunger clocks."""
        Animal.__init__(self, island, x, y, s)

        self.breed_clock = self.breed_time
        self.starve_clock = self.starve_time

        # A new human waits hunt_time ticks before hunting.
        self.hunt_clock = self.hunt_time

    def hunt(self) -> None:
        """Hunt a neighboring predator when the hunt clock expires.

        If successful, move into the predator's cell and reset hunger.
        """
        if self.moved or self.hunt_clock > 0:
            return

        location = self.check_grid(Predator)

        if location:
            predator = self.island.animal(
                location[0], location[1]
            )

            self.island.remove(predator)
            self.island.remove(self)

            self.x = location[0]
            self.y = location[1]

            self.island.register(self)

            # Eating a predator prevents starvation.
            self.starve_clock = self.starve_time
            self.moved = True

        # Wait before the next hunting attempt.
        self.hunt_clock = self.hunt_time

    def clock_tick(self) -> None:
        """Decrease the human's three clocks and check starvation."""
        self.breed_clock -= 1
        self.starve_clock -= 1
        self.hunt_clock -= 1

        if self.starve_clock <= 0:
            self.island.remove(self)


def main(
    predator_breed_time: int = 6,
    predator_starve_time: int = 3,
    initial_predators: int = 15,
    prey_breed_time: int = 3,
    initial_prey: int = 40,
    size: int = 12,
    ticks: int = 1000,
    human_breed_time: int = 10,
    human_starve_time: int = 8,
    human_hunt_time: int = 3,
    initial_humans: int = 8
) -> None:
    """Run the island simulation and graph three populations."""

    # Original predator and prey settings.
    Predator.breed_time = predator_breed_time
    Predator.starve_time = predator_starve_time
    Prey.breed_time = prey_breed_time

    # NEW: Initialize human class settings.
    Human.breed_time = human_breed_time
    Human.starve_time = human_starve_time
    Human.hunt_time = human_hunt_time

    if min(
        Predator.breed_time, Predator.starve_time,
        Prey.breed_time, Human.breed_time,
        Human.starve_time, Human.hunt_time
    ) <= 0:
        raise ValueError("All time settings must be positive.")

    # Lists for the graph.
    predator_list = []
    prey_list = []
    human_list = []

    # Create the island with all three populations.
    isle = Island(
        size,
        initial_prey,
        initial_predators,
        initial_humans
    )

    print("Problem 3 - Predator, Prey, and Human Simulation")
    print("FAU Student ID: Z23814804")

    print("\nINITIAL ISLAND")
    print("O = Prey, X = Predator, H = Human")
    print(isle)

    # Record the starting populations.
    prey_list.append(isle.count_prey())
    predator_list.append(isle.count_predators())
    human_list.append(isle.count_humans())

    stable_ticks = 0
    completed_ticks = 0

    # Maximum allowed simulation length is 1000 ticks.
    for i in range(min(ticks, 1000)):
        isle.clear_all_moved_flags()

        # Track animals already processed during this tick.
        processed = set()

        for x in range(size):
            for y in range(size):
                animal = isle.animal(x, y)

                if not animal:
                    continue

                if id(animal) in processed:
                    continue

                processed.add(id(animal))

                # Predator behavior remains the same.
                if isinstance(animal, Predator):
                    animal.eat()

                # NEW: Humans hunt predators, not prey.
                elif isinstance(animal, Human):
                    animal.hunt()

                # Skip animals removed during this tick.
                if isle.animal(animal.x, animal.y) is not animal:
                    continue

                animal.move()
                animal.breed()
                animal.clock_tick()

        # Count all three populations after this tick.
        prey_count = isle.count_prey()
        predator_count = isle.count_predators()
        human_count = isle.count_humans()

        prey_list.append(prey_count)
        predator_list.append(predator_count)
        human_list.append(human_count)

        completed_ticks = i + 1

        # Show progress every 10 ticks.
        if i % 10 == 0:
            print(
                f"Tick {completed_ticks}: "
                f"Prey={prey_count}, "
                f"Predators={predator_count}, "
                f"Humans={human_count}"
            )

        # Stop only when ALL THREE populations remain constant.
        if (
            prey_list[-1] == prey_list[-2]
            and predator_list[-1] == predator_list[-2]
            and human_list[-1] == human_list[-2]
        ):
            stable_ticks += 1
        else:
            stable_ticks = 0

        # Use 30 consecutive unchanged ticks as the
        # practical convergence condition.
        if stable_ticks >= 30:
            print("\nAll three populations stabilized.")
            break

    # Required final island display.
    print("\nFINAL ISLAND")
    print(isle)

    print("FINAL POPULATION RESULTS")
    print("Prey:", isle.count_prey())
    print("Predators:", isle.count_predators())
    print("Humans:", isle.count_humans())
    print("Total ticks:", completed_ticks)

    # Required graph of all three populations.
    plt.figure(figsize=(10, 6))

    plt.plot(prey_list, label="Prey")
    plt.plot(predator_list, label="Predators")
    plt.plot(human_list, label="Humans")

    plt.xlabel("Time (Ticks)")
    plt.ylabel("Population")
    plt.title("Predator, Prey, and Human Population Simulation")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
