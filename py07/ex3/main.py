from ex3.FantasyCardFactory import FantasyCardFactory
from ex3.AggressiveStrategy import AggressiveStrategy
from ex3.GameEngine import GameEngine


def main() -> None:
    print("=== DataDeck game engine ===")
    print()

    factory = FantasyCardFactory()
    strategy = AggressiveStrategy()
    engine = GameEngine()

    print("Configuring fantasy card game...")
    print("Factory: FantasyCardFactory")
    print("Strategy: AggressiveStrategy")
    print("Available types:", factory.get_supported_types())
    print()

    engine.configure_engine(factory, strategy)

    print("Simulating aggressive turn...")
    turn = engine.simulate_turn()

    print("Hand:", turn['hand'])
    print()
    print("Turn execution:")
    print("Strategy:", turn['strategy'])
    print("Actions:", turn['actions'])
    print()
    print("Game Report:")
    print(engine.get_engine_status())
    print()
    print(
        "Abstract factory + strategy pattern: "
        "Maximum flexibility achieved!"
    )


if __name__ == '__main__':
    main()
