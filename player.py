import numpy as np


class Player:
    def __init__(self, pname: str, money: int = 1000):
        self.pname: str = pname
        self.money: int = money
        self.cards: list = []
        self.current_bet: int = 0

    def bet(self):
        val = input(f"Input Player {self.pname} bet:")
        val_int = int(val)

        if val_int > self.money:
            val_int = self.money

        self.current_bet = val_int

    def sum_cards(self):
        return np.sum(self.cards)

    def print_cards(self):
        print(f"Player {self.pname}'s cards: {self.sum_cards()}")

    def game_player_won(self):
        self.money += self.current_bet * 1.5
        print(f"Player {self.pname} won.")

    def game_player_lost(self):
        self.money -= self.current_bet
        print(f"Player {self.pname} lost.")

    def game_player_tied(self):
        print(f"Player {self.pname} tied.")
