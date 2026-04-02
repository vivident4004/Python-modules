import functools
from typing import Callable, Any


def spell_reducer(spells: list[int], operation: str) -> int:
    match operation:
        case "add":
            return functools.reduce(lambda x, y: x+y, spells)
        case "multiply":
            return functools.reduce(lambda x, y: x*y, spells)
        case "min":
            return functools.reduce(lambda x, y: min(x, y), spells)
        case "max":
            return functools.reduce(lambda x, y: max(x, y), spells)
        case _:
            raise ValueError(f"Unknown operation: {operation}")


def partial_enchanter(base_enchantment: Callable) -> dict[str, Callable]:
    fire = functools.partial(base_enchantment, power=50, element="fire")
    water = functools.partial(base_enchantment, power=50, element="water")
    air = functools.partial(base_enchantment, power=50, element="air")
    return {'fire': fire, 'water': water, 'air': air}


@functools.lru_cache
def memoized_fibonacci(n: int) -> int:
    if n < 0:
        raise ValueError("n must be non-negative")
    if n < 2:
        return n
    else:
        return memoized_fibonacci(n-1) + memoized_fibonacci(n-2)


def spell_dispatcher() -> Callable[[Any], str]:
    @functools.singledispatch
    def elabora(arg: Any) -> Any:
        raise TypeError(f"Unknown spell type: {type(arg).__name__}")

    @elabora.register(int)
    def _(damage: int) -> str:
        return f"Damage spell: {damage} damage"

    @elabora.register(str)
    def _(ench: str) -> str:
        return f"Enchantment: {ench}"

    @elabora.register(list)
    def _(multi: list) -> str:
        return f"Multicast: {', '.join(multi)}"

    return elabora


def main() -> None:
    li = [1, 2, 3, 4]
    print("\nTesting spell reducer"
          f"with numbers {li}...")
    print(spell_reducer(li, "add"))
    print(spell_reducer(li, "multiply"))
    print(spell_reducer(li, "min"))
    print(spell_reducer(li, "max"))
    try:
        print(spell_reducer(li, "gigio"))
    except ValueError as e:
        print(e)

    print("\nTesting partial enchanter...")

    def base_enchant(power: int, element: str, target: str) -> str:
        return f"{target} enchanted with {element} and power {power}"
    partials = partial_enchanter(base_enchant)
    for value in partials.values():
        print(value(target="Sword"))

    print("\nTesting memoized Fibonacci...")
    print(f"fib(0) = {memoized_fibonacci(0)}")
    print(f"fib(1) = {memoized_fibonacci(1)}")
    print(f"fib(10) = {memoized_fibonacci(10)}")
    print(f"fib(20) = {memoized_fibonacci(20)}")

    print("\nTesting spell dispatcher...")
    caster = spell_dispatcher()
    print(caster(10))
    print(caster("fireball"))
    print(caster(["topo", "gigio", "pippatore"]))
    try:
        print(caster(42.42))
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
