def check_plant_health(plant_name: str,
                       water_level: int,
                       sunlight_hours: int) -> None:
    try:
        wl = int(water_level)
    except ValueError as e:
        raise ValueError(e)
    try:
        sh = int(sunlight_hours)
    except ValueError as e:
        raise ValueError(e)
    if plant_name is None or len(plant_name) == 0:
        raise ValueError('plant name cannot be empty!')
    if wl < 1:
        raise ValueError(f'water level {water_level} is too low (min 1)')
    if wl > 10:
        raise ValueError(f'water level {water_level} is too high (max 10)')
    if sh < 2:
        raise ValueError(f'the number of sunlight hours '
                         f'({sunlight_hours}) is too low (min 2)')
    if sh > 12:
        raise ValueError(f'the number of sunlight hours '
                         f'({sunlight_hours}) is too high (max 12)')
    print(f"Plant '{plant_name}' is healthy!")


def test_plant_checks() -> None:
    print("=== Garden plant health checker ===")
    print("\nTesting good values...")
    try:
        check_plant_health('Ocimum basilicum', 10, 12)
    except ValueError as e:
        print(f"Error: {e}")
    print("\nTesting empty plant name...")
    try:
        check_plant_health('', 10, 0)
    except ValueError as e:
        print(f"Error: {e}")
    print("\nTesting bad water level...")
    try:
        check_plant_health("Plant", 42, 0)
    except ValueError as e:
        print(f"Error: {e}")
    print("\nTesting bad sunlight hours...")
    try:
        check_plant_health("Plant", 3, 0)
    except ValueError as e:
        print(f"Error: {e}")
    print("\nAll error raising tests completed!")


if __name__ == '__main__':
    test_plant_checks()
