"""
Является связью между моделью и представлением данных.
Реализует все основные расчёты и преобразует его в нужный для view формат.
Содержит:
* Controller - класс, который обрабатывает данные и получает/отправляет их модели и представлению.
"""

import tkinter as tk
from views.view import View
from models import model


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

    def __init__(self, root_tk: tk.Tk):
        """
        :param root_tk: tkinter.Tk() объект, который используется представлением.
        """
        self.lbl = 1
        self.plot_data = None
        self.view = View(root_tk, self)
        self.default_values = {'N': 6, 'K':'N', 'E' : 0.01, 'p': 'r', 'r':0,'x':150} 
        self.colors = ['red','blue','black','green','yellow','orange','purple']
        self.color_id = 0
        self.initialize_view()

    def get_current_color(self):
        if (self.color_id>=len(self.colors)):
            self.color_id = 0
        return self.colors[self.color_id]

    def initialize_view(self):
        """
        Инициализирует поля ввода и рисует график на холсте.
        """
        summodel = model.SumModel()
        if (self.default_values['K']=='E'):
            self.default_values['N'] = summodel.calculate_number_of_iterations(self.default_values['E'],self.default_values['r'])
        #else:
        #    self.default_values['E'] = summodel.calculate_eps_of_iterations(self.default_values['N'],self.default_values['r'])
        self.default_values['p'] = self.view.get_type()
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
        summodel = model.SumModel()
        if (values['K']=='E'):
            values['N'] = summodel.calculate_number_of_iterations(values['E'],values['r'])
        #else:
        #    values['E'] = summodel.calculate_eps_of_iterations(values['N'],values['r'])
        self.lbl = str("N=" + str(values['N']) +" " +str(values['p'])+ "="+str(values['r']))
        self.plot_data = summodel.generate_w_data(values['N'],values['r'],values['p'],values['x'],values["E"])


    def updateN(self, eps, t):
        summodel = model.SumModel()
        return summodel.calculate_number_of_iterations(eps,t)

    def updateEps(self, N, t):
        summodel = model.SumModel()
        return summodel.calculate_eps_of_iterations(N,t)

    def update_view_plot(self):
        """
        Вызывает методы View для очистки и перерисовки графика
        использует копию данных для отрисовки от контроллера.
        """
        #self.view.canvas.clear()
        self.view.canvas.plot(self.plot_data[0],self.plot_data[1],color=self.get_current_color(),label = self.lbl)
        self.color_id += 1


if __name__ == '__main__':
    root = tk.Tk()
    app = Controller(root)
    root.mainloop()
