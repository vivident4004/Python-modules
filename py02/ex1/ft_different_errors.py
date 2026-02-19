def garden_operations(action: str, data: str) -> None:
    """
    Esegue operazioni basate su 'action' usando 'data'.
    Non ritorna nulla, serve solo a scatenare eccezioni o eseguire side-effect.
    """

    if action == "convert":
        int(data)

    elif action == "divide":
        _ = 42 / int(data)

    elif action == "open_file":
        f = open(data, "r")
        f.close()

    elif action == "get_item":
        inventory = {"ciao": 42, "mondo": 69}
        _ = inventory[data]


def test_error_types() -> None:
    print("=== Garden error types demo ===")

    # 1. ValueError
    print("\nTesting ValueError...")
    try:
        garden_operations("convert", "non_sono_un_numero")
    except ValueError as e:
        print(f"Caught ValueError: {e}")

    # 2. ZeroDivisionError
    print("\nTesting ZeroDivisionError...")
    try:
        garden_operations("divide", "0")
    except ZeroDivisionError as e:
        print(f"Caught ZeroDivisionError: {e}")

    # 3. FileNotFoundError
    print("\nTesting FileNotFoundError...")
    try:
        garden_operations("open_file", "pianta_inesistente.txt")
    except FileNotFoundError as e:
        print(f"Caught FileNotFoundError: {e}")

    # 4. KeyError
    print("\nTesting KeyError...")
    try:
        garden_operations("get_item", "tractor")
    except KeyError as e:
        print(f"Caught KeyError: {e}")

    # 5. Multiple errors
    print("\nTesting multiple errors together...")
    try:
        # Riprovo l'errore del file, ma catturato dal blocco multiplo
        garden_operations("open_file", "ghost_file.txt")
    except (ValueError, ZeroDivisionError, FileNotFoundError, KeyError) as e:
        print(f"Caught an error, but program continues! Details: {e}")

    print("\nAll error types tested successfully!")


if __name__ == "__main__":
    test_error_types()
