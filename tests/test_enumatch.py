import pytest
from enum import Enum
from enumatch import match


class Color(Enum):

    red = "Red"
    green = "Green"
    blue = "Blue"


def test_match_all_possibilities() -> None:

    matcher = match(
        {Color.red: (255, 0, 0), Color.green: (0, 255, 0), Color.blue: (0, 0, 255)}
    )
    assert matcher[Color.red] == (255, 0, 0)
    assert matcher[Color.green] == (0, 255, 0)
    assert matcher[Color.blue] == (0, 0, 255)


def test_match_default() -> None:

    matcher = match({Color.red: "Red", ...: "Other than Red"})
    assert matcher[Color.red] == "Red"
    assert matcher[Color.green] == "Other than Red"
    assert matcher[Color.blue] == "Other than Red"


def test_match_missing_possibility() -> None:

    with pytest.raises(ValueError, match="missing possibility"):
        match({Color.red: "Red", Color.green: "Green"})


def test_match_invalid_input() -> None:

    with pytest.raises(TypeError, match="expecting a dict"):
        match([(Color.red, "Red"), (Color.green, "Green"), (Color.blue, "Blue")])  # type: ignore


    with pytest.raises(
        TypeError, match="the first key of the given dict must be an enum attribute"
    ):
        match({...: (255, 0, 0), Color.green: (0, 255, 0), Color.blue: (0, 0, 255)})
