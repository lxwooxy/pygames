nums = [2,3,4,5,6,7,8,9,10,11,12,13,14]
lookup = {2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five', 6: 'Six', 7: 'Seven', 8: 'Eight', 9: 'Nine', 10: 'Ten', 11: 'Jack', 12: 'Queen', 13: 'King', 14: 'Ace'}
cards = ["Clubs", "Diamonds", "Hearts", "Spades"]

def create_deck():
    return [f"{lookup[rank]} of {suit}" for suit in cards for rank in nums]

if __name__ == "__main__":
    print(create_deck())