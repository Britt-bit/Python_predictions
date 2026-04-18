import random

max_guesses = 7


def main() -> None:
    while True:
        random_number = random.randint(1, 100)
        attempts = 0

        while attempts < max_guesses:
            guess = int(input("Guess a number between 1 and 100: "))
            attempts += 1

            if guess == random_number:
                print("You win! It took you", attempts, "attempts.")
                break
            if guess < random_number:
                print("Too low")
            else:
                print("Too high")

            remaining = max_guesses - attempts
            if remaining > 0:
                print(f"You have {remaining} guess(es) left.")
        else:
            print("Game over! The number was", random_number)

        again = input("Play again? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()
