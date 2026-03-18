import alchemy.elements
from alchemy.elements import create_earth, create_fire, create_water
from alchemy.potions import healing_potion as heal
from alchemy.potions import strength_potion

print("=== Import transmutation mastery ===")

print("\nMethod 1 - Full module import:")
print(f"alchemy.elements.create_fire():"
      f" {alchemy.elements.create_fire()}")

print("\nMethod 2 - Specific function import:")
print(f"create_water(): {create_water()}")

print("\nMethod 3 - Aliased import:")
print(f"heal(): {heal()}")

print("\nMethod 4 - Multiple imports:")
print(f"create_earth(): {create_earth()}")
print(f"create_fire(): {create_fire()}")
print(f"strength_potion(): {strength_potion()}")

print("\nAll import transmutation methods mastered!")
