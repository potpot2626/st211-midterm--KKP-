# FINDINGS.md -- Bug-hunt log

Group: KKP   Members: Paing

Each bug below was reproduced with a regression test that FAILS on a clean copy of the shipped code and PASSES after the fix.

---

## Bug 1
- **Suspected:** `Users.login()` in `users.py`. The docstring says it returns True if the password matches, but the code builds a `cleaned` version of the typed password with only letters and digits and compares that instead.
- **Tried:** `u.register("bob", "P@ss word!")` then `u.login("bob", "P@ss word!")`. Also `login("alice", "secret1!!!")` when the stored password is `"secret1"`.
- **Observed:** `login("bob", "P@ss word!")` returned `False`. `login("alice", "secret1!!!")` was accepted although the stored password is `"secret1"` (`assert False is True` in the regression test).
- **Expected:** `login` compares the password exactly as typed. The first call returns `True` and the second returns `False`, because the docstring says the password must match.
- **Fixed:** removed the `cleaned` step and compared `stored == password`.
- **Author:** Paing

---

## Bug 2
- **Suspected:** `Cart.total()` in `cart.py`. The loop is `range(len(self.items) - 1)`, which looks like an off-by-one that stops before the last item.
- **Tried:** a catalog with products priced 10, 20 and 30, all three added to the cart. Also a cart of 300,000 items priced 2.
- **Observed:** `total()` returned `30`, should be `60` (the last item is skipped). With 300,000 items it returned `599998`, should be `600000`.
- **Expected:** `total()` returns the sum of every item currently in the cart, as its docstring says ("Total price of everything currently in the cart").
- **Fixed:** the loop now runs over every item (`range(len(self.items))`).
- **Author:** Paing

---

## Bug 3
- **Suspected:** `Cart.checkout()` in `cart.py`. The docstring says it returns None if the cart is empty, but the code has no empty-cart check at all.
- **Tried:** `Cart(Catalog()).checkout()` on a cart with nothing in it, then `history()`.
- **Observed:** `checkout()` returned `[]` (`assert [] is None`), and `history()` then returned `[[]]`, so an empty order was recorded.
- **Expected:** `checkout()` returns `None` for an empty cart and no order is added to the history, because the docstring says so.
- **Fixed:** added an early `return None` when `self.items` is empty, before the order is appended.
- **Author:** Paing

---

## Bug 4
- **Suspected:** `Cart.import_products()` in `cart.py`. The function counts imported products in `count`, but the last line is `return count + 1`.
- **Tried:** `cart.import_products([(1, "A", 5), (2, "B", 6)])`.
- **Observed:** it returned `3` (`assert 3 == 2`).
- **Expected:** it returns how many products were imported, so `2`. The docstring says "Returns how many were imported."
- **Fixed:** changed the return to `return count`.
- **Author:** Paing

---

## Bug 5
- **Suspected:** `Catalog.search()` in `catalog.py`. The docstring says it returns the products whose title contains the keyword, but the check `keyword in info["title"]` compares exact capitalisation.
- **Tried:** two products, `add_product(1, "Python Book", 10)` and `add_product(2, "python basics", 5)`, then `search("Python")`, `search("python")` and `search("book")`.
- **Observed:** `search("Python")` returned `[1]`, `search("python")` returned `[2]`, and `search("book")` returned `[]` although "Python Book" contains the word book. The result depends on letter case.
- **Expected:** `search` returns every product whose title contains the keyword regardless of upper or lower case, so `search("book")` returns `[1]` and `search("python")` returns `[1, 2]`. A bookstore customer typing a lowercase word must still find the book.
- **Fixed:** compared the lowercase versions: `if keyword.lower() in info["title"].lower():`.
- **Author:** Paing