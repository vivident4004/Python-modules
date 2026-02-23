def ft_ancient_text() -> None:
    print("=== CYBERARCHIVES - DATA RECOVERY SYSTEM ===")
    filename = 'ancient_fragment.txt'
    fd = -42
    print(f"\nAccessing storage vault: {filename}")
    try:
        fd = open(filename, 'r')
        print("Connection established...")
        print("\nRecovered data:")
        content = fd.read()
        print(content)
        print("\nData recovery complete. Storage unit disconnected.")
    except FileNotFoundError:
        print("ERROR: storage vault not found. Run the data generator first.")
    finally:
        if fd != -42:
            fd.close()


if __name__ == "__main__":
    ft_ancient_text()
