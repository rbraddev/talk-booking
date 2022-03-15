from models import Address


def test_address_attributes():
    """
    GIVEN street, city, state, country
    WHEN Address is initialized
    THEN it has attributes with the same values as provided
    """

    address = Address(
        street="Know Your Role Boulevard",
        city="Las Vegas",
        state="Nevada",
        country="USA",
    )

    assert address.street == "Know Your Role Boulevard"
    assert address.city == "Las Vegas"
    assert address.state == "Nevada"
