
"""Problem 2: University Parking Permits."""

from typing import Sequence

# Permit prices are stored here, not inside the cost methods.
FEES = {
    "student_monthly": 25,
    "extra_vehicle": 10,
    "faculty_monthly": 40,
    "garage_monthly": 15,
}


class ParkingPermit:
    """Represent a university parking permit."""

    def __init__(
        self, owner: str, months: int, fees: dict[str, float]
    ) -> None:
        """Store the owner, months, and fee schedule."""
        if months < 0:
            raise ValueError("Months cannot be negative")
        self.owner = owner
        self.months = months
        self.fees = fees.copy()

    def cost(self) -> float:
        """Return the permit cost; subclasses override this."""
        raise NotImplementedError("Use a specific permit type")

    def __str__(self) -> str:
        """Return a readable permit description."""
        return f"{self.owner}: ${self.cost():.2f}"

    def __repr__(self) -> str:
        """Return a detailed representation of the permit."""
        return (
            f"ParkingPermit(owner={self.owner!r}, "
            f"months={self.months!r}, fees={self.fees!r})"
        )


class StudentPermit(ParkingPermit):
    """Represent a student parking permit - Ashly Jimenez."""

    def __init__(
        self, owner: str, months: int,
        fees: dict[str, float], vehicles: int
    ) -> None:
        """Initialize a student permit and vehicle count."""
        super().__init__(owner, months, fees)
        if vehicles < 1:
            raise ValueError("At least one vehicle is required")
        self.vehicles = vehicles

    def cost(self) -> float:
        """Calculate monthly fees plus extra vehicle fees."""
        monthly = self.months * self.fees["student_monthly"]
        extra = (self.vehicles - 1) * self.fees["extra_vehicle"]
        return monthly + extra

    def __str__(self) -> str:
        """Return student owner and total cost."""
        return f"Student - {self.owner}: ${self.cost():.2f}"

    def __repr__(self) -> str:
        """Return student permit constructor details."""
        return (
            f"StudentPermit({self.owner!r}, {self.months!r}, "
            f"{self.fees!r}, {self.vehicles!r})"
        )


class FacultyPermit(ParkingPermit):
    """Represent a faculty parking permit."""

    def __init__(
        self, owner: str, months: int,
        fees: dict[str, float], garage: bool
    ) -> None:
        """Initialize a faculty permit and garage access."""
        super().__init__(owner, months, fees)
        self.garage = garage

    def cost(self) -> float:
        """Calculate monthly fees and optional garage fees."""
        monthly = self.fees["faculty_monthly"]
        if self.garage:
            monthly += self.fees["garage_monthly"]
        return self.months * monthly

    def __str__(self) -> str:
        """Return faculty owner and total cost."""
        return f"Faculty - {self.owner}: ${self.cost():.2f}"

    def __repr__(self) -> str:
        """Return faculty permit constructor details."""
        return (
            f"FacultyPermit({self.owner!r}, {self.months!r}, "
            f"{self.fees!r}, {self.garage!r})"
        )


def summarize_list(permits: Sequence[ParkingPermit]) -> float:
    """Print each permit and return the combined revenue."""
    total = 0.0

    for permit in permits:
        print(permit)
        total += permit.cost()

    return total


def main() -> None:
    """Demonstrate student and faculty parking permits."""
    print("Problem 2 - Parking Permits - Ashly Jimenez")
    print("FAU Student ID: Z23814804")

    permits = [
        StudentPermit("Ashly", 3, FEES, 2),
        StudentPermit("Franchesca", 2, FEES, 1),
        FacultyPermit("Jimenez", 4, FEES, True),
        FacultyPermit("Lesley", 2, FEES, False),
    ]

    print("\nUniversity Parking Permit Information:")
    for permit in permits:
        print(repr(permit))

    print("\nParking Permit Summary:")
    revenue = summarize_list(permits)

    print(f"\nTotal Parking Revenue: ${revenue:.2f}")

if __name__ == "__main__":
    main()
