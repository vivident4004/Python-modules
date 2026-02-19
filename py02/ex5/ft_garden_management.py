class GardenError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class PlantError(GardenError):
    def __init__(self, plant: str, message: str) -> None:
        self.message = f"Error checking {plant}: {message}"
        super().__init__(self.message)


class WaterError(GardenError):
    def __init__(self, message: str = "Not enough water in tank") -> None:
        self.message = message
        super().__init__(self.message)


class GardenManager:
    def __init__(self) -> None:
        self.plants = []

    def add_plant(self, plant_name: str) -> None:
        try:
            if not plant_name:
                # Raise internal error to be caught immediately
                raise ValueError("Plant name cannot be empty!")

            self.plants.append(plant_name)
            print(f"Added {plant_name} successfully")

        except ValueError as e:
            print(f"Error adding plant: {e}")

    def water_plants(self) -> None:
        print("Opening watering system")
        try:
            for plant in self.plants:
                print(f"Watering {plant} - success")
        except Exception as e:
            print(f"Watering error: {e}")
        finally:
            print("Closing watering system (cleanup)")

    @staticmethod
    def check_plant_health(plant_name: str,
                           water_level: int,
                           sunlight_hours: int) -> None:
        try:
            wl = int(water_level)
            sh = int(sunlight_hours)
        except ValueError:
            raise PlantError(plant_name, "Values must be integers")

        if wl < 1:
            raise PlantError(plant_name,
                             f"Water level {wl} is too low (min 1)")
        if wl > 10:
            raise PlantError(plant_name,
                             f"Water level {wl} is too high (max 10)")

        if sh < 2:
            raise PlantError(plant_name, f"Sunlight {sh} is too low (min 2)")
        if sh > 12:
            raise PlantError(plant_name, f"Sunlight {sh} is too high (max 12)")

        print(f"{plant_name}: healthy (water: {wl}, sun: {sh})")


def test_garden_management() -> None:
    print("=== Garden management system ===")
    manager = GardenManager()

    print("Adding plants to garden...")
    manager.add_plant("tomato")
    manager.add_plant("lettuce")
    manager.add_plant("")

    print("Watering plants...")
    manager.water_plants()

    print("Checking plant health...")

    try:
        manager.check_plant_health("tomato", 5, 8,)
    except GardenError as e:
        print(e)

    try:
        manager.check_plant_health("lettuce", 15, 8)
    except GardenError as e:
        print(e)

    print("Testing error recovery...")
    try:
        raise WaterError("Not enough water in tank")
    except GardenError as e:
        print(f"Caught GardenError: {e}")

    print("System recovered and continuing...")
    print("Garden management system test complete!")


if __name__ == "__main__":
    test_garden_management()
