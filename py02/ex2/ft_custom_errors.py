class GardenError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class PlantError(GardenError):
    def __init__(self, plant: str,
                 message: str = "Il messaggio è opzionale") -> None:
        self.message = message
        if plant:
            self.message = f"The {plant} plant is wilting!"
        super().__init__(self.message)


class WaterError(GardenError):
    def __init__(self, message: str = "Not enough water in the tank!") -> None:
        self.message = message
        super().__init__(self.message)


def ft_custom_errors() -> None:
    print("=== Custom garden errors demo ===")
    # 1. PlantError
    print("\nTesting PlantError...")
    try:
        raise PlantError("Iris florentina", "PlantError")
    except PlantError as e:
        print(f"Caught PlantError: {e}")
    print("\nTesting WaterError...")
    try:
        raise WaterError()
    except WaterError as e:
        print(f"Caught WaterError: {e}")
    print("\nTesting catching all garden errors...")
    try:
        raise PlantError(plant="tomato")
    except GardenError as e:
        print(f"Caught a garden error: {e}")
    try:
        raise WaterError()
    except GardenError as e:
        print(f"Caught a garden error: {e}")


if __name__ == "__main__":
    ft_custom_errors()
