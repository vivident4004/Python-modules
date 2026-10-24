class Plant:
    def __init__(self, name: str, height: int) -> None:
        self.name = name
        self.height = height

    def grow(self) -> None:
        self.height += 1
        print(f"{self.name} grew 1cm")

    def describe(self) -> str:
        return f"- {self.name}: {self.height}cm"


class FloweringPlant(Plant):
    def __init__(self, name: str, height: int, colour: str) -> None:
        super().__init__(name, height)
        self.flower_color = colour
        self.is_blooming = True

    def describe(self) -> str:
        blooming = "blooming" if self.is_blooming else "not blooming"
        return (f"- {self.name}: {self.height}cm, "
                f"{self.flower_color} flowers ({blooming})")


class PrizeFlower(FloweringPlant):
    def __init__(self, name: str,
                 height: int,
                 colour: str,
                 prize_points: int) -> None:
        super().__init__(name, height, colour)
        self.prize_points = prize_points

    def describe(self) -> str:
        blooming = "blooming" if self.is_blooming else "not blooming"
        return (
            f"- {self.name}: {self.height}cm, "
            f"{self.flower_color} flowers ({blooming}), "
            f"prize points: {self.prize_points}"
        )


class Garden:
    def __init__(self, owner: str) -> None:
        self.owner = owner
        self.plants = []
        self.plants_added = 0
        self.total_growth = 0

    def add_plant(self, plant: Plant) -> None:
        self.plants.append(plant)
        self.plants_added += 1
        print(f"Added {plant.name} to {self.owner}'s garden")

    def help_grow_all(self) -> None:
        print(f"{self.owner} is helping all plants grow...")
        for plant in self.plants:
            before = plant.height
            plant.grow()
            self.total_growth += (plant.height - before)

    def report(self, stats_helper) -> None:
        print(f"=== {self.owner}'s garden report ===")
        print("Plants in garden:")
        for plant in self.plants:
            print(plant.describe())
        regular, flowering, prize = stats_helper.count_plant_types(self.plants)
        print(f"Plants added: {self.plants_added}, "
              f"total growth: {self.total_growth}cm")
        print(f"Plant types: {regular} regular, {flowering} "
              f"flowering, {prize} prize flowers")


class GardenManager:
    class GardenStats:
        @staticmethod
        def count_plant_types(plants) -> tuple:
            regular = 0
            flowering = 0
            prize = 0
            for plant in plants:
                t = plant.__class__.__name__
                if t == "PrizeFlower":
                    prize += 1
                elif t == "FloweringPlant":
                    flowering += 1
                else:
                    regular += 1
            return regular, flowering, prize

        @staticmethod
        def total_height(plants) -> int:
            total = 0
            for plant in plants:
                total += plant.height
            return total

    def __init__(self) -> None:
        self.gardens = []
        self.stats = GardenManager.GardenStats()

    def add_garden(self, garden: Garden) -> None:
        self.gardens.append(garden)

    @classmethod
    def create_garden_network(cls):
        manager = cls()
        return manager

    @staticmethod
    def is_valid_height(height: int) -> bool:
        return height >= 0

    @staticmethod
    def validate_garden_heights(garden: Garden) -> bool:
        for plant in garden.plants:
            if not GardenManager.is_valid_height(plant.height):
                return False
        return True

    @staticmethod
    def compute_garden_score(garden: Garden) -> int:
        total_height = 0
        flowering_count = 0
        prize_count = 0
        prize_points = 0

        for plant in garden.plants:
            total_height += plant.height
            t = plant.__class__.__name__
            if t == "PrizeFlower":
                prize_count += 1
                prize_points += plant.prize_points
            elif t == "FloweringPlant":
                flowering_count += 1

        # Punteggio: altezza + punti premio + bonus per categorie
        return (total_height +
                prize_points +
                (flowering_count * 10) +
                (prize_count * 20))

    def total_gardens_managed(self) -> int:
        count = 0
        for _ in self.gardens:
            count += 1
        return count


def ft_garden_analytics() -> None:
    print("=== Garden management system demo ===")

    manager = GardenManager.create_garden_network()

    alice_garden = Garden("Alice")
    bob_garden = Garden("Bob")

    manager.add_garden(alice_garden)
    manager.add_garden(bob_garden)

    oak = Plant("Oak Tree", 100)
    rose = FloweringPlant("Rose", 25, "red")
    sunflower = PrizeFlower("Sunflower", 50, "yellow", 10)

    alice_garden.add_plant(oak)
    alice_garden.add_plant(rose)
    alice_garden.add_plant(sunflower)

    alice_garden.help_grow_all()

    alice_garden.report(manager.stats)

    height_validation = GardenManager.validate_garden_heights(alice_garden)
    print(f"Height validation test: {height_validation}")

    bob_garden.add_plant(Plant("Cactus", 30))
    bob_garden.add_plant(Plant("Pine", 62))
    bob_garden.add_plant(PrizeFlower("Iris florentina", 23, "viola", 42))
    bob_garden.report(manager.stats)

    alice_score = GardenManager.compute_garden_score(alice_garden)
    bob_score = GardenManager.compute_garden_score(bob_garden)
    print(f"Garden scores: Alice = {alice_score}, Bob = {bob_score}")
    print(f"Total gardens managed: {manager.total_gardens_managed()}")


if __name__ == "__main__":
    ft_garden_analytics()
