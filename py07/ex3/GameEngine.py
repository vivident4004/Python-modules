from ex3.CardFactory import CardFactory
from ex3.GameStrategy import GameStrategy


class GameEngine:
    def __init__(self) -> None:
        self._factory: CardFactory | None = None
        self._strategy: GameStrategy | None = None
        self._turns_simulated: int = 0
        self._total_damage: int = 0
        self._cards_created: int = 0

    def configure_engine(
        self,
        factory: CardFactory,
        strategy: GameStrategy,
    ) -> None:
        self._factory = factory
        self._strategy = strategy

    def simulate_turn(self) -> dict:
        if self._factory is None or self._strategy is None:
            return {'error': 'Engine not configured.'}

        hand = [
            self._factory.create_creature('dragon'),
            self._factory.create_creature('goblin'),
            self._factory.create_spell('fireball'),
        ]
        self._cards_created += len(hand)

        hand_display = [f"{c.name} ({c.cost})" for c in hand]
        result = self._strategy.execute_turn(hand, battlefield=[])

        self._turns_simulated += 1
        self._total_damage += result.get('damage_dealt', 0)

        return {
            'hand': hand_display,
            'strategy': self._strategy.get_strategy_name(),
            'actions': result,
        }

    def get_engine_status(self) -> dict:
        strategy_name = (
            self._strategy.get_strategy_name()
            if self._strategy else None
        )
        return {
            'turns_simulated': self._turns_simulated,
            'strategy_used': strategy_name,
            'total_damage': self._total_damage,
            'cards_created': self._cards_created,
        }
