def get_range_for_difficulty(difficulty: str) -> tuple[int, int]:
    """Return the inclusive numeric range for a given difficulty level.

    Maps a difficulty string to a (low, high) integer tuple that defines
    the range of possible secret numbers for that mode. Higher difficulty
    levels use a wider range, making the secret harder to guess.

    Args:
        difficulty (str): One of "Easy", "Normal", or "Hard".

    Returns:
        tuple[int, int]: A (low, high) pair representing the inclusive
        range of valid secret numbers. Defaults to (1, 100) for any
        unrecognized difficulty string.

    Examples:
        >>> get_range_for_difficulty("Easy")
        (1, 20)
        >>> get_range_for_difficulty("Hard")
        (1, 200)
        >>> get_range_for_difficulty("Unknown")
        (1, 100)
    """
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 200
    return 1, 100


def parse_guess(raw: str) -> tuple[bool, int | None, str | None]:
    """Parse raw user input into a validated integer guess.

    Accepts whole numbers and decimal strings (truncated to int).
    Rejects empty input, None, non-numeric strings, and special characters.

    Args:
        raw (str | None): The raw string entered by the user.

    Returns:
        tuple[bool, int | None, str | None]: A three-element tuple:
            - ok (bool): True if parsing succeeded, False otherwise.
            - guess_int (int | None): The parsed integer, or None on failure.
            - error_message (str | None): A human-readable error string if
              parsing failed, or None on success.

    Examples:
        >>> parse_guess("42")
        (True, 42, None)
        >>> parse_guess("7.9")
        (True, 7, None)
        >>> parse_guess("hello")
        (False, None, 'That is not a number.')
        >>> parse_guess("")
        (False, None, 'Enter a guess.')
    """
    if raw is None:
        return False, None, "Enter a guess."
    if raw == "":
        return False, None, "Enter a guess."
    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."
    return True, value, None


def check_guess(guess: int, secret: int) -> str:
    """Compare a player's guess to the secret number and return an outcome.

    Performs a numeric comparison between the guess and the secret.
    Both arguments must be integers to ensure correct comparison behaviour
    (avoids lexicographic ordering bugs from string-typed inputs).

    Args:
        guess (int): The integer value the player submitted.
        secret (int): The secret integer the player is trying to guess.

    Returns:
        str: One of three outcome strings:
            - "Win"      — guess matches the secret exactly.
            - "Too High" — guess is greater than the secret.
            - "Too Low"  — guess is less than the secret.

    Examples:
        >>> check_guess(50, 50)
        'Win'
        >>> check_guess(60, 50)
        'Too High'
        >>> check_guess(40, 50)
        'Too Low'
    """
    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


def update_score(current_score: int, outcome: str, attempt_number: int) -> int:
    """Calculate and return an updated score based on the guess outcome.

    Awards points for a win (more points for fewer attempts used) and
    applies point deductions or small bonuses for incorrect guesses.
    A winning guess always awards a minimum of 10 points regardless of
    how many attempts were used.

    Args:
        current_score (int): The player's score before this guess.
        outcome (str): The result of the guess — "Win", "Too High",
            or "Too Low".
        attempt_number (int): The 1-based count of attempts used so far,
            used to scale the win reward.

    Returns:
        int: The updated score after applying the outcome's point change.

    Examples:
        >>> update_score(0, "Win", 1)
        80
        >>> update_score(50, "Too Low", 3)
        45
        >>> update_score(50, "Too High", 2)
        55
    """
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points
    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5
    if outcome == "Too Low":
        return current_score - 5
    return current_score
