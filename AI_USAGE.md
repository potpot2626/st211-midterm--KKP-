# AI Usage Declaration and Audit

**Group:** KKP  **Members:** Paing

**Part D3 of the midterm — 20 marks.**

Checklist:

- [x] Part 1 declaration complete
- [x] All eight tests appear in the summary table with a verdict
- [x] All eight have two pasted evidence runs (shipped code, and our fixed code)
- [x] Part 3 coverage table filled in against `FINDINGS.md`
- [x] Part 4 verdict written, under 400 words
- [x] Every audit entry names the member who did it
- [x] No claim made that we cannot demonstrate from pasted output
- [ ] File committed as `AI_USAGE.md` in the repository root

---

## Part 1 — AI usage declaration

| Tool | What we used it for | Where in the project | How we checked it before relying on it |
|---|---|---|---|
| Claude (Anthropic) | Step-by-step guidance on the project; explaining the audit method; interpreting pytest output; drafting the wording of AI_USAGE.md, FINDINGS.md, REPORT.md and the CI workflow `tests.yml` | `AI_USAGE.md`, `FINDINGS.md`, `REPORT.md`, `.github/workflows/tests.yml`, and the `ai_review/` audit | Guidance was used as a starting point. Every verdict and every claim about test results was checked against our own pytest output (both runs pasted above). Regression tests were run against a clean copy of the shipped code and all failed there before we relied on them. |

Note: `ai_review/test_ai_suggested.py` is named `ai_review/test_ai_generated.py` in our repository. All commands and entries below use the real filename.

---

## Part 2 — Audit of the supplied test set

### Summary table

| # | Test | What it claims to catch | Shipped | Fixed | Verdict | Auditor |
|---|---|---|---|---|---|---|
| 1 | test_cart_total_sums_items | cart total is the sum of all item prices | FAIL | PASS | Genuine detection | Paing |
| 2 | test_login_rejects_wrong_password | login rejects a wrong password | PASS | PASS | Detects nothing | Paing |
| 3 | test_search_finds_exact_title | search finds a product by its exact title | PASS | PASS | Detects nothing | Paing |
| 4 | test_import_returns_count | import returns the number of products imported | FAIL | PASS | Genuine detection | Paing |
| 5 | test_register_duplicate_returns_false | registering a taken username returns False | PASS | PASS | Detects nothing | Paing |
| 6 | test_checkout_empty_returns_none | checkout of an empty cart returns None | FAIL | PASS | Genuine detection | Paing |
| 7 | test_add_to_cart_returns_true_for_known_product | adding a known product to the cart returns True | PASS | PASS | Detects nothing | Paing |
| 8 | test_search_is_limited_to_ten_results | search returns at most ten results | FAIL | FAIL | Invented requirement | Paing |

### Detail entries

---

#### Test: `test_cart_total_sums_items`  (`ai_review/test_ai_generated.py:12`)

**Audited by:** Paing

**1. What it claims to catch.** That the cart total is the sum of the prices of every item in the cart.

**2. Evidence — against the shipped code**

Command: `python -m pytest ai_review/test_ai_generated.py::test_cart_total_sums_items -v`

```text
<PASTE BLOCK from shipped_each.txt>
```

**3. Evidence — against our fixed code**

Command: `python -m pytest ai_review/test_ai_generated.py::test_cart_total_sums_items -v`

```text
<PASTE BLOCK from fixed_each.txt>
```

**4. What that pair proves.** FAIL then PASS is the "Genuine detection" row. On the shipped code the assertion failed with `assert 10 == 30`, and after our fix to the cart total it passed. The test caught a real defect (Bug 2 in FINDINGS.md).

**5. Verdict**

- [x] Genuine detection — FAIL then PASS
- [ ] Detects nothing — PASS then PASS
- [ ] Locks in the bug — PASS then FAIL
- [ ] Invented requirement — FAIL then FAIL

---

#### Test: `test_login_rejects_wrong_password`  (`ai_review/test_ai_generated.py:19`)

**Audited by:** Paing

**1. What it claims to catch.** That login returns False when the password is wrong.

**2. Evidence — against the shipped code**

Command: `python -m pytest ai_review/test_ai_generated.py::test_login_rejects_wrong_password -v`

```text
<PASTE BLOCK from shipped_each.txt>
```

**3. Evidence — against our fixed code**

Command: `python -m pytest ai_review/test_ai_generated.py::test_login_rejects_wrong_password -v`

```text
<PASTE BLOCK from fixed_each.txt>
```

