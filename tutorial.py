import curses
from curses import wrapper
from time import time
import json
import random


def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to the WPM Calculator Game")
    stdscr.addstr("\nPress any key to begin")
    stdscr.refresh()
    stdscr.getkey()


def display_text(stdscr, target, current, wpm=0):
    stdscr.addstr(target)
    stdscr.addstr(1, 0, f"WPM : {wpm}")

    for i, char in enumerate(current):
        correct = target[i]
        color = curses.color_pair(1)
        if char != correct:
            color = curses.color_pair(2)
        stdscr.addstr(0, i, char, color)


def load_text(difficulty):
    with open("text.json", "r") as f:
        data = json.load(f)
        level = {
            1: "Easy",
            2: "Hard",
            3: "Insane",
            4: "Russian",
            5: "Dont select this"
        }
        return (data[level[difficulty]][str(random.randint(
            1, len(data[level[difficulty]])))])


def wpm_test(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "Please enter a difficulty level")
    stdscr.addstr(
        1, 0, "1. Easy  2. hard  3. Insane  4. Russian  5. Dont enter this\n")
    stdscr.refresh()
    difficulty = stdscr.getkey()
    target_text = load_text(int(difficulty))
    current_text = []
    wpm = 0
    start_time = time()
    stdscr.nodelay(True)

    while True:
        time_elapsed = max(time() - start_time, 1)
        wpm = round(current_text.count(' ') / (time_elapsed / 60))

        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh()

        if ''.join(current_text) == target_text:
            stdscr.nodelay(False)
            break

        try:
            key = stdscr.getkey()
        except:
            continue

        if ord(key) == 27:
            break
        if key in ("KEY_BACKSPACE", "\b", "\x7f"):
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)


def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    start_screen(stdscr)
    while True:
        wpm_test(stdscr)
        stdscr.addstr(
            2, 0, "You completed the text! Press any key to play again!! or esc to quit :(")
        key = stdscr.getkey()
        if ord(key) == 27:
            break


wrapper(main)
