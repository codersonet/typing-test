import pytest
from io import StringIO
import time
from app import typing_test, get_random_text

# Mock the stdscr (screen object) for curses
@pytest.fixture
def mock_stdscr():
    return StringIO()

# Test for get_random_text function (to check if it loads the correct text based on difficulty)
def test_get_random_text():
    text = get_random_text("easy")
    assert isinstance(text, str)
    assert len(text) > 0

    text_medium = get_random_text("medium")
    assert isinstance(text_medium, str)
    assert len(text_medium) > 0

    text_hard = get_random_text("hard")
    assert isinstance(text_hard, str)
    assert len(text_hard) > 0

# Test for typing speed calculation
def test_typing_speed(mock_stdscr):
    text = "The quick brown fox jumps over the lazy dog."
    
    # Simulating typing test
    start_time = time.time()
    typed_text = list("The quick brown fox jumps over the lazy dog.")
    elapsed_time = time.time() - start_time
    
    # Calculate words per minute (WPM)
    total_time_minutes = elapsed_time / 60
    wpm = len(typed_text) / 5 / total_time_minutes

    # Calculate accuracy
    correct_chars = sum(1 for t, g in zip(typed_text, text) if t == g)
    accuracy = (correct_chars / len(text)) * 100
    
    # Check the values of wpm, accuracy, and elapsed time
    assert isinstance(wpm, float)
    assert isinstance(accuracy, float)
    assert isinstance(elapsed_time, float)
    assert wpm > 0
    assert accuracy >= 0 and accuracy <= 100

