# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

When I first ran the app, the hints were immediately misleading and the game felt
unwinnable no matter what strategy I used. Three concrete bugs stood out:

**Bug 1 — Hints were backwards (Higher/Lower inverted)**
- **Expected:** When my guess was too high (e.g. I guessed 80 and the secret was 50),
  the app should tell me to go *lower*.
- **What actually happened:** The app said "Go HIGHER!" — the opposite of what I needed.
  Both the label ("Too High") and the emoji icon (📈) pointed in the wrong direction.
  This made it impossible to narrow down the secret by following the hints.
- **Root cause:** `check_guess` in `app.py` had `"📈 Go HIGHER!"` on the `guess > secret`
  branch and `"📉 Go LOWER!"` on the `guess < secret` branch — the messages were swapped.

**Bug 2 — Secret was secretly converted to a string every other attempt**
- **Expected:** The comparison between my guess and the secret should always be a
  numeric comparison (e.g. `60 > 50`).
- **What actually happened:** On every even-numbered attempt, `secret` was cast to a
  string before being passed to `check_guess`. This caused lexicographic comparisons
  like `str(9) > str(10)` which evaluates to `True` (because `"9" > "1"`), producing
  completely wrong and inconsistent hints on alternating turns.
- **Root cause:** Lines 158-161 of `app.py` had an intentional `if attempts % 2 == 0`
  branch that called `str(st.session_state.secret)`.

**Bug 3 — Hard difficulty has a narrower range than Normal, and Easy has fewer guesses than Normal**
- **Expected:** "Hard" should be harder than "Normal" — meaning a wider range of numbers
  to guess from and fewer attempts. "Easy" should be easier — meaning more attempts to guess.
- **What actually happened:** `get_range_for_difficulty("Hard")` returned `(1, 50)`,
  which is actually *easier* to guess within than Normal's `(1, 100)`. Hard had fewer
  attempts (5 vs 8) but a smaller range — the two settings worked against each other
  rather than compounding the difficulty. Additionally, Easy only allowed 6 guesses vs
  Normal's 8, which made Easy *harder* in terms of attempts despite having a smaller number range.
- **Root cause:** `app.py` line 10 set the Hard range to `1, 50` instead of a wider
  range, and `attempt_limit_map["Easy"]` was set to `6` instead of a higher value.
- **Fix:** Changed Hard's range to `(1, 200)` so it is genuinely harder than Normal's
  `(1, 100)`. Changed Easy's attempt limit to `10` so players have more chances, making
  Easy actually easier than Normal's 8 attempts.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
