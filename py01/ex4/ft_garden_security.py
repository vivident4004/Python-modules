class SecurePlant:
    def __init__(self, name: str, starting_height: float, days: int) -> None:
        self.name = name
        self.__height = starting_height
        self.__age = days
        print(f'Creata pianta "{self.name}".')

    def __str__(self) -> str:
        return (f"{self.name} (altezza: {self.__height} cm, età {self.__age} "
                f"giorni)")

    def get_height(self) -> float:
        return self.__height

    def get_age(self) -> int:
        print(f"{self.name} ha ora {self.__age} giorni [OK].")
        return self.__age

    def set_height(self, new_height: float) -> None:
        if new_height < 0.0:
            print(f'\nAttenzione: "{new_height}" è invalida come altezza.')
            print("Errore di sicurezza: l'altezza deve essere positiva.")
        else:
            print(f"{self.name} ha una nuova altezza di {new_height} cm [OK].")
            self.__height = new_height

    def set_age(self, new_age: int) -> None:
        if new_age < 0:
            print(f'\nAttenzione: "{new_age}" è invalida come età.')
            print("Errore di sicurezza: l'età dev'essere positiva.")
        else:
            self.__age = new_age


def ft_garden_security() -> None:
    print("=== Sistema di sicurezza del giardino ===")
    plant = SecurePlant("Rosa rubiginosa", 34.2, 42)
    print("Pianta corrente: " + str(plant))
    plant.set_height(25.0)
    plant.set_age(10)
    plant.set_height(-1.0)
    plant.set_age(-42)
    print("Pianta corrente: " + str(plant))


if __name__ == "__main__":
    ft_garden_security()
