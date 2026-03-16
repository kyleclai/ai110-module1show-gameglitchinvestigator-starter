# Project 1: Game Glitch Investigator — Grading Rubric

**Total Points: 18pts + 8pts bonus**

---

## Required Features (18pts)

### Bug Reproduction Evidence (3pts)

| Points | Criteria |
|--------|----------|
| 1 | There is concrete evidence that the game was run (e.g., screenshot, recorded output, or written trace referencing specific game events). |
| 1 | Two or more reproducible incorrect behaviors are clearly tied to observable output or game actions. |
| 1 | Bug descriptions specify expected vs. actual behavior (e.g., "Score never increases when collecting items," "Game crashes on arrow-key input due to missing boundary check"). |

**What to look for:** The student should show they actually ran the starter code — not just read it. Acceptable evidence includes a screenshot of the terminal/game output, a copy-pasted run log, or a written walkthrough that references specific in-game events (e.g., "when I pressed the arrow key, the game exited with a KeyError"). Each bug report must state both what *should* happen and what *actually* happened.

---

### Identification of At Least Three Distinct Bugs (3pts)

| Points | Criteria |
|--------|----------|
| 1 | Three or more distinct bugs are listed. |
| 1 | Bug descriptions correctly identify code-level causes or the problematic sections of code. |
| 1 | All listed bugs are real, reproducible issues present in the starter code (not hypothetical or imagined bugs). |

**What to look for:** Each bug should be distinct — not just multiple descriptions of the same underlying problem. Students must point to *where* in the code the issue originates (e.g., a specific function, line, or logic block), not just describe the symptom. Verify that each reported bug can actually be reproduced by running the unmodified starter code.

---

### Verification and Critique of AI Debugging Suggestions (3pts)

| Points | Criteria |
|--------|----------|
| 1 | At least one AI-generated explanation of a bug is included (e.g., a Copilot or ChatGPT response). |
| 1 | At least one correct AI suggestion is identified and the student explains *why* it is correct. |
| 1 | At least one incorrect or misleading AI suggestion is identified and the student explains *why* it is not correct. |

**What to look for:** The student must demonstrate critical evaluation of AI output — not just acceptance. They should quote or paraphrase the AI's suggestion, then provide their own reasoning for whether it holds up. A correct identification might be: "Copilot correctly noted that the score variable was never updated inside the loop." A critique might be: "The AI suggested wrapping the input in a try/except, but the real issue is that the input is never converted to an integer at all."

---

### Implementation of At Least Two Correct Bug Fixes (3pts)

| Points | Criteria |
|--------|----------|
| 1 | At least two bugs are documented with corresponding code changes. |
| 1 | Bug fixes resolve the reported issues without introducing new regressions. |
| 1 | The student explains what was changed to fix each bug and why the fix works. |

**What to look for:** Look at the actual diff between the starter code and the student's submission. Each fix should be clearly connected to a previously documented bug. The explanation should go beyond "I changed line X" — the student should articulate the logic (e.g., "I moved the score increment inside the conditional so it only fires when a valid item is collected"). Manually test the fixed game to confirm the bugs are resolved and no new errors were introduced.

---

### Working Game Demonstration (Post-Fix) (3pts)

| Points | Criteria |
|--------|----------|
| 1 | There is evidence of the game running without crashing after updates are made. |
| 1 | Game behavior matches the intended function for the fixed issues. |
| 1 | No new critical errors are introduced by the student's changes. |

**What to look for:** A screenshot or recorded output of the game running successfully after fixes is expected. The demonstrated behavior should directly correspond to the bugs that were fixed — if the student fixed a score bug, the demo should show the score updating correctly. Run the student's final code yourself if evidence is unclear or missing.

---

### Documentation, Reflection, and Git Usage (3pts)

| Points | Criteria |
|--------|----------|
| 1 | README clearly describes the game's purpose, the bugs found, and the fixes applied. |
| 1 | Reflection summarizes AI collaboration, including both helpful and flawed AI outputs. |
| 1 | Git history includes multiple meaningful commits with descriptive messages (not one giant commit). |

**What to look for:** The README should read as a standalone document — someone unfamiliar with the project should understand what the game does, what was broken, and what was fixed. The reflection (in `reflection.md` or the README) should name specific AI tools used and give honest, specific examples of where AI helped and where it fell short. For git, check the commit log: look for at least 3–4 commits spread across the work (e.g., "initial exploration," "fix score bug," "fix boundary crash," "add README"). A single commit with everything is not acceptable.

---

## Stretch Features (8pts bonus)

### +2pts — Advanced Edge-Case Testing

At least three `pytest` test cases targeting complex edge cases are implemented (e.g., non-numeric string input, negative numbers, empty inputs).

- Tests are specific, pass successfully, and show evidence of using the **Generate Tests** smart action or targeted AI prompting to create them.
- A screenshot of `pytest` results showing all tests passing is included in the README.

**What to look for:** Tests should not just be happy-path checks — they should probe boundaries and failure modes. Verify the tests actually run by checking for the `pytest` screenshot. Deduct if tests are trivial (e.g., only testing `1 + 1 == 2`) or if the screenshot is missing.

---

### +2pts — Feature Expansion via Agent Mode

Agent Mode is used to implement a meaningful new feature (e.g., a High Score tracker, Guess History sidebar, or Difficulty Levels). The feature must be fully functional.

- The student explains in code comments or the README how Agent Mode helped orchestrate multi-file changes.

**What to look for:** The new feature should be non-trivial — a single-line addition does not qualify. The student's explanation should specifically mention Agent Mode and describe what it did (e.g., "Agent Mode updated both `game.py` and `logic_utils.py` to wire up the high score logic"). Test the feature to confirm it works end-to-end.

---

### +2pts — Professional Documentation and Style

The **Generate Documentation** smart action is used to add professional docstrings to all functions in `logic_utils.py`.

- Code follows PEP 8 style guidelines, with evidence that Copilot was used to "Fix" or "Review" formatting and naming consistency.

**What to look for:** Every function in `logic_utils.py` should have a docstring that describes its purpose, parameters, and return value. The student should mention in the README or reflection that they used the Generate Documentation action. Check for PEP 8 compliance: consistent indentation, no lines over 79 characters, snake_case naming. There should be some evidence (e.g., a comment or reflection note) that Copilot was used for formatting review.

---

### +2pts — Thorough AI Model or Prompt Comparison

`reflection.md` includes a section comparing the output of two different AI models (e.g., Copilot GPT-4o vs. Gemini) for a specific logic bug.

- Analysis covers which model provided a more "Pythonic" fix and which explanation was easier to understand.

**What to look for:** The comparison must be grounded in a *specific* bug — not a general impression of the tools. The student should quote or closely paraphrase both models' responses and then analyze the differences. Look for genuine critical thinking: which solution was cleaner, which explanation was clearer, and why. Vague statements like "Model A was better" without evidence do not qualify.

---

*Grader note: When in doubt about partial credit, favor the student if the intent is clear and the work demonstrates genuine effort and understanding.*
