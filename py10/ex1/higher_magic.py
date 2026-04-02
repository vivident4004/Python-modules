import random
from collections.abc import Callable
from typing import Any


def spell_combiner(spell1: Callable, spell2: Callable) -> Callable:
    def combined(spell: str) -> tuple[str, str]:
        return str(spell1(spell)), str(spell2(spell))
    return combined


def power_amplifier(base_spell: Callable, multiplier: int) -> Callable:
    def mult(*args: Any, **kwargs: Any) -> int:
        return multiplier * base_spell(*args, **kwargs)
    return mult


def conditional_caster(condition: Callable, spell: Callable) -> Callable:
    def caster(*args: Any, **kwargs: Any) -> str:
        return spell(*args, **kwargs) if condition() else "Spell fizzled"
    return caster


def spell_sequence(spells: list[Callable]) -> Callable:
    def cast_all(*args: Any, **kwargs: Any) -> list:
        return [spell(*args, **kwargs) for spell in spells]
    return cast_all


def main() -> None:
    def fireball(stringa: str) -> str:
        return f"Fireball hits {stringa}"

    def healer(stringa: str) -> str:
        return f"Heals {stringa}"

    print("\nTesting spell combiner")
    print(spell_combiner(fireball, healer)("Dragon"))

    def power(*args: Any, **kwargs: Any) -> int:
        return 42

    print("\nTesting power amplifier")
    print(f"Original: {power()}, amplified: "
          f"{power_amplifier(power, 3)()}")

    def verificatore() -> bool:
        return random.randint(0, 1) == 1

    print("\nTesting conditional caster")
    print(conditional_caster(verificatore, fireball)("Dragon"))

    print("\nTesting spell sequence")
    print(spell_sequence([fireball, healer])("Dragon"))


if __name__ == "__main__":
    main()
