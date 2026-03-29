from ex0.CreatureCard import CreatureCard


def main() -> None:
    print("=== DataDeck card foundation ===")
    print()
    print("Testing abstract base class design:")
    print()

    dragon = CreatureCard("Fire Dragon", 5, "Legendary", 7, 5)
    goblin = CreatureCard("Goblin Warrior", 2, "Common", 2, 1)

    print("CreatureCard info:")
    print(dragon.get_card_info())
    print()

    print("Playing Fire Dragon with 6 mana available:")
    print("Playable:", dragon.is_playable(6))
    print("Play result:", dragon.play({'mana': 6}))
    print()

    print("Fire Dragon attacks Goblin Warrior:")
    print("Attack result:", dragon.attack_target(goblin))
    print()

    print("Testing insufficient mana (3 available):")
    print("Playable:", dragon.is_playable(3))
    print()

    print("Abstract pattern successfully demonstrated!")


if __name__ == '__main__':
    main()
