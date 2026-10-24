"""Discover the power of __init__.py.

The sacred scroll that transforms ordinary folders into magical Python packages
"""

import alchemy


def main() -> None:
    print("=== Sacred scroll mastery ===")
    print("\nTesting direct module access:")
    print("alchemy.elements.create_fire():", alchemy.elements.create_fire())
    print("alchemy.elements.create_water():", alchemy.elements.create_water())
    print("alchemy.elements.create_earth():", alchemy.elements.create_earth())
    print("alchemy.elements.create_air():", alchemy.elements.create_air())

    print("\nTesting package-level access (controlled by __init__.py):")
    try:
        print("alchemy.create_fire(): ", end="")
        print(alchemy.create_fire())
    except AttributeError:
        print("AttributeError - not exposed")
    try:
        print("alchemy.create_water(): ", end="")
        print(alchemy.create_water())
    except AttributeError:
        print("AttributeError - not exposed")
    try:
        print("alchemy.create_earth(): ", end="")
        print(alchemy.create_earth())  # ty:ignore[unresolved-attribute]
    except AttributeError:
        print("AttributeError - not exposed")
    try:
        print("alchemy.create_air(): ", end="")
        print(alchemy.create_air())  # ty:ignore[unresolved-attribute]
    except AttributeError:
        print("AttributeError - not exposed")

    print()
    alchemy.print_metadata()


if __name__ == "__main__":
    main()
