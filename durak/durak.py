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
        self.trump_suit = None

    def choose_attack_card(self, center_cards):
        """Choose a card to attack with."""
        for card in self.hand:
            return card  # Simplified logic for choosing a card

    def choose_defense_card(self, attack_card, trump_suit):
        """Choose a card to defend with."""
        attack_rank, attack_suit = attack_card.split(' of ')
        for card in self.hand:
            rank, suit = card.split(' of ')
            if suit == attack_suit and ranks.index(rank) > ranks.index(attack_rank):
                return card  # Valid defense with the same suit
            elif suit == trump_suit and attack_suit != trump_suit:
                return card  # Valid defense with a trump card
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

        # Deal cards to players
        self.deal_cards()

    def deal_cards(self):
        """Deal six cards to each player."""
        for player in self.players:
            while len(player) < 6 and self.deck:
                player.append(self.deck.pop())

    def display_game_state(self):
        """Display the current game state."""
        print("\n" + "=" * 40)
        print(f"Trump Card: {self.trump_card} (Trump Suit: {self.trump_suit})")
        print("Cards in Play: ", ", ".join(self.center_cards) if self.center_cards else "None")
        print(f"Your Hand: {', '.join(self.players[0])}")
        print("=" * 40)

    def player_move(self):
        """Handle the player's move."""
        while True:
            try:
                self.display_game_state()
                if len(self.center_cards) % 2 == 0:  # Player is attacking
                    move = input("Choose a card to attack with (e.g., '7 of Spades'): ").strip()
                else:  # Player is defending
                    move = input("Choose a card to defend with (e.g., '7 of Spades') or type 'pickup': ").strip()

                if move == "pickup" and len(self.center_cards) % 2 == 1:
                    # Player chooses to pick up cards
                    print("You picked up the cards!")
                    self.players[0].extend(self.center_cards)
                    self.center_cards = []
                    return "next_turn"
                elif move in self.players[0]:
                    # Validate and play the chosen card
                    if self.validate_move(move):
                        self.center_cards.append(move)
                        self.players[0].remove(move)
                        return "valid_move"
                    else:
                        print("Invalid move. Try again.")
                else:
                    print("Invalid input. Please choose a valid card.")
            except Exception as e:
                print(f"Error: {e}. Try again.")

    def validate_move(self, card):
        """Validate the player's move."""
        if len(self.center_cards) % 2 == 0:  # Attack move
            return True
        else:  # Defense move
            attack_card = self.center_cards[-1]
            attack_rank, attack_suit = attack_card.split(' of ')
            rank, suit = card.split(' of ')
            if suit == attack_suit and ranks.index(rank) > ranks.index(attack_rank):
                return True  # Valid defense with the same suit
            elif suit == self.trump_suit and attack_suit != self.trump_suit:
                return True  # Valid defense with a trump card
            return False

    def computer_move(self):
        """Handle the computer's move."""
        if len(self.center_cards) % 2 == 0:  # Computer is attacking
            for card in self.players[self.current_attacker]:
                self.center_cards.append(card)
                self.players[self.current_attacker].remove(card)
                print(f"Computer attacked with {card}.")
                return "attack"
        else:  # Computer is defending
            attack_card = self.center_cards[-1]
            attack_rank, attack_suit = attack_card.split(' of ')
            for card in self.players[self.current_defender]:
                rank, suit = card.split(' of ')
                if suit == attack_suit and ranks.index(rank) > ranks.index(attack_rank):
                    self.center_cards.append(card)
                    self.players[self.current_defender].remove(card)
                    print(f"Computer defended with {card}.")
                    return "defense"
                elif suit == self.trump_suit and attack_suit != self.trump_suit:
                    self.center_cards.append(card)
                    self.players[self.current_defender].remove(card)
                    print(f"Computer defended with {card}.")
                    return "defense"

            # Computer cannot defend and picks up the cards
            print("Computer couldn't defend and picked up the cards.")
            self.players[self.current_defender].extend(self.center_cards)
            self.center_cards = []
            return "pickup"

    def next_turn(self):
        """Advance to the next turn."""
        self.current_attacker = (self.current_attacker + 1) % self.num_players
        self.current_defender = (self.current_defender + 1) % self.num_players

    def check_winner(self):
        """Check if the game has a winner."""
        for i, player in enumerate(self.players):
            if not player:
                print(f"Player {i} is out of cards!")
                if i == 0:
                    print("Congratulations! You win!")
                else:
                    print("You lost. Better luck next time!")
                return True
        return False

    def play_game(self):
        """Main game loop."""
        print("Welcome to Durak!")
        while True:
            if self.check_winner():
                break

            if self.current_attacker == 0:  # Player's turn
                result = self.player_move()
            else:  # Computer's turn
                result = self.computer_move()

            if result in ["pickup", "next_turn"]:
                self.next_turn()

            # Refill cards
            self.deal_cards()

# Start the game
if __name__ == "__main__":
    game = DurakGame(num_players=2)
    game.play_game()
