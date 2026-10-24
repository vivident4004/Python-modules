import random

from ex0.Card import Card
from ex0.CreatureCard import CreatureCard
from ex1.ArtifactCard import ArtifactCard
from ex1.SpellCard import SpellCard
from ex3.CardFactory import CardFactory

_CREATURES = {
    'dragon': ('Fire Dragon', 5, 'Legendary', 7, 5),
    'goblin': ('Goblin Warrior', 2, 'Common', 2, 1),
}

_SPELLS = {
    'fireball': ('Fireball', 4, 'Rare', 'damage'),
}

_ARTIFACTS = {
    'mana_ring': ('Mana Ring', 2, 'Uncommon', 3, '+1 mana per turn'),
}


class FantasyCardFactory(CardFactory):
    def create_creature(
        self, name_or_power: str | int | None = None
    ) -> Card:
        key = (
            name_or_power if name_or_power in _CREATURES else 'dragon'
        )
        return CreatureCard(*_CREATURES[key])

    def create_spell(
        self, name_or_power: str | int | None = None
    ) -> Card:
        key = (
            name_or_power if name_or_power in _SPELLS else 'fireball'
        )
        return SpellCard(*_SPELLS[key])

    def create_artifact(
        self, name_or_power: str | int | None = None
    ) -> Card:
        key = (
            name_or_power
            if name_or_power in _ARTIFACTS
            else 'mana_ring'
        )
        return ArtifactCard(*_ARTIFACTS[key])

    def create_themed_deck(self, size: int) -> dict:
        creators = [
            self.create_creature,
            self.create_spell,
            self.create_artifact,
        ]
        cards = [random.choice(creators)() for _ in range(size)]
        return {'cards': cards, 'size': size, 'theme': 'Fantasy'}

    def get_supported_types(self) -> dict:
        return {
            'creatures': list(_CREATURES.keys()),
            'spells': list(_SPELLS.keys()),
            'artifacts': list(_ARTIFACTS.keys()),
        }
