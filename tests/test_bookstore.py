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


# ---- YOUR REGRESSION TESTS (the bug hunt) ----

# ---- YOUR SLOW TESTS (at least 2) ----