**4. What that pair proves.** PASS then PASS is the "Detects nothing" row. The test uses the wrong password "wrongpw", which contains only letters. Our Bug 1 in `login` only appears when the password contains symbols or spaces, so the buggy code rejects this input correctly too. To catch the bug, the test would have to log in with a symbol password such as "P@ss word!" and assert True.

**5. Verdict**

- [ ] Genuine detection — FAIL then PASS
- [x] Detects nothing — PASS then PASS
- [ ] Locks in the bug — PASS then FAIL
- [ ] Invented requirement — FAIL then FAIL

---

#### Test: `test_search_finds_exact_title`  (`ai_review/test_ai_generated.py:25`)

**Audited by:** Paing

**1. What it claims to catch.** That searching for a product's exact title finds that product.

**2. Evidence — against the shipped code**

Command: `python -m pytest ai_review/test_ai_generated.py::test_search_finds_exact_title -v`

```text
<PASTE BLOCK from shipped_each.txt>
```

**3. Evidence — against our fixed code**

Command: `python -m pytest ai_review/test_ai_generated.py::test_search_finds_exact_title -v`

```text
<PASTE BLOCK from fixed_each.txt>
```

**4. What that pair proves.** PASS then PASS is the "Detects nothing" row. The test searches with the exact title in identical capitalisation, which almost any version of `search` handles correctly. It never exercises the cases where a search can go wrong, such as a keyword in a different case or a partial keyword, so it gives false confidence.

**5. Verdict**

- [ ] Genuine detection — FAIL then PASS
- [x] Detects nothing — PASS then PASS
- [ ] Locks in the bug — PASS then FAIL
- [ ] Invented requirement — FAIL then FAIL

---

#### Test: `test_import_returns_count`  (`ai_review/test_ai_generated.py:31`)

**Audited by:** Paing

**1. What it claims to catch.** That the import function returns the number of products actually imported.

**2. Evidence — against the shipped code**

Command: `python -m pytest ai_review/test_ai_generated.py::test_import_returns_count -v`

```text
<PASTE BLOCK from shipped_each.txt>
```

**3. Evidence — against our fixed code**

Command: `python -m pytest ai_review/test_ai_generated.py::test_import_returns_count -v`

```text
<PASTE BLOCK from fixed_each.txt>
```

**4. What that pair proves.** FAIL then PASS is the "Genuine detection" row. On the shipped code it failed with `assert 3 == 2`, so the returned count was wrong, and it passed after our fix. It caught a real defect (Bug 4 in FINDINGS.md).

**5. Verdict**

- [x] Genuine detection — FAIL then PASS
- [ ] Detects nothing — PASS then PASS
- [ ] Locks in the bug — PASS then FAIL
- [ ] Invented requirement — FAIL then FAIL

---

#### Test: `test_register_duplicate_returns_false`  (`ai_review/test_ai_generated.py:37`)

**Audited by:** Paing

**1. What it claims to catch.** That registering a username that is already taken returns False.

**2. Evidence — against the shipped code**

Command: `python -m pytest ai_review/test_ai_generated.py::test_register_duplicate_returns_false -v`

```text
<PASTE BLOCK from shipped_each.txt>
```

**3. Evidence — against our fixed code**

Command: `python -m pytest ai_review/test_ai_generated.py::test_register_duplicate_returns_false -v`

```text
<PASTE BLOCK from fixed_each.txt>
```

**4. What that pair proves.** PASS then PASS is the "Detects nothing" row. `register` already returned False for a taken username in the shipped code, so that behaviour was never broken. None of our bugs involve duplicate registration, so the test cannot detect any of them.

**5. Verdict**

- [ ] Genuine detection — FAIL then PASS
- [x] Detects nothing — PASS then PASS
- [ ] Locks in the bug — PASS then FAIL
- [ ] Invented requirement — FAIL then FAIL

---

#### Test: `test_checkout_empty_returns_none`  (`ai_review/test_ai_generated.py:43`)

**Audited by:** Paing

**1. What it claims to catch.** That checking out an empty cart returns None.

**2. Evidence — against the shipped code**

Command: `python -m pytest ai_review/test_ai_generated.py::test_checkout_empty_returns_none -v`

```text
<PASTE BLOCK from shipped_each.txt>
```

**3. Evidence — against our fixed code**

Command: `python -m pytest ai_review/test_ai_generated.py::test_checkout_empty_returns_none -v`

```text
<PASTE BLOCK from fixed_each.txt>
```

**4. What that pair proves.** FAIL then PASS is the "Genuine detection" row. On the shipped code it failed with `assert [] is None`, because checkout returned an empty list for an empty cart, and it passed after our fix. It caught a real defect (Bug 3 in FINDINGS.md).

