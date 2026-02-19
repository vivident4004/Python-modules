class Player:
    def __init__(self, name):
        self.name = name
        self.achievements = set()


def player_factory(*args) -> list[Player]:
    player_list = []
    a = args[0]
    b = args[1]
    c = args[2]
    a.achievements.add('first_kill')
    a.achievements.add('level_10')
    a.achievements.add('speed_demon')
    a.achievements.add('treasure_hunter')
    b.achievements.add('first_kill')
    b.achievements.add('level_10')
    b.achievements.add('boss_slayer')
    b.achievements.add('collector')
    c.achievements.add('level_10')
    c.achievements.add('treasure_hunter')
    c.achievements.add('boss_slayer')
    c.achievements.add('speed_demon')
    c.achievements.add('perfectionist')
    player_list.append(a)
    player_list.append(b)
    player_list.append(c)
    return player_list


def ft_achievement_tracker() -> None:
    print("=== Achievement tracker system ===")
    a, b, c = Player("Alice"), Player("Bob"), Player("Charlie")
    player_list = player_factory(a, b, c)
    for player in player_list:
        print(f"{player.name}'s achievements: {player.achievements}")

    print("=== Achievement analytics ===")
    unione = (a.achievements |
              b.achievements |
              c.achievements)
    print(f"Unique achievements: {unione}")
    print("Total unique achievements: ", len(unione))

    intersezione = (a.achievements &
                    b.achievements &
                    c.achievements)
    print(f"\nCommon to all players: {intersezione}")

    rari = ((a.achievements ^ (b.achievements | c.achievements)) &
            (b.achievements ^ (c.achievements | a.achievements)) &
            (c.achievements ^ (a.achievements | b.achievements)))
    print(f"Rarity achievements: {rari}")

    print("\nIn common between Alice and Bob: ",
          a.achievements & b.achievements)
    print("Alice's unique achievements: ", a.achievements - b.achievements)
    print("Bob's unique achievements: ", b.achievements - a.achievements)


if __name__ == "__main__":
    ft_achievement_tracker()
