class Figure:
    def __init__(self, figure_type: str, length: float):
        if length <= 0:
            raise ValueError("Довжина має бути більшою за нуль!")
        self.type = figure_type
        self.length = length

    @property
    def get_angles(self) -> int:
        fig_type = self.type.lower()
        if fig_type == "квадрат":
            return 4
        elif fig_type == "прямокутник":
            return 4
        elif fig_type == "трикутник":
            return 3
        else:
            return 0


if __name__ == "__main__":  # pragma: no cover
    fig = Figure("квадрат", 5)
    print(f"Кількість кутів: {fig.get_angles}")