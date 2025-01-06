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
            return sorted(non_trump_cards, key=lambda c: ranks.index(c.split(' of ')[0]))[0]
        elif trump_cards:
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
            return sorted(same_suit_cards, key=lambda c: ranks.index(c.split(' of ')[0]))[0]
        elif trump_cards:
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
        self.max_cards_per_round = 7
        self.attack_completed = False  # Track when the attacker ends the round

        # Initialize AI Opponents
        self.ai_opponents = [
            AIOpponent(self.players[i], self.trump_suit)
            for i in range(1, self.num_players)
        ]

        self.deal_cards()

    def deal_cards(self):
        """Deal six cards to each player."""
        for player in self.players:
            while len(player) < 6 and self.deck:
                player.append(self.deck.pop())
        for ai in self.ai_opponents:
            ai.hand = self.players[self.ai_opponents.index(ai) + 1]

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
                    move = input("Choose a card to attack with (e.g., '7 of Spades') or type 'no further questions': ").strip()
                    if move == "no further questions":
                        self.attack_completed = True
                        return "end_round"
                    if move in self.players[0]:
                        self.center_cards.append(move)
                        self.players[0].remove(move)
                        print(f"You attacked with {move}.")
                        if len(self.center_cards) >= self.max_cards_per_round:
                            self.attack_completed = True
                            return "end_round"
                        return "player_attacked"
                    else:
                        print("Invalid input. Please choose a valid card.")
                else:  # Player is defending
                    move = input("Choose a card to defend with (e.g., '7 of Spades') or type 'pickup': ").strip()
                    if move == "pickup":
                        print("You picked up the cards!")
                        self.players[0].extend(self.center_cards)
                        self.center_cards = []
                        self.attack_completed = True
                        return "pickup"
                    elif move in self.players[0] and self.validate_move(move):
                        self.center_cards.append(move)
                        self.players[0].remove(move)
                        print(f"You defended with {move}.")
                        return "player_defended"
                    else:
                        print("Invalid move. Try again.")
            except Exception as e:
                print(f"Error: {e}. Try again.")

    def computer_move(self):
        """Handle the AI's move."""
        ai = self.ai_opponents[self.current_attacker - 1]

        if len(self.center_cards) % 2 == 0:  # AI is attacking
            if self.attack_completed:
                return "end_round"
            attack_card = ai.choose_attack_card(self.center_cards)
            if attack_card:
                self.center_cards.append(attack_card)
                self.players[self.current_attacker].remove(attack_card)
                print(f"Computer attacked with {attack_card}.")
                if len(self.center_cards) >= self.max_cards_per_round:
                    self.attack_completed = True
                    return "end_round"
                return "computer_attacked"
            else:
                print("Computer has no valid cards to attack with.")
                self.attack_completed = True
                return "end_round"
        else:  # AI is defending
            attack_card = self.center_cards[-1]
            defense_card = ai.choose_defense_card(attack_card)
            if defense_card:
                self.center_cards.append(defense_card)
                self.players[self.current_defender].remove(defense_card)
                print(f"Computer defended with {defense_card}.")
                return "computer_defended"
            else:
                print("Computer couldn't defend and picked up the cards.")
                self.players[self.current_defender].extend(self.center_cards)
                self.center_cards = []
                self.attack_completed = True
                return "pickup"

    def next_turn(self):
        """Advance to the next turn."""
        self.current_attacker = (self.current_attacker + 1) % self.num_players
        self.current_defender = (self.current_defender + 1) % self.num_players

    def resolve_round(self):
        """Resolve the round by clearing center cards and refilling hands."""
        print("Round resolved. Drawing new cards...")
        self.center_cards = []
        self.deal_cards()
        self.attack_completed = False

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

            if self.current_attacker == 0:  # Player's turn to attack
                result = self.player_move()
                if result == "end_round":
                    self.resolve_round()
                elif result == "pickup":
                    self.next_turn()
            else:  # AI's turn to attack
                result = self.computer_move()
                if result == "end_round":
                    self.resolve_round()
                elif result == "pickup":
                    self.next_turn()
