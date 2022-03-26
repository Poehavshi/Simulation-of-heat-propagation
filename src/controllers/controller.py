"""
Является связью между моделью и представлением данных.
Реализует все основные расчёты и преобразует его в нужный для view формат.
Содержит:
* Controller - класс, который обрабатывает данные и получает/отправляет их модели и представлению.
"""

import tkinter as tk
from src.views.view import View
from src.models import model


class Controller:
    """
    Класс, который создаёт экземпляр представления и передаёт данные между
    моделью и представлением

    Все переменные передаваемые между model, view, и controller представлены в формате:
        values = {'base': b, 'exponent': e}
    где b и e - float.

    Контроллер предполагает, что модель принимает values dict и возвращает кортеж
    из np.array вида (x, y), который подходит для отрисовки библиотекой matplotlib

    Контроллер предполагает, что у представления есть данные методы:
    * set_values(values) - используется для первоначальной инициализации view
    * clear() и .plot(x, y) для очисти холста и отрисовки данных (x, y).
    Контроллер предоставляет следующие методы для использования представлением:
    * update_view - Обновляет данные для отрисовки и обновляет plot в представлении
    """

    def __init__(self, root: tk.Tk):
        """
        :param root: tkinter.Tk() объект, который используется представлением.
        """
        self.plot_data = None
        self.view = View(root, self)
        self.default_values = {'base': 1, 'exponent': 2}
        self.initialize_view()

    def initialize_view(self):
        """
        Инициализирует поля ввода и рисует график на холсте.
        """
        self.view.set_values(self.default_values)
        self.update_view(self.default_values)

    def update_view(self, values: dict):
        """
        Запрашивает x и y для отрисовки графика из модели, и обновляет график в View новыми данными

        :param values: значения для графика
        """
        self.get_plot_data(values)
        self.update_view_plot()

    def get_plot_data(self, values: dict):
        """
        Отправляет данные в модель и сохраняет данные, которые модель вернула.

        :param values: словарь с данным от модели
        """
        self.plot_data = model.generate_exp_data(**values)

    def update_view_plot(self):
        """
        Вызывает методы View для очистки и перерисовки графика
        использует копию данных для отрисовки от контроллера.
        """
        self.view.canvas.clear()
        self.view.canvas.plot(*self.plot_data)


if __name__ == '__main__':
    root = tk.Tk()
    app = Controller(root)
    root.mainloop()
