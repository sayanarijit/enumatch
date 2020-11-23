import pytest
from enum import Enum
from enumatch import match, forall
import typing as t


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

    with pytest.raises(
        ValueError, match="missing possibilities: Color.green, Color.blue"
    ):
        match({Color.red: "Red"})


def test_match_invalid_input() -> None:

    with pytest.raises(TypeError, match="expecting a dict"):
        match(
            [  # type: ignore
                (Color.red, "Red"),
                (Color.green, "Green"),
                (Color.blue, "Blue"),
            ]
        )

    with pytest.raises(
        TypeError, match="the first key of the given dict must be an enum attribute"
    ):
        match({...: (255, 0, 0), Color.green: (0, 255, 0), Color.blue: (0, 0, 255)})


def test_nested() -> None:

    # matcher[r][g][b]: (int, int, int)
    matcher = match(
        {
            Color.red: match(
                {
                    Color.red: forall(Color, (255, 0, 0)),
                    Color.green: match(
                        {
                            Color.red: (255, 255, 0),
                            Color.green: (255, 255, 0),
                            Color.blue: (255, 255, 255),
                        }
                    ),
                    Color.blue: forall(Color, (255, 0, 0)),
                }
            ),
            Color.green: forall(Color, forall(Color, (0, 0, 0))),
            Color.blue: forall(Color, forall(Color, (0, 0, 0))),
        }
    )

    assert matcher[Color.red][Color.green][Color.blue] == (255, 255, 255)

    assert matcher[Color.red][Color.green][Color.red] == (255, 255, 0)
    assert matcher[Color.red][Color.green][Color.green] == (255, 255, 0)

    assert matcher[Color.red][Color.blue][Color.blue] == (255, 0, 0)
    assert matcher[Color.red][Color.red][Color.blue] == (255, 0, 0)

    assert matcher[Color.green][Color.green][Color.blue] == (0, 0, 0)
    assert matcher[Color.blue][Color.green][Color.blue] == (0, 0, 0)
