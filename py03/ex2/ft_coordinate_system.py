import sys
import math


def ft_calculate_distance(point1: tuple, point2: tuple) -> float:
    return math.sqrt((point1[0] - point2[0])**2
                     + (point1[1] - point2[1])**2
                     + (point1[2] - point2[2])**2)


def ft_parse_coordinates(string: str) -> tuple | None:
    if not string.__class__ == str:
        raise TypeError("Invalid coordinates string")
    try:
        coords = string.split(",")
        if len(coords) != 3:
            raise TypeError('Coordinates must contain exactly 3 values '
                            'separated by comma: "x,y,z"')
        # return tuple(map(int, coords))
        # Uso l'impacchettamento di tuple
        pos = int(coords[0]), int(coords[1]), int(coords[2])
        return pos
    except ValueError as e:
        raise e


def ft_coordinate_system() -> None:
    print("=== Game coordinate system ===")
    if len(sys.argv) >= 2:
        try:
            coord_tuple = ft_parse_coordinates(sys.argv[1])
            print("\nParsed position: ", coord_tuple)
            print(f"Distance between (0, 0, 0) and {coord_tuple}: "
                  f"{ft_calculate_distance((0, 0, 0), coord_tuple):.2f}")
        except Exception as e:
            print(f"Error: {e}")
    else:
        origin = (0, 0, 0)
        # Caso 1
        pos1 = (10, 20, 5)
        print(f"\nPosition created: {pos1}")
        dist1 = ft_calculate_distance(origin, pos1)
        print(f"Distance between {origin} and {pos1}: {dist1:.2f}")

        # Caso 2
        input_str = "3,4,0"
        print(f"\nParsing coordinates: \"{input_str}\"")
        try:
            pos2 = ft_parse_coordinates(input_str)
            print(f"Parsed position: {pos2}")
            dist2 = ft_calculate_distance(origin, pos2)
            print(f"Distance between {origin} and {pos2}: {dist2}")
        except Exception as e:
            print(f"Error: {e}")
        bad_inputs = [
            "abc,def,ghi",
            "1,2",
            "1,2,3,4",
            "1 2 3",
            12345
        ]
        invalid_str = bad_inputs[0]

        print(f"\nParsing invalid coordinates: \"{invalid_str}\"")
        try:
            ft_parse_coordinates(invalid_str)
        except ValueError as e:
            print(f"Error parsing coordinates: {e}")
            print(f"Error details - "
                  f"Type: {e.__class__.__name__}, Args: {e.args}")

        print("\nUnpacking demonstration:")
        if 'pos2' in locals():
            x, y, z = pos2
            print(f"Player at x={x}, y={y}, z={z}")
            print(f"Coordinates: X={x}, Y={y}, Z={z}")


if __name__ == "__main__":
    ft_coordinate_system()
