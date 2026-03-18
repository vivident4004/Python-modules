from .elements import create_air, create_earth, create_fire, create_water


def healing_potion() -> str:
    fire_result = create_fire()
    water_result = create_water()
    return f"Healing potion brewed with {fire_result} and {water_result}"


def strength_potion() -> str:
    earth_result = create_earth()
    fire_result = create_fire()
    return f"Strength potion brewed with {earth_result} and {fire_result}"


def invisibility_potion() -> str:
    air_result = create_air()
    water_result = create_water()
    return f"Invisibility potion brewed with {air_result} and {water_result}"


def wisdom_potion() -> str:
    fire_result = create_fire()
    water_result = create_water()
    earth_result = create_earth()
    air_result = create_air()
    all_four_results = (f"{fire_result}, {water_result}, {earth_result},"
                        f" and {air_result}")
    return f"Wisdom potion brewed with all elements: {all_four_results}"
