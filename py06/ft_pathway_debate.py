import alchemy.transmutation


def main() -> None:
    print("=== Pathway debate mastery ===")
    print("\nTesting absolute imports (from basic.py):")
    print(f"lead_to_gold(): {alchemy.transmutation.lead_to_gold()}")
    print(f"stone_to_gem(): {alchemy.transmutation.stone_to_gem()}")

    print("\nTesting relative imports (from advanced.py):")
    print(f"philosophers_stone(): "
          f"{alchemy.transmutation.philosophers_stone()}")
    print(f"elixir_of_life(): {alchemy.transmutation.elixir_of_life()}")

    print("\nTesting package access:")
    print(f"alchemy.transmutation.lead_to_gold(): "
          f"{alchemy.transmutation.lead_to_gold()}")
    print(f"alchemy.transmutation.philosophers_stone(): "
          f"{alchemy.transmutation.philosophers_stone()}")

    print("\nBoth pathways work! Absolute: clear, relative: concise")


if __name__ == "__main__":
    main()
