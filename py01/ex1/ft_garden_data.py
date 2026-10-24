class Plant:
    def __init__(self, name: str, height: float, age: int) -> None:
        self.name = name
        self.height = height
        self.age = age

    def info(self) -> None:
        print(f"{self.name}: altezza = {self.height} cm, "
              f"età = {self.age} giorni")


def ft_garden_data() -> None:
    rosa = Plant("Rosa rubiginosa", 34.2, 42)
    iris = Plant("Iris florentina", 23.6, 14)
    giglio = Plant("Lilium candidum", 22.1, 27)
    rosa.info()
    iris.info()
    giglio.info()


if __name__ == "__main__":
    ft_garden_data()
