import curses
from curses import wrapper

import time
import random

def start_game(stdscr):
    stdscr.clear()
    #numbers are rows and colomun on where to place text
    stdscr.addstr(0,0, "Welcome To Typing Speed Test!")
    stdscr.addstr("\nPress Any Key to Begin!")
    stdscr.refresh()
    stdscr.getkey()

def display_text(stdscr, target, current, wpm=0):
    stdscr.addstr(target)
    stdscr.addstr(1,0, f"WPM: {wpm}")

    for i, char in enumerate(current):
        correct_char= target[i]
        color = curses.color_pair(1)
        if char != correct_char:
            color = curses.color_pair(2)

        stdscr.addstr(0, i, char, color)

def choose_text():
    with open("text file.txt", "r") as f:
        lines = f.readlines()
        return random.choice(lines).strip()


def wpm_test(stdscr):
    target_text = choose_text()
    current_text = []
    wpm = 0

    start_time = time.time()

    #not to delay until user enters input
    stdscr.nodelay(True)

    while True:
        #use max to avoid zero division error
        time_passed = max(time.time() - start_time, 1)

        wpm = round((len(current_text) / (time_passed/60))/5)

        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh()

        if "".join(current_text) == target_text:
            stdscr.nodelay(False)
            break
        
        try:
            key = stdscr.getkey()
        except:
            continue

        #escape key to exit
        if ord(key)== 27:
            break

        #backspace to remove char from current_text
        if key in ("KEY_BACKSPACE", "\b", "\x7f"):
            if len(current_text)>0:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)


def main(stdscr):
    #add style pair
    #initialize curses
    stdscr= curses.initscr()

    #turn on color support
    curses.start_color()

    #defining color pairs
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    start_game(stdscr)

    while True:
        wpm_test(stdscr)
        stdscr.addstr(2,0, "Congradulations! You Completed The Text! \nPress Any Key To Continue")
        key = stdscr.getkey()
        
        if ord(key) == 27:
            break

wrapper(main)