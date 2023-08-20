import game_logic
from user_interfaces import ConsoleOutput


if __name__ == '__main__':
   ui = ConsoleOutput()
   game = game_logic.Game(n_decks= 5, user_interface = ui)
   