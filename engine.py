# Name: Grishma Raut
# Student ID: 202571518
# ICT401 Assessment 3 - engine.py
# This file has the game rules only. It has no print() or input(),
# so both the CLI and the GUI can use the same GameEngine class.

import random


def loadWords(filename):
    # read the word file and return a list of [word, hint]
    words = []
    try:
        with open(filename, "r") as file:
            for line in file:
                line = line.strip()

                # skip empty lines and lines without the | sign
                if line == "" or "|" not in line:
                    continue

                parts = line.split("|")
                word = parts[0].strip().upper()
                hint = parts[1].strip()

                # only keep the word if it has letters only and has a hint
                if word.isalpha() and hint != "":
                    words.append([word, hint])
    except FileNotFoundError:
        # the file is missing, so give back an empty list
        return []
    except:
        # any other problem reading the file
        return []

    return words


def saveResult(game, interface):
    # add one line to game_history.txt when a game ends
    if game.isWon():
        result = "WIN"
    else:
        result = "LOSS"

    line = (game.getSecretWord() + "|" + result + "|" + interface +
            "|score=" + str(game.getScore()) +
            "|lives=" + str(game.getLives()))

    try:
        with open("game_history.txt", "a") as file:
            file.write(line + "\n")
        return True
    except:
        # do not crash the game if the file cannot be written
        return False


class GameEngine:

    def __init__(self, words, lives=6):
        # protected attributes, other files use the get methods below
        self._secret_word = ""
        self._hint = ""
        self._guessed_letters = []
        self._remaining_lives = lives
        self._score = 0
        self.selectWord(words)

    def selectWord(self, words):
        # pick a random word and its hint from the list
        chosen = random.choice(words)
        self._secret_word = chosen[0]
        self._hint = chosen[1]

    # get methods so other files can read the values
    def getSecretWord(self):
        return self._secret_word

    def getHint(self):
        return self._hint

    def getGuessedLetters(self):
        return self._guessed_letters

    def getLives(self):
        return self._remaining_lives

    def getScore(self):
        return self._score

    def getDisplayWord(self):
        # show guessed letters and _ for the rest, like A _ P _ E
        display = ""
        for letter in self._secret_word:
            if letter in self._guessed_letters:
                display = display + letter + " "
            else:
                display = display + "_ "
        return display.strip()

    def validateLetter(self, letter):
        # check the guess is allowed, return an error message or "" if it is fine
        if len(letter) != 1:
            return "Please enter one letter only."
        if not letter.isalpha():
            return "Numbers and symbols are not allowed."
        if letter in self._guessed_letters:
            return "You already guessed " + letter + "."
        return ""

    def checkLetter(self, letter):
        # make the guess uppercase so the case does not matter
        letter = letter.strip().upper()

        message = self.validateLetter(letter)
        if message != "":
            # a bad guess does not take away a life
            return "invalid", message

        self._guessed_letters.append(letter)

        if letter in self._secret_word:
            self._score = self._score + 10
            return "correct", "Good guess, " + letter + " is in the word."
        else:
            self._remaining_lives = self._remaining_lives - 1
            return "wrong", "Sorry, " + letter + " is not in the word."

    def isWon(self):
        # the game is won when every letter in the word is guessed
        for letter in self._secret_word:
            if letter not in self._guessed_letters:
                return False
        return True

    def isLost(self):
        return self._remaining_lives <= 0

    def isOver(self):
        return self.isWon() or self.isLost()
