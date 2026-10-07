# Name: Grishma Raut
# Student ID: 202571518
# ICT401 Assessment 3 - cli_app.py
# Text version of the game. All the rules come from engine.py,
# this file only shows things on the screen and reads what the user types.

import engine

# menu choices and the word file for each level
FILES = {"1": "easy.txt", "2": "medium.txt", "3": "hard.txt"}


def showGame(game):
    # make a string of the guessed letters
    guessed = ""
    for letter in game.getGuessedLetters():
        guessed = guessed + letter + " "

    print("")
    print("Word:    " + game.getDisplayWord())
    print("Hint:    " + game.getHint())
    print("Lives:   " + str(game.getLives()))
    print("Score:   " + str(game.getScore()))
    print("Guessed: " + guessed)


def playGame(filename):
    words = engine.loadWords(filename)

    # an empty list means the file is missing or has no good lines
    if len(words) == 0:
        print("Could not read " + filename + ". Please check the file.")
        return

    game = engine.GameEngine(words)
    print("\nA new word has been picked. Good luck!")

    # keep asking for letters until the game is over
    while not game.isOver():
        showGame(game)
        guess = input("Guess a letter: ")
        status, message = game.checkLetter(guess)
        print(message)

    # the game has ended, show the result
    showGame(game)
    if game.isWon():
        print("\nYou win! The word was " + game.getSecretWord() + ".")
    else:
        print("\nYou lost. The word was " + game.getSecretWord() + ".")

    # save the result in the history file
    if engine.saveResult(game, "CLI"):
        print("Result saved to game_history.txt")
    else:
        print("Sorry, the result could not be saved.")


def main():
    print("WORD GUESSING GAME")

    # menu loop, it keeps going until the user picks quit
    while True:
        print("\nChoose a level:")
        print("1. Easy")
        print("2. Medium")
        print("3. Hard")
        print("4. Quit")
        choice = input("Enter your choice: ").strip()

        if choice == "4":
            print("Thanks for playing.")
            break
        elif choice in FILES:
            playGame(FILES[choice])
        else:
            print("Please enter a number from 1 to 4.")


main()
