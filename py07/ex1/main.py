from ex0.CreatureCard import CreatureCard
from ex1.SpellCard import SpellCard
from ex1.ArtifactCard import ArtifactCard
from ex1.Deck import Deck


def main() -> None:
    print("=== DataDeck deck builder ===")
    print()

    deck = Deck()
    deck.add_card(CreatureCard("Fire Dragon", 5, "Legendary", 7, 5))
    deck.add_card(SpellCard("Lightning Bolt", 3, "Common", "damage"))
    deck.add_card(
        ArtifactCard("Mana Crystal", 2, "Rare", 5, "+1 mana per turn")
    )

    print("Building deck with different card types...")
    print("Deck stats:", deck.get_deck_stats())
    print()
    print("Drawing and playing cards:")

    game_state = {'mana': 10}
    while True:
        card = deck.draw_card()
        if card is None:
            break
        card_type = card.get_card_info().get('type', 'Unknown')
        print(f"\nDrew: {card.name} ({card_type})")
        print("Play result:", card.play(game_state))

    print()
    print(
        "Polymorphism in action: "
        "Same interface, different card behaviors!"
    )


if __name__ == '__main__':
    main()
