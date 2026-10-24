def check_temperature(temp_str: str) -> int:
    temp = int(temp_str)
    if temp < 0:
        raise ValueError(f"a {temp}" + '\u00a0\u2103' +
                         " fa troppo freddo per le piante "
                         "(min 0" + '\u00a0\u2103' + ").")
    if temp > 40:
        raise ValueError(f"a {temp}" + '\u00a0\u2103' +
                         " fa troppo caldo per le piante "
                         "(max 40" + '\u00a0\u2103' + ").")
    return temp


if __name__ == '__main__':
    print("=== Verificatore di temperature del giardino ===")
    try:
        temp_str = "C"
        print(f"Provando con la temperatura «{temp_str}»:")
        print(f"La temperatura {check_temperature(temp_str)} "
              f"è perfetta per le piante")
    except ValueError as e:
        print(f"Errore: {e}")
    try:
        temp_str = "42"
        print(f"Provando con temperatura «{temp_str}»:")
        print(f"La temperatura {check_temperature(temp_str)} "
              f"è perfetta per le piante")
    except ValueError as e:
        print(f"Errore: {e}")
    try:
        temp_str = "22"
        print(f"Provando con temperatura «{temp_str}»:")
        print(f"La temperatura {check_temperature(temp_str)} "
              f"è perfetta per le piante")
    except ValueError as e:
        print(f"Errore: {e}")
    try:
        temp_str = "-1"
        print(f"Provando con temperatura «{temp_str}»:")
        print(f"La temperatura {check_temperature(temp_str)} "
              f"è perfetta per le piante")
    except ValueError as e:
        print(f"Errore: {e}")
    try:
        temp_str = "0"
        print(f"Provando con temperatura «{temp_str}»:")
        print(f"La temperatura {check_temperature(temp_str)} "
              f"è al limite per le piante")
    except ValueError as e:
        print(f"Errore: {e}")
    try:
        temp_str = "40"
        print(f"Provando con temperatura «{temp_str}»:")
        print(f"La temperatura {check_temperature(temp_str)} "
              f"è al limite per le piante")
    except ValueError as e:
        print(f"Errore: {e}")
    print("Tutte le prove sono state completate con successo.")
