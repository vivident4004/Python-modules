class NonePlantError(Exception):
    def __init__(self, message) -> None:
        self.message = "Cannot water None - invalid plant!"
        super().__init__(self.message)


def water_plants(plant_list: list) -> None:
    print("Opening watering system")
    plant = None
    try:
        for plant in plant_list:
            if plant is None:
                raise NonePlantError(plant)
            print(f"Watering {plant}")
    except NonePlantError as e:
        print(f"Error: {e}")
    finally:
        print("Closing watering system")


def test_watering_system() -> None:
    print("=== Garden watering system ===\n")
    print("Testing normal watering system...")
    water_plants(["Rosa rubiginosa", "Iris florentina",
                  "Tilia japonica", "Ocimum basilicum"])
    print("Watering completed successfully!\n")

    print("Testing watering system with error...")
    water_plants(["Rosa rubiginosa", "Iris florentina",
                  None, "Ocimum basilicum"])
    print("\nCleanup always happens, even with errors!")


if __name__ == "__main__":
    test_watering_system()
