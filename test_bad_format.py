"""Test file with intentional formatting errors."""


def test_function():
    # This is a very long comment that exceeds the 88 character limit and should cause flake8 to fail with E501 error because it's too long
    long_string = "This is a very long string literal that exceeds the 88 character limit and should cause flake8 to fail with E501 error because it's too long"
    return long_string
