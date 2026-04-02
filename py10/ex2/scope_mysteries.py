from typing import Any


def mage_counter() -> callable:
    i = 0

    # counter() is a closure
    def counter():
        nonlocal i
        i += 1
        return i
    return counter


def spell_accumulator(initial_power: int) -> callable:
    def accumulator():
        nonlocal initial_power
        initial_power += 1
        return initial_power
    return accumulator


def enchantment_factory(enchantment_type: str) -> callable:
    def factory(item: str) -> str:
        return enchantment_type + " " + item
    return factory


def memory_vault() -> dict[str, callable]:
    dic = dict()

    def store(key: str, value: Any) -> None:
        nonlocal dic
        dic[key] = value

    def recall(key: str) -> Any:
        return dic.get(key, "memory not found")

    return {"store": store, "recall": recall}


def main() -> None:
    print("\nTesting mage counter...")
    c = mage_counter()
    for i in range(1, 4):
        print(f"Call {i}: {c()}")

    print("\nTesting spell accumulator...")
    s = spell_accumulator(41)
    for i in range(1, 4):
        print(f"Call {i}: {s()}")

    print("\nTesting enchantment factory...")
    objects = ["Sword", "Shield", "Topo", "Gigio"]
    f = enchantment_factory("Flaming")
    for bertozz in objects:
        print(f(bertozz))

    print("\nTesting memory vault...")
    m = memory_vault()
    print("Storing 'secret' = 42")
    m["store"]('secret', 42)
    print("Recalling 'secret':", m["recall"]('secret'))
    print("Recalling 'unknown':", m["recall"]('unknown'))


if __name__ == "__main__":
    main()
