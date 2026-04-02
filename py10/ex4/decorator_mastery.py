import random
import time
from functools import wraps
from typing import Callable, Any


def spell_timer(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args: Any, **kwargs) -> Any:
        start = time.time()
        time.sleep(random.random())
        print(f"Casting {func.__name__}...")
        a = func(*args, **kwargs)
        print(f"Spell completed in {time.time() - start:.3f} seconds")
        return a
    return wrapper


def power_validator(min_power: int) -> Callable:
    def f(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            p = kwargs.get('power', args[-1])
            if p >= min_power:
                return func(args[0], **kwargs)
            return "Insufficient power for this spell"
        return wrapper
    return f


def retry_spell(max_attempts: int) -> Callable:
    def f(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            att = 1
            while att <= max_attempts:
                try:
                    return func(args[0], **kwargs)
                except Exception:
                    print("Spell failed, retrying... (attempt "
                          f"{att}/{max_attempts})")
                    att += 1
            return f"Spell casting failed after {max_attempts} attempts"
        return wrapper
    return f


class MageGuild:
    def __init__(self, name: str):
        self.name = name

    @staticmethod
    def validate_mage_name(name: str) -> bool:
        if len(name) < 3:
            # raise ValueError("Mage name must be at least 3 characters long")
            return False
        return all(c.isalpha() or c.isspace() for c in name)

    @power_validator(min_power=10)
    def cast_spell(self, spell_name: str, power: int) -> str:
        return f"Successfully cast {spell_name} with {power} power"


@spell_timer
def fireball(nome):
    print(f"Result: {nome}!")


@power_validator(min_power=42)
def power(min_power: int):
    return f"Power: {min_power}"


@retry_spell(max_attempts=5)
def pippo(i: int) -> str:
    if i % 4 == 0:
        raise ValueError
    if i == 1:
        return f"Pippo {i} grammo di coca"
    return f"Pippo {i} grammi di coca"


def main() -> None:
    print("\nTesting spell timer...")
    fireball("t_vanni")
    fireball("f.bertozz()")

    a = random.randint(0, 100)
    print(f"\nTesting power validator with power {a}...")
    print(power(a))

    print("\nTesting retry_spell...")
    for i in range(5):
        print(pippo(i))

    print("\nTesting MageGuild...")
    mage1 = MageGuild("t_vanni")
    print(f"Testing validate_name with {mage1.name}...")
    print(MageGuild.validate_mage_name(mage1.name))
    mage2 = MageGuild("f.bertozz")
    print(f"Testing validate_name with {mage2.name}...")
    print(MageGuild.validate_mage_name(mage2.name))
    mage3 = MageGuild("giusto")
    print(f"Testing validate_name with {mage3.name}...")
    print(MageGuild.validate_mage_name(mage3.name))
    guild = MageGuild("guild")
    print(guild.cast_spell(spell_name="Lightning", power=15))
    print(guild.cast_spell(spell_name="Lightning", power=4))


if __name__ == "__main__":
    main()
