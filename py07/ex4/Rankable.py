from abc import ABC, abstractmethod


class Rankable(ABC):
    """Abstract interface for tournament ranking."""

    @abstractmethod
    def calculate_rating(self) -> int:
        """Return the current rating."""
        pass

    @abstractmethod
    def update_wins(self, wins: int) -> None:
        """Add wins to the tournament record."""
        pass

    @abstractmethod
    def update_losses(self, losses: int) -> None:
        """Add losses to the tournament record."""
        pass

    @abstractmethod
    def get_rank_info(self) -> dict:
        """Return ranking information."""
        pass
