import sys


def ft_command_quest() -> None:
    print("=== Command quest ===")
    if len(sys.argv) < 2:
        print("No arguments provided. Usage: "
              "ft_command_quest <command> <arguments>")
        print(f"Program name: {sys.argv[0]}")
        print(f"Total arguments: {len(sys.argv)}")
    else:
        print(f"Program name: {sys.argv[0]}")
        print(f"Arguments received: {len(sys.argv)}")
        for i in range(1, len(sys.argv)):
            print(f"Argument {i}: {sys.argv[i]}")
        print(f"Total arguments: {len(sys.argv)}")


if __name__ == "__main__":
    ft_command_quest()
