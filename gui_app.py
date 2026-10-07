# Name: Grishma Raut
# Student ID: 202571518
# ICT401 Assessment 3 - gui_app.py
# Window version of the game made with tkinter.
# It uses the same GameEngine class from engine.py without changing it.

from tkinter import *
from tkinter import messagebox

import engine


class WordGameGUI:

    def __init__(self, window):
        self.window = window
        self.window.title("Word Guessing Game")
        self.window.resizable(0, 0)

        self.game = None
        self.level_file = "easy.txt"
        self.buttons = {}

        # StringVar lets the labels change when we call set()
        self.level_text = StringVar()
        self.word_text = StringVar()
        self.hint_text = StringVar()
        self.lives_text = StringVar()
        self.score_text = StringVar()
        self.message_text = StringVar()

        # top row with the level buttons and quit button
        top = Frame(window)
        top.pack(pady=10)
        Button(top, text="Easy", width=8, command=self.startEasy).pack(side="left", padx=2)
        Button(top, text="Medium", width=8, command=self.startMedium).pack(side="left", padx=2)
        Button(top, text="Hard", width=8, command=self.startHard).pack(side="left", padx=2)
        Button(top, text="Quit", width=8, command=window.destroy).pack(side="left", padx=10)

        # labels to show the game
        Label(window, textvariable=self.level_text).pack()
        Label(window, textvariable=self.word_text, font=("Courier", 22)).pack(pady=10)
        Label(window, textvariable=self.hint_text).pack()
        self.lives_label = Label(window, textvariable=self.lives_text, font=("Arial", 12))
        self.lives_label.pack(pady=5)
        Label(window, textvariable=self.score_text).pack()
        Label(window, textvariable=self.message_text).pack(pady=5)

        # the on screen keyboard in three rows
        rows = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
        for row in rows:
            row_frame = Frame(window)
            row_frame.pack()
            for letter in row:
                # letter=letter makes each button keep its own letter
                button = Button(row_frame, text=letter, width=3, bg="white",
                                command=lambda letter=letter: self.guess(letter))
                button.pack(side="left", padx=1, pady=1)
                self.buttons[letter] = button

        Label(window, text="").pack()
        self.newGame()

    # the three level buttons each call one of these
    def startEasy(self):
        self.level_file = "easy.txt"
        self.newGame()

    def startMedium(self):
        self.level_file = "medium.txt"
        self.newGame()

    def startHard(self):
        self.level_file = "hard.txt"
        self.newGame()

    def newGame(self):
        words = engine.loadWords(self.level_file)

        # stop if the word file is missing or empty
        if len(words) == 0:
            messagebox.showinfo("Error", "Could not read " + self.level_file)
            return

        self.game = engine.GameEngine(words)

        # turn all the letter buttons back on
        for letter in self.buttons:
            self.buttons[letter].config(state="normal", bg="white")

        self.level_text.set("Level: " + self.level_file.replace(".txt", ""))
        self.message_text.set("Click a letter to start.")
        self.updateScreen()

    def guess(self, letter):
        # this runs when a letter button is clicked
        if self.game.isOver():
            return

        status, message = self.game.checkLetter(letter)
        self.message_text.set(message)

        # turn the button off so it cannot be clicked again
        if status == "correct":
            self.buttons[letter].config(state="disabled", bg="lightgreen")
        elif status == "wrong":
            self.buttons[letter].config(state="disabled", bg="tomato")

        self.updateScreen()

        if self.game.isOver():
            self.endGame()

    def updateScreen(self):
        # copy the values from the engine to the labels
        self.word_text.set(self.game.getDisplayWord())
        self.hint_text.set("Hint: " + self.game.getHint())
        self.lives_text.set("Lives left: " + str(self.game.getLives()))
        self.score_text.set("Score: " + str(self.game.getScore()))

        # change the colour when lives are getting low
        lives = self.game.getLives()
        if lives > 3:
            self.lives_label.config(fg="green")
        elif lives > 1:
            self.lives_label.config(fg="orange")
        else:
            self.lives_label.config(fg="red")

    def endGame(self):
        # show the full word with spaces between the letters
        word = ""
        for letter in self.game.getSecretWord():
            word = word + letter + " "
        self.word_text.set(word.strip())

        engine.saveResult(self.game, "GUI")

        if self.game.isWon():
            messagebox.showinfo("You win", "Well done! The word was "
                                + self.game.getSecretWord() +
                                "\nScore: " + str(self.game.getScore()))
        else:
            messagebox.showinfo("Game over", "You ran out of lives. The word was "
                                + self.game.getSecretWord())

        # start the next game after the message is closed
        self.newGame()


window = Tk()
WordGameGUI(window)
window.mainloop()
