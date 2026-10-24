from ex4.TournamentCard import TournamentCard


class TournamentPlatform:
    def __init__(self) -> None:
        self._cards: dict[str, TournamentCard] = {}
        self._matches_played: int = 0
        self._counter: int = 0

    def register_card(self, card: TournamentCard) -> str:
        self._counter += 1
        base = card.name.lower().replace(' ', '_')
        card_id = f"{base}_{self._counter:03d}"
        self._cards[card_id] = card
        return card_id

    def create_match(self, card1_id: str, card2_id: str) -> dict:
        card1 = self._cards.get(card1_id)
        card2 = self._cards.get(card2_id)
        if card1 is None or card2 is None:
            return {'error': 'One or both cards not found.'}

        if card1.attack_power >= card2.attack_power:
            winner, loser = card1, card2
            winner_id, loser_id = card1_id, card2_id
        else:
            winner, loser = card2, card1
            winner_id, loser_id = card2_id, card1_id

        winner.update_wins(1)
        loser.update_losses(1)
        self._matches_played += 1

        return {
            'winner': winner_id,
            'loser': loser_id,
            'winner_rating': winner.calculate_rating(),
            'loser_rating': loser.calculate_rating(),
        }

    def get_leaderboard(self) -> list:
        ranked = sorted(
            self._cards.items(),
            key=lambda item: item[1].calculate_rating(),
            reverse=True,
        )
        leaderboard = []
        for card_id, card in ranked:
            rank_info = card.get_rank_info()
            leaderboard.append({
                'id': card_id,
                'name': card.name,
                'rating': card.calculate_rating(),
                'record': (
                    f'{rank_info["wins"]}-{rank_info["losses"]}'
                ),
            })
        return leaderboard

    def generate_tournament_report(self) -> dict:
        ratings = [c.calculate_rating() for c in self._cards.values()]
        avg = int(sum(ratings) / len(ratings)) if ratings else 0
        return {
            'total_cards': len(self._cards),
            'matches_played': self._matches_played,
            'avg_rating': avg,
            'platform_status': 'active',
        }
