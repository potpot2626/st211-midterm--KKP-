"""Your test suite. Write smoke, regression, and slow tests here.

Every test MUST carry exactly one marker (@pytest.mark.smoke / regression /
slow) and name its author in the docstring, e.g.:

    @pytest.mark.smoke
    def test_login_works():
        '''Author: <name>. Smoke test for login.'''

Run:  pytest            (all)     pytest -m smoke     pytest -m regression
"""
import pytest
from bookstore_app import Users, Catalog, Cart


@pytest.mark.smoke
def test_example_register():
    """Author: Paing. Smoke: a new user can register."""
    assert Users().register("newuser", "password123") is True


# ---- YOUR SMOKE TESTS (at least 5) ----

@pytest.mark.smoke
def test_login_accepts_correct_and_rejects_wrong():
    """Author: Paing. Smoke: login works for the right password only."""
    u = Users()
    u.register("alice", "password123")
    assert u.login("alice", "password123") is True
    assert u.login("alice", "wrongpass") is False

@pytest.mark.smoke
def test_register_then_login():
    """Author: Paing. Smoke: a registered user is saved and can log in."""
    u = Users()
    assert u.register("bob", "password123") is True
    assert u.login("bob", "password123") is True


@pytest.mark.smoke
def test_add_product_is_saved():
    """Author: Paing. Smoke: an added product is stored in the catalog."""
    cat = Catalog()
    cat.add_product(1, "Python Book", 20)
    assert 1 in cat.products
    assert cat.products[1]["title"] == "Python Book"
    assert cat.products[1]["price"] == 20


@pytest.mark.smoke
def test_add_to_cart():
    """Author: Paing. Smoke: a product can be added to the cart."""
    cat = Catalog()
    cat.add_product(1, "Python Book", 20)
    cart = Cart(cat)
    assert cart.add(1) is True
    assert 1 in cart.items


@pytest.mark.smoke
def test_checkout_returns_order():
    """Author: Paing. Smoke: checkout of a non-empty cart returns the order."""
    cat = Catalog()
    cat.add_product(1, "Python Book", 20)
    cart = Cart(cat)
    cart.add(1)
    order = cart.checkout()
    assert order is not None
    assert 1 in order

# ---- YOUR REGRESSION TESTS (the bug hunt) ----

@pytest.mark.regression
def test_login_with_symbol_password():
    """Author: Paing. Regression: Users.login() strips non-alphanumeric
    characters from the typed password before comparing it. Observed:
    register("bob", "P@ss word!") then login("bob", "P@ss word!") returns
    False, and login("alice", "secret1!!!") is accepted when the stored
    password is "secret1". Expected: login compares the password exactly
    as typed, so the first returns True and the second returns False."""
    u = Users()
    u.register("bob", "P@ss word!")
    assert u.login("bob", "P@ss word!") is True

    u.register("alice", "secret1")
    assert u.login("alice", "secret1!!!") is False


@pytest.mark.regression
def test_cart_total_includes_last_item():
    """Author: Paing. Regression: Cart.total() skips the last item because
    the loop uses range(len(self.items) - 1). Observed: with items priced
    10, 20 and 30 in the cart, total() returned 30 (the first two items
    only). Expected: total() returns the sum of every item, so 60 here,
    and 10 for a cart holding one item priced 10."""
    cat = Catalog()
    cat.add_product(1, "A", 10)
    cat.add_product(2, "B", 20)
    cat.add_product(3, "C", 30)
    cart = Cart(cat)
    cart.add(1)
    cart.add(2)
    cart.add(3)
    assert cart.total() == 60

    single = Cart(cat)
    single.add(1)
    assert single.total() == 10

@pytest.mark.regression
def test_checkout_empty_cart_returns_none():
    """Author: Paing. Regression: Cart.checkout() does not handle an empty
    cart. Observed: checkout() on an empty cart returned [] and
    history() then returned [[]], so an empty order was recorded.
    Expected: checkout() returns None for an empty cart, and no order is
    added to the history."""
    cart = Cart(Catalog())
    assert cart.checkout() is None
    assert cart.history() == []

@pytest.mark.regression
def test_import_products_returns_correct_count():
    """Author: Paing. Regression: Cart.import_products() returns one more
    than the number of products imported. Observed: importing 2 products
    returned 3. Expected: it returns how many were imported, so 2, and
    both products are in the catalog."""
    cart = Cart(Catalog())
    count = cart.import_products([(1, "A", 5), (2, "B", 6)])
    assert count == 2
    assert len(cart.catalog.products) == 2

@pytest.mark.regression
def test_search_ignores_letter_case():
    """Author: Paing. Regression: Catalog.search() is case-sensitive.
    Observed: with a product titled "Python Book", search("book") returned []
    and search("python") did not find it. Expected: search returns every
    product whose title contains the keyword regardless of upper or lower
    case, so both calls return [1]."""
    cat = Catalog()
    cat.add_product(1, "Python Book", 10)
    assert cat.search("book") == [1]
    assert cat.search("python") == [1]

# ---- YOUR SLOW TESTS (at least 2) ----

@pytest.mark.slow
def test_bulk_import_one_million_products():
    """Author: Paing. Slow: bulk-importing 1,000,000 products stores every
    one of them in the catalog."""
    # Slow because import_products() loops 1,000,000 times and calls
    # time.sleep(0) on every iteration.
    cart = Cart(Catalog())
    products = [(i, f"Book {i}", 10) for i in range(1000000)]
    cart.import_products(products)
    assert len(cart.catalog.products) == 1000000
    assert cart.catalog.products[999999]["title"] == "Book 999999"


@pytest.mark.slow
def test_large_cart_checkout():
    """Author: Paing. Slow: a cart holding 500,000 items checks out as one
    order and is emptied afterwards."""
    # Slow because it first imports 500,000 products (one loop iteration and
    # time.sleep(0) each), then adds all 500,000 to the cart one by one.
    cart = Cart(Catalog())
    cart.import_products([(i, "Book", 2) for i in range(500000)])
    for i in range(500000):
        cart.add(i)
    order = cart.checkout()
    assert len(order) == 500000
    assert cart.items == []
    assert len(cart.history()) == 1

@pytest.mark.regression
@pytest.mark.slow
def test_large_order_total_includes_every_item():
    """Author: Paing. Regression + slow: with 300,000 items in the cart,
    total() must count every item. On the original code total() skipped the
    last item, so it returned 599998 instead of 600000."""
    # Slow because it imports 300,000 products (one loop iteration and
    # time.sleep(0) each), adds all of them to the cart one by one, and
    # then totals 300,000 items.
    cart = Cart(Catalog())
    cart.import_products([(i, "Book", 2) for i in range(300000)])
    for i in range(300000):
        cart.add(i)
    assert cart.total() == 600000