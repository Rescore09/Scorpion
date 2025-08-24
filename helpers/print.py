from random import choice
from helpers.utils import *

class Print:
    PREFIXES = ["[+]", "[-]", "[*]", "[$]"]
    SESSION_PREFIX = choice(PREFIXES)

    @staticmethod
    def prt(content: str, color: str = "WHITE", bold: bool = False):
        color = color.upper()
        ansi_color = globals().get(color, WHITE)
        print(f"{BOLD}{ansi_color}{Print.SESSION_PREFIX}{RESET} {BOLD}{content}{RESET}")
