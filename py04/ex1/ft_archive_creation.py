def ft_archive_creation() -> None:
    print("=== CYBERARCHIVES - DATA RECOVERY SYSTEM ===")
    print("\nInitializing new storage unit: new_discovery.txt")
    filename = "new_discovery.txt"
    try:
        fd = open(filename, 'w')
        print("Storage unit created successfully")
        print("\nInscribing preservation data...")
        fd.write("[ENTRY 001] New quantum algorithm discovered\n")
        fd.write("[ENTRY 002] Efficiency increased by 347%\n")
        fd.write("[ENTRY 003] Archived by a data archivist trainee\n")
        fd.close()
        fd = open(filename, 'r')
        print(fd.read())
        print("Data inscription complete. Storage unit sealed.")
        print(f"Archive {filename} ready for long-term preservation.")
    except (IOError, FileNotFoundError, PermissionError) as e:
        print({e})
    finally:
        try:
            fd.close()
        except NameError as e:
            print(e)


if __name__ == '__main__':
    ft_archive_creation()
