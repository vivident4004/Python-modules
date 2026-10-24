import sys


class Inventory:
    def __init__(self, inventory_dict: dict) -> None:
        self.inventory = inventory_dict
        self.total_items = sum(inventory_dict.values())
        self.unique_items = len(inventory_dict.keys())

    def print_keys(self) -> None:
        print("=== Current inventory ===")
        for key, value in self.inventory.items():
            print(f"{key}: {value} units "
                  f"({value / self.total_items * 100:.1f}%)")

    def print_stats(self) -> None:
        print("=== Current statistics ===")
        max_key, max_value = max(self.inventory.items(), key=lambda x: x[1])
        min_key, min_value = (min(self.inventory, key=self.inventory.get),
                              min(self.inventory.values()))
        print(f"Most abundant: {max_key} ({max_value} units)")
        print(f"Least abundant: {min_key} ({min_value} units)")

    def item_categories(self) -> None:
        print("=== Item categories ===")
        abundant = {k: self.inventory[k] for k in self.inventory
                    if self.inventory[k] > 5}
        if abundant:
            print(f"Abundant: {abundant}")
        moderate = {k: self.inventory[k] for k in self.inventory
                    if 4 <= self.inventory[k] <= 5}
        if moderate:
            print(f"Moderate: {moderate}")
        scarce = {k: self.inventory[k] for k in self.inventory
                  if self.inventory[k] <= 4}
        if scarce:
            print(f"Scarce: {scarce}")

    def management_suggestion(self) -> None:
        print("=== Management suggestion ===")
        restock = [k for k in self.inventory if self.inventory[k] < 2]
        if restock:
            print(f"Restock needed for: {restock}")
        else:
            print("No restock needed, inventory looking good!")

    def print_properties(self) -> None:
        print("=== Dictionary properties demo ===")
        print("Dictionary keys:", ', '.join(list(self.inventory.keys())))
        print(f"Dictionary values: {list(self.inventory.values())}")
        print(f"Simple lookup: 'sword' in inventory = "
              f"{'sword' in self.inventory}")


def ft_inventory_system() -> None:
    print("=== Inventory system analysis ===")
    inv = {arg.split(':')[0]: int(arg.split(':')[1]) for arg in sys.argv[1:]}
    inventory = Inventory(inv)
    print(f"Total items in inventory: {inventory.total_items}")
    print(f"Unique items in inventory: {inventory.unique_items}")
    print()
    inventory.print_keys()
    print()
    inventory.print_stats()
    print()
    inventory.item_categories()
    print()
    inventory.management_suggestion()
    print()
    inventory.print_properties()


if __name__ == "__main__":
    ft_inventory_system()
