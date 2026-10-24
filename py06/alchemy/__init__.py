"""Pacchetto per la gestione di entità elementali."""

__version__ = "1.0.0"
__author__ = "Master Pythonicus"
from .elements import create_fire, create_water

__all__ = [
    "create_fire",
    "create_water"
]


def print_metadata() -> None:
    """Stampa a video i metadati del pacchetto.

    Visualizza la versione corrente e l'autore del software.
    Utilizza le variabili globali __version__ e __author__.
    """
    print("Package metadata:")
    print(f"Version: {__version__}")
    print(f"Author: {__author__}")
