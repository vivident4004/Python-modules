class Plant:
    def __init__(self, name: str, height: float, days: int) -> None:
        self.name = name
        self.height = height
        self.days = days

    def __str__(self) -> str:
        return (f"{self.name} ({self.__class__.__name__}): {self.height} cm, "
                f"{self.days} giorni")


class Flower(Plant):
    def __init__(self, name: str,
                 height: float,
                 days: int,
                 colour: str) -> None:
        super().__init__(name, height, days)
        self.colour = colour

    def __str__(self) -> str:
        return (super().__str__() + f", colore {self.colour}.")

    def bloom(self) -> None:
        print(self.name + " sta sbocciando!")


class Tree(Plant):
    def __init__(self, name: str,
                 height: float,
                 days: int,
                 trunk_diameter: float) -> None:
        super().__init__(name, height, days)
        self.trunk_diameter = trunk_diameter

    def __str__(self) -> str:
        return (super().__str__()
                + f", diametro tronco: {self.trunk_diameter} cm.")

    def produce_shade(self) -> None:
        print(self.name + " produce 78 m" + '\u00B2' + " d'ombra.")


class Vegetable(Plant):
    def __init__(self, name: str,
                 height: float,
                 days: int,
                 harvest_season: str,
                 nutritional_value: str) -> None:
        super().__init__(name, height, days)
        self.season = harvest_season
        self.nutritional_value = nutritional_value

    def __str__(self) -> str:
        return (super().__str__() + f", periodo di raccolta: {self.season}.")

    def print_nutritional_value(self):
        print(f"{self.name} ha molta {self.nutritional_value}.")


def ft_plant_types() -> None:
    rosa = Flower("Rosa rubiginosa", 34.2, 42, "rosa")
    iris = Flower("Iris florentina", 23.6, 14, "viola")
    tiglio = Tree("Tilia japonica", 1542, 20561, 55.4)
    quercia = Tree("Quercus robur", 3000, 101325, 121.1)
    pomodoro = Vegetable("Solanum lycopersicum", 132, 100,
                         "estate", "vitamina C")
    melanzana = Vegetable("Solanum melongena", 78, 69,
                          "estate", "tiamina")
    basilico = Vegetable("Ocimum basilicum", 1.5, 10,
                         "primavera", "vitamina K")
    plants = [rosa, iris, tiglio, quercia, pomodoro, melanzana, basilico]

    print("--- Tipi di piance nel giarino ---")
    for plant in plants:
        print(plant)
        if plant.__class__.__name__ == "Flower":
            plant.bloom()
        if plant.__class__.__name__ == "Tree":
            plant.produce_shade()
        if plant.__class__.__name__ == "Vegetable":
            plant.print_nutritional_value()
        print()


if __name__ == "__main__":
    ft_plant_types()
