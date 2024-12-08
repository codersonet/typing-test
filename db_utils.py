import curses
import mysql.connector
import random
import os

def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="your_username",
        password="your_password",
        database="typing_speed"
    )

def save_to_db(name, difficulty, wpm, accuracy, elapsed_time):
    db = connect_to_db()
    cursor = db.cursor()

    query_scores = "INSERT INTO user_scores (name, difficulty, wpm, accuracy) VALUES (%s, %s, %s, %s)"
    cursor.execute(query_scores, (name, difficulty, wpm, accuracy))

    marks = int(wpm * accuracy / 100)
    query_logs = """
        INSERT INTO user_logs 
        (user_name, test_date, test_time, difficulty, wpm, accuracy, marks, elapsed_time) 
        VALUES (%s, CURDATE(), CURTIME(), %s, %s, %s, %s, %s)
    """
    cursor.execute(query_logs, (name, difficulty, wpm, accuracy, marks, elapsed_time))

    db.commit()
    db.close()

def view_scores(stdscr):
    db = connect_to_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM user_scores")
    scores = cursor.fetchall()
    db.close()

    stdscr.clear()
    stdscr.addstr("Scores:\n", curses.A_BOLD)
    for score in scores:
        stdscr.addstr(f"Name: {score[1]}, Difficulty: {score[2]}, WPM: {score[3]}, Accuracy: {score[4]}\n")
    stdscr.addstr("\nPress any key to return to the menu...")
    stdscr.refresh()
    stdscr.getkey()

def view_logs(stdscr):
    db = connect_to_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM user_logs")
    logs = cursor.fetchall()
    db.close()

    stdscr.clear()
    stdscr.addstr("User Logs:\n", curses.A_BOLD)
    for log in logs:
        stdscr.addstr(f"{log}\n")
    stdscr.addstr("\nPress any key to return to the menu...")
    stdscr.refresh()
    stdscr.getkey()

def get_random_text(difficulty, time_limit_minutes):
    base_path = f"text_library/{difficulty}"
    if not os.path.exists(base_path):
        raise FileNotFoundError("Text files for this difficulty do not exist.")
    
    files = os.listdir(base_path)
    file_path = os.path.join(base_path, random.choice(files))
    with open(file_path, "r") as f:
        full_text = f.read().strip()

    # Define average WPM for each difficulty level
    avg_wpm = {"easy": 20, "medium": 40, "hard": 60}
    if difficulty not in avg_wpm:
        raise ValueError("Invalid difficulty level provided.")

    # Calculate the number of characters needed for the time limit
    chars_needed = avg_wpm[difficulty] * time_limit_minutes * 5

    # Adjust the text length
    if len(full_text) > chars_needed:
        # Truncate if text is longer
        text = full_text[:chars_needed]
    else:
        # Repeat text if shorter
        repeats = (chars_needed // len(full_text)) + 1
        text = (full_text * repeats)[:chars_needed]

    return text

