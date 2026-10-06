# REPORT.md

Group: KKP   Members: Paing

## Part A -- Test types

**Smoke test.** A small, fast check that the core features work at all. It runs on every push and before anything slower, so a broken build is caught in seconds. Bookstore examples: register a new user and get `True`; add a product to the catalog, add it to the cart and check out a non-empty cart, then check the returned order contains the item.

**Regression test.** A test written for a bug that was found, to prove the bug is fixed and to stop it coming back. It must fail on the buggy code and pass on the fixed code. It runs on every push or pull request, together with the smoke tests, and again in the full nightly run. Bookstore examples: logging in with the symbol password `"P@ss word!"` returns `True` (Bug 1); `total()` of a cart priced 10, 20 and 30 returns 60 and not 30 (Bug 2).

**Slow test.** A test that takes much longer than the others because it handles a lot of data or repeats an action many times. It is not run on every push; it runs in the scheduled nightly job, before a release, or on demand. Bookstore examples: importing 300,000 products and adding them all to a cart one by one; adding and removing items in a loop many thousands of times.

## Part B -- Scenario classification

1. **Password-reset email delivered within one minute: slow.** The test has to wait for a real email to arrive, which depends on an external mail system and takes up to a minute. That is far too slow to run on every push, so it belongs in the nightly or pre-release run.
2. **Previously fixed shipping-cost bug has not returned: regression.** The bug was already found and fixed, and the test exists only to make sure it does not come back. It should fail on the old buggy code and pass on the fixed code, and it is quick, so it runs on every push.
3. **Nightly job generating a sales report from ten years of orders: slow.** The point of the test is the huge amount of data, so it takes a long time by design. It matches the nightly schedule, so it runs in the nightly full suite and not on every push.
4. **Payment page loads after every deployment: smoke.** It checks that a critical feature works at all, it is quick, and it runs after every deployment as the first sanity check. If it fails there is no point running anything else.
5. **Refund issued twice must not credit the customer twice: regression.** It is a fault a customer already reported, so a test is written to make sure it never returns. It checks one specific wrong behaviour, so it is fast and runs on every push.
6. **Recommendation engine still responds with one million titles: slow.** The test is about performance with a very large catalogue, so it needs a large data set and takes a long time. It is also a kind of regression check on responsiveness, but its main character is slow, so it runs nightly.

## Part F -- Team reflection

1. **Why is running only regression tests before every commit inefficient?** Regression tests only cover bugs we already found. They say nothing about the features that have no bug report yet, such as registration or adding to the cart, so a new break could slip through. The set also grows with every bug fixed, so it gets slower, while a small smoke suite gives a faster check of the whole application.
2. **Why do smoke tests usually run first in a CI/CD pipeline?** They are fast and they check the most basic functions. If a smoke test fails, the build is broken at a basic level, and running the slower tests would waste time and compute. Failing early gives the team feedback in seconds.
3. **What risks arise if slow tests are never run?** Problems that only appear with large data or many operations stay hidden until real users hit them. For example, a bug in handling 300,000 items would never be seen, and performance problems would appear in production. Slow tests also tend to rot if nobody runs them.
4. **Can one test belong to two categories?** Yes. Markers describe characteristics, not exclusive boxes. In our suite `test_large_order_total_includes_every_item` is both regression and slow: it reproduces the cart-total bug that skipped the last item, and it uses 300,000 items.
5. **Bug-finders and bug-fixers are often different people. What does that change about a bug report?** The report must be written so someone who has not seen the bug can understand and reproduce it alone. It needs the exact function, the exact input, the observed result and the expected result with the reason it is correct, as in our `FINDINGS.md` entries. Phrases like "it does not work properly" are useless to a fixer who has to guess.

## Bonus -- one test with two markers

`test_large_order_total_includes_every_item` carries both `@pytest.mark.regression` and `@pytest.mark.slow`.

- **Why it is a regression test:** it reproduces Bug 2, where `Cart.total()` skipped the last item. On the shipped code it returns `599998` instead of `600000`, so it fails on the buggy code and passes after the fix.
- **Why it is slow:** it imports 300,000 products (one loop iteration and `time.sleep(0)` each), adds all of them to the cart one at a time, and then totals 300,000 items.
- **Where it belongs in CI/CD:** in the nightly full-suite job, not in the per-push smoke job. It still protects against the bug coming back, but it is too slow to run on every push.