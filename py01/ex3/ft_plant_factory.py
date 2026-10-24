class Plant:
    def __init__(self, name: str, height: float, days: int,) -> None:
        self.name = name
        self.height = height
        self.age = days

    def __str__(self) -> str:
        return (f"{self.name} (altezza: {self.height} cm, età {self.age} "
                f"giorni)")


def ft_plant_factory() -> None:
    plant_data = [
        ("Rosa rubiginosa", 23.4, 17),
        ("Iris florentina", 42.7, 12),
        ("Lilium candidum", 10.9, 55),
        ("Tulipa clusiana", 25.0, 42),
        ("Iris versicolor", 38.3, 3)
    ]
    garden = []
    print("--- Inizializzazione del giardino ---")
    for plant in plant_data:
        new_plant = Plant(*plant)
        garden.append(new_plant)
        print(f"Aggiunta {new_plant} al giardino.")
    print(f"Totale piante: {len(garden)}")


if __name__ == "__main__":
    ft_plant_factory()
