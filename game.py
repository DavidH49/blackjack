from player import Player
import numpy as np
from icecream import ic


class Game:
    def __init__(self):
        self.CARD_SET_DEFAULT: list = [0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10] * 4
        self.PLAYERS: list = [Player("1")]
        self.card_set: list = self.CARD_SET_DEFAULT

    def deal_cards(self) -> int:
        if len(self.card_set) == 0:
            self.card_set = self.CARD_SET_DEFAULT
            np.random.shuffle(self.card_set)

        return self.card_set.pop()

    def handle_bets(self):
        for p in self.PLAYERS:
            if p.money <= 0:
                continue
            p.bet()

    def handle_dealing_dealer(self) -> list:
        cards_dealer: list = [self.deal_cards(), self.deal_cards()]
        print(f"Dealer's cards: {cards_dealer[0]}, ?")

        return cards_dealer

    def handle_dealing_players(self):
        for p in self.PLAYERS:
            p.cards = [self.deal_cards(), self.deal_cards()]
            p.print_cards()

    def handle_actions_player(self):
        for p in self.PLAYERS:
            while True:
                if p.sum_cards() >= 21:
                    break

                if p.cards == [0, 10] or p.cards == [10, 0]:
                    break

                action = input(f"Player {p.pname}: [double/hit/stand]: ")

                if action.lower() == "double":
                    p.cards.append(self.deal_cards())
                    p.print_cards()
                    p.current_bet *= 2
                    break
                elif action.lower() == "hit":
                    p.cards.append(self.deal_cards())
                    p.print_cards()
                elif action.lower() == "stand":
                    break
                else:
                    print("Please type one of the three options")
                    continue

    def handle_actions_dealer(self, cards_dealer: list) -> list:
        while True:
            if sum(cards_dealer) >= 17:
                break

            if cards_dealer == [0, 10] or cards_dealer == [10, 0]:
                break

            cards_dealer.append(self.deal_cards())

        return cards_dealer

    def handle_aces(self, cards: list) -> int:
        if 0 in cards:
            if sum(cards) + 11 <= 21:
                return 11
            else:
                return 1

        return 0

    def handle_blackjack(self, player: Player, cards_dealer: list) -> bool:
        blackjack_player: bool = player.cards == [0, 10] or player.cards == [10, 0]
        blackjack_dealer: bool = cards_dealer == [0, 10] or cards_dealer == [10, 0]

        if blackjack_player or blackjack_dealer:
            if blackjack_player and blackjack_dealer:
                player.game_player_tied()
            elif blackjack_player:
                player.game_player_won()
            else:
                player.game_player_lost()

            return True
        return False

    def handle_evaluating(self, p: Player, cards_dealer: list) -> None:
        # Check for Blackjack
        if self.handle_blackjack(p, cards_dealer):
            return

        #ace_player = self.handle_aces(p.cards)
        #ace_dealer = self.handle_aces(cards_dealer)
        #p.cards.append(ace_player)
        #cards_dealer.append(ace_dealer)

        sum_dealer = sum(cards_dealer)

        # Check if the dealer busted
        if sum_dealer > 21:
            if p.sum_cards() <= 21:
                p.game_player_won()
            else:
                p.game_player_tied()
            return

        sum_cards = sum(p.cards)

        # Check if the player busted or won
        if sum_cards > 21:
            p.game_player_lost()
        elif sum_cards == 21 or sum_cards > sum_dealer:
            p.game_player_won()
        elif sum_cards == sum_dealer:
            p.game_player_tied()
        else:
            p.game_player_lost()

    def game_loop(self):
        np.random.shuffle(self.card_set)

        while True:
            # Ask all players for their bets
            self.handle_bets()

            # Give the dealer two cards
            cards_dealer: list = self.handle_dealing_dealer()

            # Give both players two cards
            self.handle_dealing_players()

            # Ask both players if they want to hit or stand
            self.handle_actions_player()

            # Give the dealer more cards
            cards_dealer = self.handle_actions_dealer(cards_dealer)
            print(f"Dealer's cards: {sum(cards_dealer)}")

            # Check whose cards have a higher value
            for p in self.PLAYERS:
                self.handle_evaluating(p, cards_dealer)
