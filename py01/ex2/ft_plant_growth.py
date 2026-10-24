class Plant:
    def __init__(self, name: str, height: float, days: int,
                 water_reserve: int = 5) -> None:
        self.name = name
        self.height = height
        self.days = days
        self.water_reserve = water_reserve

    def get_info(self) -> None:
        print(f"{self.name}: altezza = {self.height} cm, "
              f"età = {self.days} giorni")

    def grow(self) -> None:
        self.height += 1

    def age(self) -> None:
        self.days += 1
        self.water_reserve -= 1

    # def __del__(self):
    #     print(f"{self.name} è morta.")


def ft_plant_growth() -> None:
    rosa = Plant("Rosa rubiginosa", 34.2, 42, 10)
    iris = Plant("Iris florentina", 23.6, 14, 3)
    giglio = Plant("Lilium candidum", 22.1, 27, 1)
    plants = [rosa, iris, giglio]
    for plant in plants:
        plant.get_info()
    for day in range(7):
        print("Giorno " + str(day + 1))
        for plant in plants:
            plant.age()
            plant.grow()
            if plant.water_reserve <= 2:
                print(f"Annaffia {plant.name}!")
            if plant.water_reserve == 0:
                plants.remove(plant)
                print(f"{plant.name} è morta.")
            if iris.water_reserve < 2:
                iris.water_reserve += 5
                print(f"Annaffiato {iris.name} con 5 unità d'acqua.")
    for plant in plants:
        plant.get_info()
    print("Le piante sono cresciute di 7 cm")


if __name__ == "__main__":
    ft_plant_growth()
