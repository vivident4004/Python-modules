def artifact_sorter(artifacts: list[dict]) -> list[dict]:
    return sorted(artifacts, key=lambda artifact: artifact['power'])


def power_filter(mages: list[dict], min_power: int) -> list[dict]:
    return list(filter(lambda artifact: artifact['power'] >= min_power, mages))


def spell_transformer(spells: list[str]) -> list[str]:
    return list(map(lambda spell: "* " + spell + " *", spells))


def mage_stats(mages: list[dict]) -> dict:
    max_power = max(mages, key=lambda artifact: artifact['power'])['power']
    min_power = min(mages, key=lambda artifact: artifact['power'])['power']
    # map() estrae i valori power da ogni dizionario,
    # sum() li somma, len(mages) dà il numero di elementi.
    avg_power = sum(map(lambda artifact: artifact['power'],
                        mages)) / len(mages)
    return {'max_power': max_power, 'min_power': min_power,
            'avg_power': avg_power}


def main() -> None:
    artifacts = [
        {'name': 'Crystal Orb', 'power': 85, 'type': 'orb'},
        {'name': 'Fire Staff', 'power': 92, 'type': 'staff'},
        {'name': 'Shadow Blade', 'power': 60, 'type': 'sword'}
    ]
    print("Testing artifact sorter...")
    sorted_artifacts = artifact_sorter(artifacts)
    print(f"{sorted_artifacts[0]['name']} "
          f"({sorted_artifacts[0]['power']} power)"
          f" comes before {sorted_artifacts[1]['name']} "
          f"({sorted_artifacts[1]['power']} power)")

    mages = [
        {'name': 'Gandalf', 'power': 95, 'element': 'light'},
        {'name': 'Merlin', 'power': 85, 'element': 'arcane'},
        {'name': 'Saruman', 'power': 70, 'element': 'shadow'}
    ]
    print("\nTesting power filter...")
    powerful_mages = power_filter(mages, 80)
    print("Mages with power >= 80:", [m['name'] for m in powerful_mages])

    spells = ['fireball', 'heal', 'shield']
    print("\nTesting spell transformer...")
    print(*spell_transformer(spells))

    print("\nTesting mage stats...")
    stats = mage_stats(mages)
    print(f"Max: {stats['max_power']}, min: {stats['min_power']}, "
          f"avg: {stats['avg_power']}")


if __name__ == "__main__":
    main()
