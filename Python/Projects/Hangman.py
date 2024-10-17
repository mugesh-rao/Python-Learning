import random

stages = ['''
  +---+
  |   |
      |
      |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
      |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
  |   |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========''']

word_list = ["advark", "baboon", "camel"]

games_is_finished = False
lives = len(stages) - 1
chosen_word = random.choice(word_list)
word_len = len(chosen_word)

display =[]
for _ in range(word_len):
    display += "_"

while not games_is_finished:
 guess = input("Guess a value : ").lower()


 if guess in display:
    print("You've Already Guessed{guess}")

 for postion in range(word_len):
    letter = chosen_word[postion]
    if letter == guess :
        display[postion] = letter
 print(f"{' '.join(display)}")

 if guess not in chosen_word:
      lives -= 1
      if lives == 0:
        games_is_finished = True
        print("You Lose")


if "_" not in display: 
    games_is_finished = True
    print("you win")

print(stages[lives])
   