# Bug-Hunt Findings Log

Fill in one entry per bug you find, AS YOU FIND IT (before doing the AI
comparison). Write in your own words, like a detective's notebook. Show the real
path -- including things you tried that did not work.

Group: <KKP>
Members: <Paing>

---

## Bug 1

- **Module / function:** users.py -> login()
- **What we suspected and why:** login() strips every non-alphanumeric character from the typed password (`cleaned`), but register() stores the password exactly as typed. The two sides are treated differently, so a password with a symbol or space can never match.
- **What we did:** In the Python shell, registered "bob" with "P@ss word!" and then logged in with the same password. Checked that a letters-and-digits password ("dave", "abc123") worked. Then wrote a regression test.
- **What we observed (the wrong result):** `login("bob", "P@ss word!")` returned False. The test output was `AssertionError: assert False is True` at `assert u.login("bob", "P@ss word!") is True`. It also works the wrong way round: logging in as "alice" (stored "secret1") with "secret1!!!" is accepted.
- **What we expected instead:** `login("bob", "P@ss word!")` returns True, and `login("alice", "secret1!!!")` returns False. The docstring says login returns True if the password matches, so the typed password must be compared exactly as it was registered.
- **The fix we made:** - Removed the `cleaned = ...` line and changed the comparison to `stored == password`, so login compares the password exactly as typed. register() is unchanged.
- **Author of this finding:** Paing

---

## Bug 2

- **Module / function:**
- **What we suspected and why:**
- **What we did:**
- **What we observed (the wrong result):**
- **What we expected instead:**
- **The fix we made:**
- **Author of this finding:**

---

## Bug 3

(copy the block above for each additional bug you find)
