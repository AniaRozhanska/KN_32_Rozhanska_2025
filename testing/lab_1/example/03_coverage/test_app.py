import sys
from pathlib import Path

# Fix import path
sys.path.append(str(Path(__file__).parent))

import pytest
from app import Figure


# Тест для квадрата
def test_square_angles():
    fig = Figure("квадрат", 5.0)
    assert fig.get_angles == 4


# Тест для прямокутника
def test_rectangle_angles():
    fig = Figure("прямокутник", 10.0)
    assert fig.get_angles == 4


# Тест для трикутника
def test_triangle_angles():
    fig = Figure("трикутник", 3.0)
    assert fig.get_angles == 3


# Тест для невідомої фігури (перевірка else -> 0)
def test_unknown_figure_angles():
    fig = Figure("коло", 2.0)
    assert fig.get_angles == 0


# Тест для помилки (некоректна довжина <= 0)
def test_invalid_length():
    with pytest.raises(ValueError):
        Figure("квадрат", 0)

    with pytest.raises(ValueError):
        Figure("квадрат", -5.0)