from ..images import Image


def test_castle_image():
    assert "Welcome to Cath's Cats' Castle!" in Image.CASTLE
    assert r"'---'--'-/___\-'--'---'" in Image.CASTLE


def test_cat_image():
    assert "Thank you for visiting. Please come again!" in Image.CAT
    assert r"|  | (   |        hjw | /" in Image.CAT
