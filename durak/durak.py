import random

# Suits and Ranks
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = ['6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

# Create a deck of cards
def create_deck():
    return [f"{rank} of {suit}" for suit in suits for rank in ranks]

class AIOpponent:
    def __init__(self, hand, trump_suit):
        self.hand = hand
        self.trump_suit = trump_suit

    def choose_attack_card(self, center_cards):
        """Choose the weakest card to attack with."""
        non_trump_cards = [card for card in self.hand if not card.endswith(f"of {self.trump_suit}")]
        trump_cards = [card for card in self.hand if card.endswith(f"of {self.trump_suit}")]

        if non_trump_cards:
            # Return the weakest non-trump card
            return sorted(non_trump_cards, key=lambda c: ranks.index(c.split(' of ')[0]))[0]
        elif trump_cards:
            # Return the weakest trump card if no non-trump cards are available
            return sorted(trump_cards, key=lambda c: ranks.index(c.split(' of ')[0]))[0]
        return None

    def choose_defense_card(self, attack_card):
        """Choose the weakest valid card to defend with."""
        attack_rank, attack_suit = attack_card.split(' of ')

        # Find valid defense cards
        same_suit_cards = [
            card for card in self.hand if card.endswith(f"of {attack_suit}") and
            ranks.index(card.split(' of ')[0]) > ranks.index(attack_rank)
        ]
        trump_cards = [
            card for card in self.hand if card.endswith(f"of {self.trump_suit}") and attack_suit != self.trump_suit
        ]

        if same_suit_cards:
            # Use the weakest card of the same suit
            return sorted(same_suit_cards, key=lambda c: ranks.index(c.split(' of ')[0]))[0]
        elif trump_cards:
            # Use the weakest trump card if defending with the same suit isn't possible
            return sorted(trump_cards, key=lambda c: ranks.index(c.split(' of ')[0]))[0]
        return None  # No valid defense card found


class DurakGame:
    def __init__(self, num_players=2):
        self.num_players = num_players
        self.deck = create_deck()
        random.shuffle(self.deck)
        self.players = [[] for _ in range(num_players)]
        self.trump_card = self.deck.pop()
        self.trump_suit = self.trump_card.split(' of ')[1]
        self.current_attacker = 0
        self.current_defender = 1
        self.center_cards = []  # Cards currently in play

        # Initialize AI Opponents
        self.ai_opponents = [
            AIOpponent(self.players[i], self.trump_suit)
            for i in range(1, self.num_players)
        ]

        # Deal cards to players
        self.deal_cards()

    def next_turn(self, defender_picked_up=False):
        """
        Advance to the next turn.
        If the defender picks up, the attack passes to the next player.
        Otherwise, the defender becomes the new attacker.
        """
        if defender_picked_up:
            # Defender picks up, attack moves to the next player
            self.current_attacker = (self.current_attacker + 1) % self.num_players
            self.current_defender = (self.current_attacker + 1) % self.num_players
        else:
            # Defender successfully defends, becomes the attacker
            self.current_attacker = self.current_defender
            self.current_defender = (self.current_attacker + 1) % self.num_players

    def check_winner(self):
        """Check if the game has a winner."""
        active_players = [i for i, player in enumerate(self.players) if player]
        if len(active_players) == 1:
            winner = active_players[0]
            print(f"Player {winner} is the winner!")
            return True
        return False

    def play_game(self):
        """Main game loop."""
        print("Welcome to Durak!")
        while True:
            if self.check_winner():
                break

            if self.current_attacker == 0:  # Player's turn to attack
                result = self.player_move()

                if result == "player_attacked":
                    # After the player attacks, AI defends
                    result = self.computer_move()
                    if result == "pickup":
                        self.next_turn(defender_picked_up=True)
                elif result == "pickup":
                    self.next_turn(defender_picked_up=True)

            else:  # AI's turn to attack
                result = self.computer_move()

                if result == "computer_attacked":
                    # After the AI attacks, player defends
                    result = self.player_move()
                    if result == "pickup":
                        self.next_turn(defender_picked_up=True)
                elif result == "pickup":
                    self.next_turn(defender_picked_up=True)

            # Refill cards
            self.deal_cards()


# Start the game
if __name__ == "__main__":
    game = DurakGame(num_players=2)
    game.play_game()
