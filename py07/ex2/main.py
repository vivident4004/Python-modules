from ex2.EliteCard import EliteCard


def main() -> None:
    print("=== DataDeck ability system ===")
    print()

    warrior = EliteCard("Arcane Warrior", 6, "Legendary", 5, 3, 4)

    print("EliteCard capabilities:")
    print("- Card: ['play', 'get_card_info', 'is_playable']")
    print("- Combatable: ['attack', 'defend', 'get_combat_stats']")
    print("- Magical: ['cast_spell', 'channel_mana', 'get_magic_stats']")
    print()

    print("Playing Arcane Warrior (elite card):")
    print()

    print("Combat phase:")
    print("Attack result:", warrior.attack("Enemy"))
    print("Defense result:", warrior.defend(5))
    print()

    print("Magic phase:")
    print("Spell cast:", warrior.cast_spell("Fireball", ["Enemy1", "Enemy2"]))
    print("Mana channel:", warrior.channel_mana(3))
    print()

    print("Multiple interface implementation successful!")


if __name__ == '__main__':
    main()
