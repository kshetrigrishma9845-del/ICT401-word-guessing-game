# Name: Grishma Raut
# Student ID: 202571518
# ICT401 Assessment 4 - tester.py
# A tester program for the GameEngine class, as shown in the Week 9 lecture.
# It builds an engine with a known word, calls the methods, and compares
# the result with the expected value. The engine can be tested like this
# because it has no print() or input() statements.

import engine

# counters for the summary at the end
passed = 0
failed = 0


def check(test_name, actual, expected):
    # compare one result and print whether it passed
    global passed, failed
    if actual == expected:
        passed = passed + 1
        result = "PASS"
    else:
        failed = failed + 1
        result = "FAIL"
    print(result + "  " + test_name)
    print("      expected: " + str(expected))
    print("      actual:   " + str(actual))


def newEngine():
    # always start from the same word so the tests give the same result
    return engine.GameEngine([["APPLE", "A common fruit"]])


print("TESTING THE GAME ENGINE")
print("=" * 50)

# 1. the hidden word starts with all letters covered
game = newEngine()
check("Hidden word at the start", game.getDisplayWord(), "_ _ _ _ _")

# 2. a correct letter is shown and scores 10 points
game = newEngine()
status, message = game.checkLetter("A")
check("Correct letter gives status", status, "correct")
check("Correct letter updates the word", game.getDisplayWord(), "A _ _ _ _")
check("Correct letter scores 10", game.getScore(), 10)
check("Correct letter keeps all lives", game.getLives(), 6)

# 3. a wrong letter takes one life
game = newEngine()
status, message = game.checkLetter("Z")
check("Wrong letter gives status", status, "wrong")
check("Wrong letter takes one life", game.getLives(), 5)

# 4. lower case is treated as upper case
game = newEngine()
game.checkLetter("a")
check("Lower case is accepted", game.getDisplayWord(), "A _ _ _ _")

# 5. numbers and symbols are rejected and cost nothing
game = newEngine()
status, message = game.checkLetter("7")
check("Number is rejected", status, "invalid")
check("Number costs no life", game.getLives(), 6)

game = newEngine()
status, message = game.checkLetter("#")
check("Symbol is rejected", status, "invalid")

# 6. more than one character is rejected
game = newEngine()
status, message = game.checkLetter("ab")
check("Two letters are rejected", status, "invalid")

# 7. the same letter cannot be guessed twice
game = newEngine()
game.checkLetter("A")
status, message = game.checkLetter("A")
check("Repeated letter is rejected", status, "invalid")
check("Repeated letter costs no life", game.getLives(), 6)

# 8. the game is won when every letter is guessed
game = newEngine()
for letter in "APLE":
    game.checkLetter(letter)
check("Game is won", game.isWon(), True)
check("Game is over", game.isOver(), True)

# 9. the game is lost after six wrong guesses
game = newEngine()
for letter in "ZXQVBN":
    game.checkLetter(letter)
check("Game is lost", game.isLost(), True)
check("No lives are left", game.getLives(), 0)

# 10. a missing file returns an empty list instead of crashing
check("Missing file returns empty list", engine.loadWords("no_such_file.txt"), [])
check("Real file loads ten words", len(engine.loadWords("easy.txt")), 10)

print("=" * 50)
print("Tests passed: " + str(passed))
print("Tests failed: " + str(failed))
