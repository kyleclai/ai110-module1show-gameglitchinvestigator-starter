from logic_utils import check_guess, parse_guess, get_range_for_difficulty, update_score


# --- check_guess ---

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"

def test_guess_by_one_above():
    # Edge case: guess is exactly one above the secret
    assert check_guess(51, 50) == "Too High"

def test_guess_by_one_below():
    # Edge case: guess is exactly one below the secret
    assert check_guess(49, 50) == "Too Low"

def test_guess_at_boundary_low():
    # Guess equals the lowest possible value (1) and secret is also 1
    assert check_guess(1, 1) == "Win"

def test_guess_at_boundary_high():
    # Guess equals a large value and secret matches
    assert check_guess(200, 200) == "Win"


# --- parse_guess ---

def test_parse_guess_valid_integer():
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None

def test_parse_guess_empty_string():
    # Empty input should fail gracefully
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None

def test_parse_guess_none():
    # None input should fail gracefully
    ok, value, err = parse_guess(None)
    assert ok is False
    assert value is None

def test_parse_guess_non_numeric_string():
    # A word should not be accepted as a guess
    ok, value, err = parse_guess("hello")
    assert ok is False
    assert value is None

def test_parse_guess_float_rounds_to_int():
    # Floats should be accepted and truncated to int
    ok, value, err = parse_guess("7.9")
    assert ok is True
    assert value == 7

def test_parse_guess_negative_number():
    # Negative numbers should parse as ints (even if out of game range)
    ok, value, err = parse_guess("-5")
    assert ok is True
    assert value == -5

def test_parse_guess_special_characters():
    # Special characters should not be accepted
    ok, value, err = parse_guess("!@#")
    assert ok is False


# --- get_range_for_difficulty ---

def test_easy_range():
    low, high = get_range_for_difficulty("Easy")
    assert low == 1
    assert high == 20

def test_normal_range():
    low, high = get_range_for_difficulty("Normal")
    assert low == 1
    assert high == 100

def test_hard_range():
    low, high = get_range_for_difficulty("Hard")
    assert low == 1
    assert high == 200

def test_hard_is_harder_than_normal():
    # Hard range should be wider than Normal range
    _, hard_high = get_range_for_difficulty("Hard")
    _, normal_high = get_range_for_difficulty("Normal")
    assert hard_high > normal_high

def test_easy_is_easier_than_normal():
    # Easy range should be narrower than Normal range
    _, easy_high = get_range_for_difficulty("Easy")
    _, normal_high = get_range_for_difficulty("Normal")
    assert easy_high < normal_high

def test_unknown_difficulty_defaults_to_normal():
    # Unknown difficulty should fall back to (1, 100)
    low, high = get_range_for_difficulty("Impossible")
    assert low == 1
    assert high == 100


# --- update_score ---

def test_score_increases_on_win():
    new_score = update_score(0, "Win", 1)
    assert new_score > 0

def test_score_decreases_on_too_low():
    new_score = update_score(50, "Too Low", 1)
    assert new_score < 50

def test_win_on_first_attempt_gives_max_points():
    # Winning on attempt 1 should give more points than winning on attempt 5
    early_win = update_score(0, "Win", 1)
    late_win = update_score(0, "Win", 5)
    assert early_win > late_win

def test_score_never_goes_below_minimum_on_win():
    # Even a very late win should award at least 10 points
    score = update_score(0, "Win", 100)
    assert score >= 10
