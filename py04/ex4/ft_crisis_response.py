def ft_crisis_response() -> None:
    print("=== CYBERARCHIVES - CRISIS RESPONSE SYSTEM ===")
    print("CRISIS ALERT: attempting access to 'lost_archive.txt'...")
    try:
        with open("lost_archive.txt", 'r') as file:
            print(file.read())
        print("STATUS: normal operations resumed")
    except (FileNotFoundError, PermissionError) as e:
        if e.__class__.__name__ == "FileNotFoundError":
            print("RESPONSE: archive not found in system matrix")
            print("STATUS: crisis handled, system stable")
        if e.__class__.__name__ == "PermissionError":
            print("RESPONSE: security protocols deny access")
            print("STATUS: crisis handled, security maintained")

    print("\nCRISIS ALERT: attempting access to 'classified_vault.txt'...")
    try:
        with open("classified_vault.txt", 'r') as file:
            print(file.read())
        print("STATUS: normal operations resumed")
    except (FileNotFoundError, PermissionError)as e:
        if e.__class__.__name__ == "FileNotFoundError":
            print("RESPONSE: archive not found in system matrix")
            print("STATUS: crisis handled, system stable")
        if e.__class__.__name__ == "PermissionError":
            print("RESPONSE: security protocols deny access")
            print("STATUS: crisis handled, security maintained")

    print("\nROUTINE ACCESS: Attempting access to 'standard_archive.txt'...")
    try:
        with(open("standard_archive.txt", 'r')) as file:
            print(f"Archive recovered: '{file.read()}'")
        print("STATUS: normal operations resumed")
    except (FileNotFoundError, PermissionError)as e:
        if e.__class__.__name__ == "FileNotFoundError":
            print("RESPONSE: archive not found in system matrix")
            print("STATUS: crisis handled, system stable")
        if e.__class__.__name__ == "PermissionError":
            print("RESPONSE: security protocols deny access")
            print("STATUS: crisis handled, security maintained")

    print("\nAll crisis scenarios handled successfully. Archives secure.")


if __name__ == "__main__":
    ft_crisis_response()
