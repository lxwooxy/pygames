import random
import time

def generate_hacker_text():
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{}|;:',.<>?/"
    hacker_text = ""
    phrases = ["IM HACKING THE MAINFRAME", "ACCESS GRANTED", "ENCRYPTION BYPASSED", "DATA EXFILTRATED"]
    for _ in range(1000):
        for _ in range(200):
            if random.random() < 0.05:
                hacker_text += random.choice(phrases) + " "
            else:
                hacker_text += random.choice(characters)
            if random.random() < 0.1:
                print(hacker_text)
        time.sleep(0.5)

def main():
    generate_hacker_text()
    

if __name__ == "__main__":
    main()