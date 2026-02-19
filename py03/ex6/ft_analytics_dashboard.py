class Player:
    def __init__(self, name, score, active, region):
        self.name = name
        self.score = score
        self.active = active
        self.achievements = {}
        self.region = region


def player_factory() -> list:
    players = [Player('Alice', 2300, True, 'North'),
               Player('Bernardo', 1800, False, 'South'),
               Player('Camilla', 2150, True, 'East'),
               Player('Diego', 2050, True, 'West'),
               Player('Eliana', 420, False, 'East'),
               Player('Francesco', 8, False, 'North')]
    a1 = {'first_kill', 'level_10', 'boss_slayer', 'aldo_moro'}
    a2 = {'level_20', 'brigata_rossa', 'ecoterrorista'}
    a3 = {'level_30', 'miner', 'bombarolo', 'ecoterrorista'}
    a4 = {'aldo_moro', 'dragon_slayer'}
    players[0].achievements = a1
    players[1].achievements = a2
    players[2].achievements = a3
    players[3].achievements = a4
    return players


def ft_analytics_dashboard() -> None:
    print("=== Game analytics dashboard ===\n")

    print("=== List comprehension examples ===")
    players = player_factory()
    print(f"High-scorers (score > 2000): "
          f"{[p.name for p in players if p.score > 2000]}")
    print(f"Every player's scores doubled: {[p.score * 2 for p in players]}")
    print(f"Active players: {[p.name for p in players if p.active]}")

    print("\n=== Dict comprehension examples ===")
    print(f"Active players' scores: "
          f"{ {p.name:p.score for p in players if p.active} }")
    score_names = ['low', 'medium', 'high']
    print(f"Score categories: { {s:i+1 for i, s in enumerate(score_names) } }")
    print(f"Achievement counts: "
          f"{ {p.name:len(p.achievements) for p in players} }")

    print("\n=== Set comprehension examples ==")
    # Duplico gli elementi, cosí dimostro che l'insieme ha solo valori univoci
    players = players * 2
    print(f"Unique players: { {p.name for p in players} }")
    # Comprensione annidata
    print(f"Unique achievements: "
          f"{ {a for p in players for a in p.achievements } }")
    print(f"Regions of active players: "
          f"{ {p.region for p in players if p.active} }")

    print("\n=== Combined analysis ===")
    print(f"Total players: {len(set(players))}")
    print(f"Total unique achievements: "
          f"{ len({a for p in players for a in p.achievements}) }")
    print(f"Average score: "
          f"{sum(p.score for p in set(players)) / len(set(players)):.1f}")
    top = max(set(players), key=lambda p: p.score)
    print(f"Top performer: {top.name} "
          f"({top.score} points, {len(top.achievements)} achievements)")


if __name__ == "__main__":
    ft_analytics_dashboard()
