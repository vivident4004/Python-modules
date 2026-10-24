from ex3.GameStrategy import GameStrategy


class AggressiveStrategy(GameStrategy):
    """Plays lowest-cost cards first and attacks directly."""

    def execute_turn(self, hand: list, battlefield: list) -> dict:
        sorted_hand = sorted(hand, key=lambda c: c.cost)
        played = [c.name for c in sorted_hand]
        mana_used = sum(c.cost for c in sorted_hand)
        targets = self.prioritize_targets(['Enemy Player'])
        damage = sum(c.cost for c in sorted_hand)
        return {
            'cards_played': played,
            'mana_used': mana_used,
            'targets_attacked': targets,
            'damage_dealt': damage,
        }

    def get_strategy_name(self) -> str:
        return 'AggressiveStrategy'

    def prioritize_targets(self, available_targets: list) -> list:
        """Attack all available targets."""
        return available_targets
