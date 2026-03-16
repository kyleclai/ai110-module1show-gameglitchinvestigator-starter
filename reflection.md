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
- **Fix:** Swapped the two return strings so the `guess > secret` branch returns `"📉 Go LOWER!"` and the `guess < secret` branch returns `"📈 Go HIGHER!"`. The fix works because the hint message now matches the actual numeric relationship between guess and secret.

**Bug 2 — Secret was secretly converted to a string every other attempt**
- **Expected:** The comparison between my guess and the secret should always be a
  numeric comparison (e.g. `60 > 50`).
- **What actually happened:** On every even-numbered attempt, `secret` was cast to a
  string before being passed to `check_guess`. This caused lexicographic comparisons
  like `str(9) > str(10)` which evaluates to `True` (because `"9" > "1"`), producing
  completely wrong and inconsistent hints on alternating turns.
- **Root cause:** Lines 158-161 of `app.py` had an intentional `if attempts % 2 == 0`
  branch that called `str(st.session_state.secret)`.
- **Fix:** Removed the `if attempts % 2 == 0` block entirely and added an `assert isinstance(secret, int)` guard before `check_guess` is called. This ensures the secret is always read as an integer from session state without any conditional type casting, so comparisons are always numeric regardless of attempt number.

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

**Bug 4 — UI prompt always showed "1 to 100" regardless of difficulty**
- **Expected:** The on-screen prompt should tell the player the actual range for the
  selected difficulty (e.g. "Guess a number between 1 and 200" on Hard).
- **What actually happened:** The `st.info(...)` message had the range hardcoded as
  `"between 1 and 100"`, so Easy and Hard players saw the wrong range in the prompt
  even though the game itself used the correct range internally.
- **Root cause:** `app.py` used a string literal `"1 and 100"` instead of the `low`
  and `high` variables that were already computed from `get_range_for_difficulty`.
- **Fix:** Replaced the hardcoded values with `f"between {low} and {high}"` so the
  prompt dynamically reflects the actual range for the chosen difficulty.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
Claude integrated with VSCode.
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
After playing the game, I noticed the hints logic was backwards. Luckily, upon reviewing the project, Claude also noticed this bug, correctly identified the location of the logic error, and recommended a fix. I verified this fix by creating pytest assertions to ensure the logic works as intended.
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
Claude suggested to change the Hard mode logic to have a smaller number pool to guess from. This isn't correct as it would make the Hard mode easier to win than the Normal mode (given the number of guesses is constant). However, this suggestion highlighted that I could make the modes more difficult by editing the range of numbers - allowing me to fix the bug manually.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
After applying each fix, I re-ran the Streamlit app and manually tested the exact scenario that originally exposed the bug. For the inverted hints bug, I deliberately guessed a number I knew was too high and confirmed the app now said "Go LOWER!" instead of "Go HIGHER!". For the string-conversion bug, I submitted several guesses in a row and verified that hints were consistent across both odd and even attempt numbers — no more lexicographic weirdness.

- Describe at least one test you ran (manual or using pytest)
  and what it showed you about your code.
I wrote three pytest cases in `test_game_logic.py` — `test_winning_guess`, `test_guess_too_high`, and `test_guess_too_low` — which tested that `check_guess` returned the correct outcome for each scenario. Writing the tests revealed a mismatch: my test expected a plain string like `"Too High"`, but the actual implementation returns a tuple `(outcome, message)`. That forced me to decide whether to fix the tests or the function signature, which was a useful discovery I wouldn't have caught from manual testing alone.

- Did AI help you design or understand any tests? How?
Claude helped me think through what scenarios to cover — for example, asking what happens when guess equals secret exactly (the win case), and whether I needed to test invalid input at the `check_guess` level or only at `parse_guess`. I used those suggestions as a starting checklist, then adjusted based on what the actual function signatures looked like in `app.py`.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
The secret number kept changing because every time the user interacted with the app — clicking a button or typing in the input — Streamlit re-ran the entire Python script from top to bottom. Without session state, `random.randint(low, high)` would execute on every rerun, generating a brand-new secret each time instead of keeping the original one.

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
Imagine your entire program restarts from line 1 every time a user clicks anything. Session state is like a sticky notepad that survives those restarts — it lets the app remember things like the secret number, the attempt count, and the game status across interactions, so the game doesn't reset itself with every button press. I learned more about how this works by reading the official Streamlit documentation at https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state.

- What change did you make that finally gave the game a stable secret number?
I wrapped the `random.randint(low, high)` call in an `if "secret" not in st.session_state` guard (line 97–98 of `app.py`). The first time the script runs, the secret is generated and stored in `st.session_state.secret`. On every subsequent rerun, the condition is false so the stored value is preserved instead of replaced. Interestingly, I did not actually observe this bug during my initial playthrough — I was manually clearing my browser cache and rerunning the app between test sessions, which wiped session state each time and masked the issue. I only realized the bug existed after reviewing the code more carefully and understanding that a normal player would experience the secret silently changing mid-game without ever seeing an error.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
One strategy I want to reuse is using Plan Mode in Claude to outline an execution plan before diving into fixes. On this project, `reflection.md` essentially became my living plan — I kept it updated with bugs I found and my current thinking, and Claude could reference the persistent chat context to update the reflection in my own language. This made documentation feel natural rather than like an afterthought. I also want to keep using Git not just for version control, but as a real-time way to observe the project evolving — seeing diffs and commit history helped me stay grounded in what actually changed rather than just trusting what AI described.

- What is one thing you would do differently next time you work with AI on a coding task?
Next time I would think more broadly beyond logic bugs — I spent most of my time on code-level issues but didn't think much about UI behavior and how a real player would experience the app. I also leaned heavily on AI to surface bugs rather than forming my own hypotheses first from playing the game. Going forward, I want to combine both: play the app like a user, form my own theories, then use AI to help investigate — rather than asking AI what's wrong and just verifying its list.

- In one or two sentences, describe how this project changed the way you think about AI generated code.
Working with an incomplete and sometimes inaccurate task description made this feel like a real industry project — I couldn't rely on AI to hand me a perfect bug list, and not every hint it gave was right. That experience shifted how I think about AI-generated code: it's a collaborator that requires verification, not a source of truth, and the most important skill is knowing when to trust it and when to push back.
