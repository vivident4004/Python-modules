from ..potions import healing_potion
from .basic import lead_to_gold


def philosophers_stone() -> str:
    lead_to_gold_result = lead_to_gold()
    return (f"Philosopher's stone created using {lead_to_gold_result} "
            f"and {healing_potion()}")


def elixir_of_life() -> str:
    return "Elixir of life: eternal youth achieved!"
