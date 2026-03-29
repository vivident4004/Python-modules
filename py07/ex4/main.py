from ex4.TournamentCard import TournamentCard
from ex4.TournamentPlatform import TournamentPlatform


def main() -> None:
    print("=== DataDeck tournament platform ===")
    print()

    platform = TournamentPlatform()

    dragon = TournamentCard("Fire Dragon", 5, "Legendary", 7, 4, 1200)
    wizard = TournamentCard("Ice Wizard", 4, "Epic", 5, 6, 1150)

    print("Registering tournament cards...")
    dragon_id = platform.register_card(dragon)
    wizard_id = platform.register_card(wizard)

    for card_id, card in [(dragon_id, dragon), (wizard_id, wizard)]:
        stats = card.get_tournament_stats()
        print(f"{card.name} (ID: {card_id}):")
        print(f"- Interfaces: {stats['interfaces']}")
        print(f"- Rating: {stats['rating']}")
        print(f"- Record: {stats['record']}")
        print()

    print("Creating tournament match...")
    match = platform.create_match(dragon_id, wizard_id)
    print("Match result:", match)
    print()

    print("Tournament leaderboard:")
    for i, entry in enumerate(platform.get_leaderboard(), 1):
        print(
            f"{i}. {entry['name']} - "
            f"Rating: {entry['rating']} ({entry['record']})"
        )
    print()

    print("Platform report:")
    print(platform.generate_tournament_report())
    print()
    print("=== Tournament platform successfully deployed! ===")
    print("All abstract patterns working together harmoniously!")


if __name__ == "__main__":
    main()
