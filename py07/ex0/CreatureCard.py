from ex0.Card import Card


class CreatureCard(Card):
    """Concrete card: a creature with attack and health."""

    def __init__(
        self,
        name: str,
        cost: int,
        rarity: str,
        attack: int,
        health: int,
    ) -> None:
        if attack <= 0 or health <= 0:
            raise ValueError("Attack and health must be positive integers.")
        super().__init__(name, cost, rarity)
        self.attack = attack
        self.health = health

    def play(self, game_state: dict) -> dict:
        """Summon the creature to the battlefield."""
        return {
            'card_played': self.name,
            'mana_used': self.cost,
            'effect': 'Creature summoned to battlefield',
        }

    def get_card_info(self) -> dict:
        """Return creature card information."""
        info = super().get_card_info()
        info['type'] = 'Creature'
        info['attack'] = self.attack
        info['health'] = self.health
        return info

    def attack_target(self, target) -> dict:
        """Attack a target and return the combat result."""
        target_name = (
            target.name if hasattr(target, 'name') else str(target)
        )
        return {
            'attacker': self.name,
            'target': target_name,
            'damage_dealt': self.attack,
            'combat_resolved': True,
        }
