import pytest
from app import Figure

@pytest.mark.unit
def test_triangle_type():
    triangle = Figure("трикутник", 4)
    assert triangle.type == "трикутник"


def test_invalid_length():
    with pytest.raises(ValueError):
        Figure("квадрат", 0)


@pytest.mark.parametrize("figure", Figure.FIGURES)
def test_allowed_figure(figure):
    assert Figure(figure, 1).type == figure


@pytest.fixture
def square():
    return Figure("квадрат", 5)

def test_square_length(square):
    assert square.get_figure_length == 5


@pytest.fixture(scope="module")
def allowed_figures():
    return Figure.FIGURES

def test_allowed_figures_count(allowed_figures):
    assert len(allowed_figures) == 3

def test_allowed_figures_contains_square(allowed_figures):
    assert "квадрат" in allowed_figures