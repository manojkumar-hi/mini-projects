import random

def play_game():
    print("🎮 Welcome to Number Guessing Game!")
    print("Choose a level:")
    print("1. Easy (1-10)")
    print("2. Medium (1-50)")
    print("3. Difficult (1-100)")

    choice = input("Enter your choice (1/2/3): ")

    if choice == '1':
        max_num = 10
        attempts = 5
    elif choice == '2':
        max_num = 50
        attempts = 7
    elif choice == '3':
        max_num = 100
        attempts = 10
    else:
        print("Invalid choice. Please start again.")
        return

    secret_number = random.randint(1, max_num)
    print(f"\nGuess the number between 1 and {max_num}. You have {attempts} attempts!")

    for i in range(1, attempts + 1):
        try:
            guess = int(input(f"Attempt {i}: "))
            if guess == secret_number:
                print("🎉 Congratulations! You guessed the correct number!")
                break
            elif guess < secret_number:
                print("🔼 Too low!")
            else:
                print("🔽 Too high!")
        except ValueError:
            print("Please enter a valid number.")

    else:
        print(f"❌ Out of attempts! The number was: {secret_number}")

# Start the game
play_game()
