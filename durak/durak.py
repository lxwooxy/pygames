import tkinter as tk
import random

# Suits and Ranks
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = ['6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

# Create a deck of cards
def create_deck():
    return [f"{rank} of {suit}" for suit in suits for rank in ranks]

class DurakGame:
    def __init__(self, root, num_players=2):
        self.root = root
        self.num_players = num_players
        self.deck = create_deck()
        random.shuffle(self.deck)
        self.players = [[] for _ in range(num_players)]
        self.trump_card = self.deck.pop()
        self.trump_suit = self.trump_card.split(' of ')[1]
        self.current_attacker = 0
        self.current_defender = 1
        self.center_cards = []
        self.status_var = tk.StringVar()
        self.status_var.set("Welcome to Durak!")
        self.init_ui()

        # Deal cards to players
        self.deal_cards()

    def init_ui(self):
        """Initialize the game UI."""
        self.canvas = tk.Canvas(self.root, width=800, height=600, bg="green")
        self.canvas.pack()

        # Player hand display
        self.player_hand_frame = tk.Frame(self.root, bg="green")
        self.player_hand_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # Status label
        self.status_label = tk.Label(self.root, textvariable=self.status_var, font=("Arial", 16), bg="green", fg="white")
        self.status_label.pack(side=tk.TOP, pady=10)

        # Button for actions
        self.action_button = tk.Button(self.root, text="Next Move", command=self.next_move, font=("Arial", 14))
        self.action_button.pack(side=tk.TOP, pady=5)

        self.update_ui()

    def deal_cards(self):
        """Deal six cards to each player."""
        for player in self.players:
            while len(player) < 6 and self.deck:
                player.append(self.deck.pop())

    def update_ui(self):
        """Update the UI with the latest game state."""
        # Clear player hand frame
        for widget in self.player_hand_frame.winfo_children():
            widget.destroy()

        # Display player's cards
        for card in self.players[0]:
            btn = tk.Button(self.player_hand_frame, text=card, command=lambda c=card: self.player_move(c))
            btn.pack(side=tk.LEFT, padx=5, pady=5)

        # Display trump card
        self.canvas.delete("all")
        self.canvas.create_text(400, 50, text=f"Trump Card: {self.trump_card}", font=("Arial", 16), fill="white")
        self.canvas.create_text(400, 100, text=f"Trump Suit: {self.trump_suit}", font=("Arial", 16), fill="white")

        # Display center cards
        self.canvas.create_text(400, 300, text="Center Cards", font=("Arial", 16), fill="white")
        y = 320
        for card in self.center_cards:
            self.canvas.create_text(400, y, text=card, font=("Arial", 14), fill="yellow")
            y += 20

    def player_move(self, card):
        """Handle player's move."""
        if len(self.center_cards) % 2 == 0:  # Player is attacking
            self.center_cards.append(card)
            self.players[0].remove(card)
            self.status_var.set(f"You attacked with {card}. Waiting for defender.")
        else:
            self.status_var.set("You can't defend for the computer. Click 'Next Move'.")

        self.update_ui()

    def next_move(self):
        """Handle the computer's move."""
        if len(self.center_cards) % 2 == 1:  # Defender's turn
            defender_cards = self.players[self.current_defender]
            attack_card = self.center_cards[-1]
            defending_card = None

            # Try to defend with a card of the same suit or trump
            for card in defender_cards:
                rank, suit = card.split(' of ')
                attack_rank, attack_suit = attack_card.split(' of ')
                if suit == attack_suit and ranks.index(rank) > ranks.index(attack_rank):
                    defending_card = card
                    break
                elif suit == self.trump_suit and attack_suit != self.trump_suit:
                    defending_card = card
                    break

            if defending_card:
                self.center_cards.append(defending_card)
                defender_cards.remove(defending_card)
                self.status_var.set(f"Defender defended with {defending_card}.")
            else:
                self.status_var.set("Defender couldn't defend. Cards picked up.")
                self.players[self.current_defender].extend(self.center_cards)
                self.center_cards = []
                self.current_attacker = (self.current_attacker + 1) % self.num_players
                self.current_defender = (self.current_defender + 1) % self.num_players
        else:  # New attack phase
            self.status_var.set("New attack phase. Your turn to attack.")

        # Refill cards
        self.deal_cards()
        self.update_ui()

# Tkinter app initialization
def start_game(num_players):
    root = tk.Tk()
    root.title("Durak Card Game")
    root.geometry("800x600")
    DurakGame(root, num_players=num_players)
    root.mainloop()

if __name__ == "__main__":
    start_game(num_players=2)
