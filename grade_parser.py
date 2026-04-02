# grade_parser.py - Starter (BUGGY) version

def process_grades(student_list):
    """
    Takes a list of strings like ["Alice:85", "Bob:92", "Charlie:78"]
    and returns a summary dict with total, count, and average.
    """
    summary = {"total": 0, "count": 0, "average": 0.0}

    for entry in student_list:
        parts = entry.split(":")
        name = parts[0]
        score = int(parts[1])  # BUG 1: score is string, needs int(parts[1])

        summary["total"] += score  # BUG 3: adding a string to an int will raise TypeError 
        summary["count"] += 1

    if summary["count"] > 0:  # Guard against empty list (ZeroDivisionError)
        summary["average"] = summary["total"] / summary["count"]

    return summary


# --- Run it ---
# class_data = ["Alice:85", "Bob:92", "Charlie:78"]
class_data = []
result = process_grades(class_data)
print(f"Total: {result['total']}, Average: {result['average']}")
