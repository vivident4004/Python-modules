from random import randint
import time
from typing import Generator


class Player:
    def __init__(self, name: str, level: int = 0) -> None:
        self.name = name
        self.level = level


def hash_multiplication_int(k, w, p):
    """
    k: la chiave (intero)
    w: dimensione della parola macchina in bit (es. 32)
    p: numero di bit desiderati per l'hash (m = 2^p)
    """

    # 1. Calcolo della costante s basata sulla sezione aurea (Knuth)
    # Parametro precalcolato per non usare math
    # A = (sqrt(5) - 1) / 2 approx 0.618
    # s = A * 2^w
    # s = int((math.sqrt(5) - 1) / 2 * (2**w))
    s = 2654435769

    # 2. Moltiplicazione (k * s)
    valore_prodotto = k * s

    # 3. Estrazione di r0 (i w bit meno significativi)
    # Usiamo una maschera bit a bit per simulare il limite della parola
    # di w bit.
    # (1 << w) - 1 equivale a una sequenza di w '1' in binario.
    mask_w = (1 << w) - 1
    r0 = valore_prodotto & mask_w

    # 4. Estrazione dei p bit piú significativi di r0
    # Sposto r0 a destra di (w - p) posizioni.
    shift = w - p
    h = r0 >> shift
    return h


def event_generator(max_iter: int, players: list, actions: list) \
        -> Generator[str, None, None]:
    # Costanti per l'hashing come sul Cormen
    w = 32
    p = 15
    for k in range(max_iter):
        h = hash_multiplication_int(k, w, p)
        player_index = h % (len(players) - 1)
        action_index = (h + 1) % (len(actions) - 1)
        if actions[action_index] == 'leveled up':
            players[player_index].level += 1
        event = (f"Event {k + 1}: player {players[player_index].name} "
                 f"(level {players[player_index].level}) "
                 f"{actions[action_index]}.")
        yield event


def fibonacci_generator(a: int = 0, b: int = 1) -> Generator[int, None, None]:
    while True:
        yield a
        a, b = b, a + b


# La funzione restituire vero sse a è un «testimone»
# del fatto che n è un numero composto
# t e u sono t.c. t >= 1, u è dispari ed n - 1 = 2^t*u
def is_witness(a: int, n: int) -> bool:
    # u = 2
    # while True:
    #     if (n - 1) % u == 0:
    #         break
    #     u += 2
    # t = math.floor(math.log2((n - 1) / u))
    # Calcolo n - 1 = 2 ^ t * u
    # Invece di cercare divisori, dividiamo per 2 finché possiamo.
    u = n - 1
    t = 0
    while u % 2 == 0:
        u //= 2
        t += 1
    # Calcola (a^u) mod p
    x = pow(a, u, mod=n)
    # if x == 1 or x == n - 1:
    #     return True
    # for _ in range (t - 1):
    #     y = pow(x, 2, mod=n)
    #     if (y == 1) and (x != 1) and (x != n - 1):
    #         return True
    #     x = y
    # if x != 1:
    #     return True
    # return False
    # Se x è 1 o n-1, allora a non è un testimone (n potrebbe essere primo)
    if x == 1 or x == n - 1:
        return False

    # Ripeti t-1 volte
    for _ in range(t - 1):
        x = pow(x, 2, n)
        if x == n - 1:
            return False  # Trovato -1 (che è n-1 mod n), potrebbe essere primo
        if x == 1:
            return True
    # Se arriviamo qui, n è composto
    return True


def miller_rabin(n: int, s: int) -> bool:
    for j in range(1, s):
        a = randint(2, n - 1)
        if is_witness(a, n):
            return False
    return True


# https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test#Deterministic_variants
# Variante che dimostra la primalità di numeri minori di 2**64
def miller_rabin_det(n: int) -> bool:
    bases = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    if n in bases:
        return True
    for a in bases:
        if is_witness(a, n):
            return False
    return True


# https://www.johndcook.com/blog/2019/02/25/prime-test/
def prime_generator(n: int) -> Generator[int, None, None]:
    if n <= 2:
        n = 3
        yield 2
    if n % 2 == 0:
        n += 1
    while True:
        if n >= 3825123056546413051:
            if miller_rabin(n, 50):
                yield n
        else:
            if miller_rabin_det(n):
                yield n
        n += 2


def ft_data_stream():
    print("=== Game data stream processor ===")
    players = [Player('Alice', 5),
               Player('Bernardo', 12),
               Player('Camilla', 8),
               Player('Diego', 0),
               Player('Eliana', 0),
               Player('Francesco', 8),
               Player('Ginevra', 0),
               Player('Italo', 2),
               Player('Ludovica', 69),
               Player('Matilde', 0),
               Player('Nicola', 0)]

    actions = ['killed monster',
               'found treasure',
               'found treasure',
               'leveled up',
               'opened chest',
               'opened chest',
               'opened chest',
               'opened chest',
               'slayed skeleton',
               'slayed skeleton',
               'leveled up',
               'slayed skeleton',
               'slayed skeleton',
               'slayed skeleton',
               'found egg',
               'mined coal',
               'leveled up',
               'leveled up',
               'mined iron',
               'mined iron',
               'mined iron',
               'mined iron',
               'mined gold',
               'mined silver',
               'mined diamond']

    print("\nProcessing 1000 game events...")
    max_iter = 1000
    generator = event_generator(max_iter, players, actions)
    treasure_events = 0
    level_up_events = 0
    start = time.time()
    for i in range(max_iter):
        to_print = next(generator)
        if i < 3:
            print(to_print)
        if 'treasure' in to_print:
            treasure_events += 1
        if 'leveled up' in to_print:
            level_up_events += 1
    print("...\n")
    end = time.time()
    print("=== Stream analytics ===")
    print(f"Total events processed: {max_iter}")

    # Comprensione delle liste da 200 di QI
    print(f"High-level players (10+): "
          f"{sum(1 for p in players if p.level > 10)}")
    print(f"Treasure events: {treasure_events}")
    print(f"Level-up events: {level_up_events}")

    print("\nMemory usage: constant")
    print(f"Processing time: {end - start:.5f}")

    print("=== Generator demonstration ===")
    max_iter = 10
    fib_gen = fibonacci_generator()
    print(f"Fibonacci sequence (first {max_iter} numbers): ", end="")
    for n in range(max_iter):
        if n < max_iter - 1:
            print(f"{next(fib_gen)}", end=", ")
        else:
            print(f"{next(fib_gen)}", end="")

    start_number = 123456
    p_gen = prime_generator(start_number)
    print(f"\nPrime numbers "
          f"(successive {max_iter} starting from {start_number}): ", end="")
    for n in range(max_iter):
        if n < max_iter - 1:
            print(f"{next(p_gen)}", end=", ")
        else:
            print(f"{next(p_gen)}")


if __name__ == "__main__":
    ft_data_stream()
