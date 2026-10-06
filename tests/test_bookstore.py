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
    """Author: <example>. Smoke: a new user can register."""
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
    
# ---- YOUR SLOW TESTS (at least 2) ----
