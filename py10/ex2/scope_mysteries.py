from collections.abc import Callable
from typing import Any


def mage_counter() -> Callable:
    i = 0

    def counter() -> int:
        nonlocal i
        i += 1
        return i
    return counter


def spell_accumulator(initial_power: int) -> Callable:
    total = initial_power

    def accumulator(amount: int) -> int:
        nonlocal total
        total += amount
        return total
    return accumulator


def enchantment_factory(enchantment_type: str) -> Callable:
    def factory(item: str) -> str:
        return enchantment_type + " " + item
    return factory


def memory_vault() -> dict[str, Callable]:
    dic: dict = {}

    def store(key: str, value: Any) -> None:
        dic[key] = value

    def recall(key: str) -> Any:
        return dic.get(key, "memory not found")

    return {"store": store, "recall": recall}


def main() -> None:
    print("\nTesting mage counter...")
    counter_a = mage_counter()
    counter_b = mage_counter()
    print(f"counter_a call 1: {counter_a()}")
    print(f"counter_a call 2: {counter_a()}")
    print(f"counter_b call 1: {counter_b()}")

    print("\nTesting spell accumulator...")
    s = spell_accumulator(100)
    print(f"Base 100, add 20: {s(20)}")

    print("\nTesting enchantment factory...")
    flaming = enchantment_factory("Flaming")
    frozen = enchantment_factory("Frozen")
    print(flaming("Sword"))
    print(frozen("Shield"))

    print("\nTesting memory vault...")
    m = memory_vault()
    print("Store 'secret' = 42")
    m["store"]('secret', 42)
    print("Recall 'secret':", m["recall"]('secret'))
    print("Recall 'unknown':", m["recall"]('unknown'))


if __name__ == "__main__":
    main()
