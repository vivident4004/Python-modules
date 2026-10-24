from ex0.Card import Card
from ex2.Combatable import Combatable
from ex4.Rankable import Rankable


class TournamentCard(Card, Combatable, Rankable):
    def __init__(
        self,
        name: str,
        cost: int,
        rarity: str,
        attack_power: int,
        defense: int,
        base_rating: int = 1200,
    ) -> None:
        super().__init__(name, cost, rarity)
        self.attack_power = attack_power
        self.defense = defense
        self._wins: int = 0
        self._losses: int = 0
        self._rating: int = base_rating

    def play(self, game_state: dict) -> dict:
        return {
            'card_played': self.name,
            'mana_used': self.cost,
            'effect': 'Tournament card enters play',
        }

    def get_card_info(self) -> dict:
        info = super().get_card_info()
        info['type'] = 'TournamentCard'
        info['attack'] = self.attack_power
        info['defense'] = self.defense
        return info

    def attack(self, target: Card) -> dict:
        target_name = (
            target.name if hasattr(target, 'name') else str(target)
        )
        return {
            'attacker': self.name,
            'target': target_name,
            'damage': self.attack_power,
        }

    def defend(self, incoming_damage: int) -> dict:
        blocked = min(self.defense, incoming_damage)
        return {
            'defender': self.name,
            'damage_taken': incoming_damage - blocked,
            'damage_blocked': blocked,
        }

    def get_combat_stats(self) -> dict:
        return {'attack': self.attack_power, 'defense': self.defense}

    def calculate_rating(self) -> int:
        return self._rating

    def update_wins(self, wins: int) -> None:
        self._wins += wins
        self._rating += wins * 16

    def update_losses(self, losses: int) -> None:
        self._losses += losses
        self._rating -= losses * 16

    def get_rank_info(self) -> dict:
        return {
            'name': self.name,
            'rating': self._rating,
            'wins': self._wins,
            'losses': self._losses,
        }

    def get_tournament_stats(self) -> dict:
        return {
            'name': self.name,
            'interfaces': ['Card', 'Combatable', 'Rankable'],
            'rating': self._rating,
            'record': f'{self._wins}-{self._losses}',
        }
