from abc import ABC, abstractmethod


class Magical(ABC):
    @abstractmethod
    def cast_spell(self, spell_name: str, targets: list) -> dict:
        """Cast a named spell on a list of targets."""
        pass

    @abstractmethod
    def channel_mana(self, amount: int) -> dict:
        """Channel a given amount of mana."""
        pass

    @abstractmethod
    def get_magic_stats(self) -> dict:
        """Return magic statistics."""
        pass
