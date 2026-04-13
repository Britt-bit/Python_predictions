import random

choices = ["rock", "paper", "scissors"]

computer_wins = 0
user_wins = 0
number_of_plays = 5

while number_of_plays > 0:
    random_choice = random.choice(choices)

    user_choice = input("Enter rock, paper, or scissors: ").strip().lower()
    while user_choice not in choices:
        print('Invalid choice. Please enter "rock", "paper", or "scissors".')
        user_choice = input("Enter rock, paper, or scissors: ").strip().lower()

    if user_choice == random_choice:
        print("It's a tie! You both chose", user_choice)
        number_of_plays += 1
    elif (user_choice == "rock" and random_choice == "scissors") or \
         (user_choice == "paper" and random_choice == "rock") or \
         (user_choice == "scissors" and random_choice == "paper"):
        print("You win! You chose", user_choice, "and the computer chose", random_choice)
        user_wins += 1
    else:
        print("You lose! You chose", user_choice, "and the computer chose", random_choice)
        computer_wins += 1
    
    number_of_plays -= 1

if user_wins > computer_wins:
    print(f"You won the game! Final score: You {user_wins} - Computer {computer_wins}")
elif computer_wins > user_wins:
    print(f"You lost the game! Final score: You {user_wins} - Computer {computer_wins}")
else:
    print(f"The game is a tie! Final score: You {user_wins} - Computer {computer_wins}")