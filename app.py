import curses
import time
from db_utils import save_to_db, view_scores, view_logs, get_random_text
from datetime import datetime

def typing_test(stdscr, text, time_limit_minutes):
    stdscr.clear()
    stdscr.addstr("Start typing the following text:\n\n")
    stdscr.addstr(text + "\n", curses.A_BOLD)
    stdscr.addstr("\nPress any key to start...\n")
    stdscr.refresh()
    stdscr.getkey()

    start_time = time.time()
    typed_text = []
    elapsed_time = 0

    while True:
        stdscr.clear()
        elapsed_time = time.time() - start_time
        minutes_left = max(0, time_limit_minutes * 60 - elapsed_time)
        seconds_left = int(minutes_left % 60)
        stdscr.addstr(f"Time Left: {minutes_left // 60}:{seconds_left:02d} minutes\n", curses.A_BOLD)
        stdscr.addstr(f"Time Elapsed: {elapsed_time:.1f} seconds\n", curses.A_BOLD)
        stdscr.addstr("\nTyping Test:\n\n")
        stdscr.addstr(text + "\n", curses.A_BOLD)
        stdscr.addstr("\n" + "".join(typed_text))
        stdscr.refresh()

        char = stdscr.getkey()
        if char == '\n' or elapsed_time >= time_limit_minutes * 60:
            break
        typed_text.append(char)

    end_time = time.time()
    total_time_minutes = (end_time - start_time) / 60
    wpm = len(typed_text) / 5 / total_time_minutes

    correct_chars = sum(1 for t, g in zip(typed_text, text) if t == g)
    accuracy = (correct_chars / len(text)) * 100

    return wpm, accuracy, elapsed_time

def main_menu(stdscr):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

    stdscr.clear()
    stdscr.addstr("Typing Speed Test\n", curses.A_BOLD)
    stdscr.addstr("1. Start Test\n")
    stdscr.addstr("2. View Scores\n")
    stdscr.addstr("3. View Logs\n")
    stdscr.addstr("4. Exit\n")
    stdscr.addstr("Choose an option: ")
    stdscr.refresh()

    option = stdscr.getkey()
    return option

def main(stdscr):
    while True:
        option = main_menu(stdscr)
        if option == "1":
            stdscr.clear()
            stdscr.addstr("Enter your name: ")
            stdscr.refresh()
            curses.echo()
            name = stdscr.getstr().decode()
            curses.noecho()

            stdscr.addstr("Choose difficulty (easy/medium/hard): ")
            stdscr.refresh()
            difficulty = stdscr.getstr().decode()

            stdscr.addstr("Enter the time limit in minutes (e.g., 1, 2, 3): ")
            stdscr.refresh()
            time_limit_minutes = int(stdscr.getstr().decode())

            try:
                text = get_random_text(difficulty, time_limit_minutes)  # Pass time_limit_minutes
                wpm, accuracy, elapsed_time = typing_test(stdscr, text, time_limit_minutes)
                save_to_db(name, difficulty, wpm, accuracy, elapsed_time)

                stdscr.addstr("\nTest Complete!\n")
                stdscr.addstr(f"WPM: {wpm:.2f}\n")
                stdscr.addstr(f"Accuracy: {accuracy:.2f}%\n")
                stdscr.addstr(f"Total Time: {elapsed_time:.1f} seconds\n")
                stdscr.addstr("Press any key to return to the menu...")
                stdscr.refresh()
                stdscr.getkey()
            except FileNotFoundError as e:
                stdscr.addstr(str(e) + "\n")
                stdscr.addstr("Press any key to return to the menu...")
                stdscr.refresh()
                stdscr.getkey()

        elif option == "2":
            view_scores(stdscr)
        elif option == "3":
            view_logs(stdscr)
        elif option == "4":
            break
        else:
            stdscr.addstr("Invalid option! Press any key to return to the menu...")
            stdscr.refresh()
            stdscr.getkey()

if __name__ == "__main__":
    curses.wrapper(main)