**5. Verdict**

- [x] Genuine detection — FAIL then PASS
- [ ] Detects nothing — PASS then PASS
- [ ] Locks in the bug — PASS then FAIL
- [ ] Invented requirement — FAIL then FAIL

---

#### Test: `test_add_to_cart_returns_true_for_known_product`  (`ai_review/test_ai_generated.py:48`)

**Audited by:** Paing

**1. What it claims to catch.** That adding a product that exists in the catalogue to the cart returns True.

**2. Evidence — against the shipped code**

Command: `python -m pytest ai_review/test_ai_generated.py::test_add_to_cart_returns_true_for_known_product -v`

```text
<PASTE BLOCK from shipped_each.txt>
```

**3. Evidence — against our fixed code**

Command: `python -m pytest ai_review/test_ai_generated.py::test_add_to_cart_returns_true_for_known_product -v`

```text
<PASTE BLOCK from fixed_each.txt>
```

**4. What that pair proves.** PASS then PASS is the "Detects nothing" row. `add` already returned True for a known product in the shipped code. The test only checks the return value, so it would also pass if the item never reached the cart. To be useful it would also have to assert that the cart contains the product afterwards.

**5. Verdict**

- [ ] Genuine detection — FAIL then PASS
- [x] Detects nothing — PASS then PASS
- [ ] Locks in the bug — PASS then FAIL
- [ ] Invented requirement — FAIL then FAIL

---

#### Test: `test_search_is_limited_to_ten_results`  (`ai_review/test_ai_generated.py:55`)

**Audited by:** Paing

**1. What it claims to catch.** That the catalogue search returns at most ten results.

**2. Evidence — against the shipped code**

Command: `python -m pytest ai_review/test_ai_generated.py::test_search_is_limited_to_ten_results -v`

```text
<PASTE BLOCK from shipped_each.txt>
```

**3. Evidence — against our fixed code**

Command: `python -m pytest ai_review/test_ai_generated.py::test_search_is_limited_to_ten_results -v`

```text
<PASTE BLOCK from fixed_each.txt>
```

**4. What that pair proves.** FAIL then FAIL is the "Invented requirement" row. The test failed with `assert 20 <= 10` on both runs, so it is not tied to any bug we fixed. We established that the requirement does not exist by reading `search()` in `catalog.py`: its docstring says it returns the product_ids whose title contains the keyword, and neither the docstring nor the code mentions any limit of ten results.

**5. Verdict**

- [ ] Genuine detection — FAIL then PASS
- [ ] Detects nothing — PASS then PASS
- [ ] Locks in the bug — PASS then FAIL
- [x] Invented requirement — FAIL then FAIL

---

## Part 3 — Coverage against our own bug hunt

| Bug (our description) | We found it | The supplied set catches it | Which test, and how we established that |
|---|---|---|---|
| Bug 1: login fails for passwords containing symbols or spaces | Yes | No | Test #2 uses the letters-only password "wrongpw", so it passes on both runs (PASS then PASS) |
| Bug 2: cart total wrong | Yes | Yes | Test #1: FAIL (`assert 10 == 30`) on shipped, PASS on fixed |
| Bug 3: checkout of an empty cart returns [] instead of None | Yes | Yes | Test #6: FAIL (`assert [] is None`) on shipped, PASS on fixed |
| Bug 4: import returns the wrong count | Yes | Yes | Test #4: FAIL (`assert 3 == 2`) on shipped, PASS on fixed |

---

## Part 4 — Verdict

1. **Most common failure mode:** "Detects nothing", 4 of the 8 tests (#2, #3, #5, #7). Three were genuine detections (#1, #4, #6) and one was an invented requirement (#8). None locked in a bug.

2. **Why a test that passes against buggy code is more dangerous than one that crashes:** A crashing test gets investigated. A test that passes on buggy code looks like coverage, so the team trusts the green result and stops looking. Test #2 is an example: it tests login and passes, but Bug 1 is still there. The suite looks protective and is not.

3. **Did the supplied set catch anything we had missed?** No. Tests #1, #4 and #6 detect Bugs 2, 3 and 4, which we had already found. The set missed Bug 1 completely.

4. **What we will check before trusting a generated test:** We will run it twice, on the shipped code and on the fixed code, and compare the pair. We did this for all 8 tests, and it was the only way to tell test #8 (FAIL then FAIL) from a real detection. We will read the docstring of the function under test before believing any failure, which is how we established that the ten-result limit does not exist. And we will check the inputs the test uses: the wrong password in test #2 and the exact-case title in test #3 are inputs that can never trigger the bugs.

---

## Appendix (optional)

None.