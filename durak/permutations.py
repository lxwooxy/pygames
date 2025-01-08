from itertools import permutations

nums = [2,3,4,5,6,7,8,9,10,11,12,13,14]
lookup = {2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five', 6: 'Six', 7: 'Seven', 8: 'Eight', 9: 'Nine', 10: 'Ten', 11: 'Jack', 12: 'Queen', 13: 'King', 14: 'Ace'}
cards = ["Clubs", "Diamonds", "Hearts", "Spades"]

def create_deck():
    return [f"{lookup[rank]} of {suit}" for suit in cards for rank in nums]

    


def select_elements(dict):
    
    
    keys = list(dict.keys())
    values = list(dict.values())
    result = {}
    used_numbers = set()

    for key in keys:
        for pair in values[keys.index(key)]:
            if pair[0] not in used_numbers and pair[1] not in used_numbers:
                result[key] = pair
                used_numbers.update(pair)
                break

    if len(used_numbers) == len(keys) * 2:
        return result
    return None

if __name__ == "__main__":
    # print(create_deck())
    
    dict = {
        "a": [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7)],
        "b": [(5, 6), (5, 7), (3, 9), (3, 10), (3, 11), (3, 12)],
        "c": [(3, 4), (8, 10), (2, 10), (2, 11), (2, 12), (2, 13)],
        "d": [(9, 10), (2, 4), (5, 8), (5, 9), (5, 10), (5, 11)],
        "e": [(7, 8), (6, 9), (6, 7), (6, 10), (6, 11), (6, 12)],
        "f": [(11, 12), (11, 13), (11, 14), (11, 15), (11, 16), (11, 17)],
        "g": [(15, 16), (15, 17), (13, 19), (13, 20), (13, 18), (13, 17)],
        "h": [(13, 14), (18, 20), (12, 20), (12, 19), (12, 18), (12, 17)],
        "i": [(19, 20), (12, 14), (15, 18), (15, 19), (15, 20), (15, 17)],
        "j": [(17, 18), (16, 19), (16, 17), (16, 18), (16, 19), (16, 20)]
    }
        
    print(select_elements(dict))

        