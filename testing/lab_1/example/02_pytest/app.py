class Figure:
    FIGURES = ["трикутник", "квадрат", "прямокутник"]

    def __init__(self, figure_type: str, length: float):
        if length <= 0:
            raise ValueError("Довжина має бути більшою за нуль!")
        if figure_type not in self.FIGURES:
            raise ValueError(f"Невідомий тип фігури: {figure_type}")
        
        self.type = figure_type
        self.length = length

    @property
    def get_figure_length(self) -> float:
        return self.length