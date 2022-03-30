import matplotlib as mpl
import tkinter as tk

import numpy as np
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)  # NavigationToolbar2TkAgg является устаревшим
from tkinter import ttk

mpl.use("TkAgg")


class MPLgraph(FigureCanvasTkAgg):
    """
    Matplotlib объект похожий на tk.Canvas()
    Используется объектом View для отображения графика
    """

    def __init__(self, figure: mpl.figure.Figure, parent=None, **options):
        """
        :param figure: область на которой происходит отрисовка графика
        """
        FigureCanvasTkAgg.__init__(self, figure, parent, **options)
        self.figure = figure
        self.add = figure.add_subplot(111)
        # .show() является устаревшим и заменён на .draw(). См.:
        # https://github.com/matplotlib/matplotlib/pull/9275
        self.draw()
        self.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.toolbar = NavigationToolbar2Tk(self, parent)
        self.toolbar.update()

    def plot(self, x: np.array, y: np.array):
        """
        Берёт массивы координат x и y, по ним рисует графики.
        """
        self.add.plot(x, y)
        self.figure.canvas.draw()

    def clear(self):
        """
        Очищает область с графиком.
        """
        self.add.clear()
        self.figure.canvas.draw()


class View(ttk.Frame):
    """
    Tkinter GUI с двумя областями ввода ("base" и "exponent") и
    холстом (canvas) matplotlib

    Представление предполагает, что у контроллера есть метод update_view(), который принимает
    переменные в формате:

    values = {'base': b, 'exponent': e}

    где b и e - float,
    и возвращает (x, y) кортеж из numpy.array.

    Предоставление содержит следующие методы для внешнего использования контроллером:

    * set_values используется для первоначальной инициализации представления
    * clear  очищает MPLgraph plot
    * plot рисует данные формата (x, y) кортежа из numpy.array
    """

    def __init__(self, parent, controller, param_name, **options):
        """
        Создаёт необходимые виджеты и словарь self.values для хранения
        состояний полей ввода в формате:
            {'base': b, 'exponent': e}
        где b и e - float.

        :param parent: виджет-родитель
        :param controller: объект с update_view методом
        """
        ttk.Frame.__init__(self, parent, **options)
        self.canvas = None
        self.figure = None
        self.named_param = None
        self.named_param_entry = None
        self.param_name = param_name

        self.countN = None
        self.countN_entry = None
        self.pack()

        self.parent = parent
        self.controller = controller
        self.values = {}

        self.create_entries()
        self.create_bindings()
        self.create_canvas()

    def create_entries(self):
        """
        Создаёт поля ввода и связанные с ними лейблы в View, также привязывает
        StringVar объекты к виджетам поля ввода.
        """
        self.countN_entry = self.add_entry('N')
        self.countN = tk.StringVar()
        self.countN_entry.config(textvariable=self.countN)
        self.countN_entry.focus_set()

        self.named_param_entry = self.add_entry(self.param_name)
        self.named_param = tk.StringVar()
        self.named_param_entry.config(textvariable=self.named_param)



    def add_entry(self, text: str):
        """
        Создаёт пару виджетов лейбла и поля ввода


        :param text: строка с текстом для лейбла, поля ввода и для ключа в self.values словаре.

        :return entry: созданный ttk.Entry объект
        """
        ttk.Label(self, text=text).pack(side=tk.LEFT)

        # проверка каждого нажатия клавиши на ввод числового значения в поле ввода
        entry = ttk.Entry(self, validate='key')
        entry['validatecommand'] = (self.register(self.is_number_or_empty),
                                    '%P')
        entry['invalidcommand'] = 'bell'  # звуковой сигнал, если нажали неправильно
        entry.pack(side=tk.LEFT)
        return entry

    def is_number_or_empty(self, entry: str) -> bool:
        """
        Проверяет (например по нажатию клавиши) чтобы увидеть, что состояние поле ввода является приемлемым
        (не пустым и возможным для конвертации во float)

        :param entry: строка, которую нужно проверить.
        :return: является ли строка правильной
        """
        return self.is_number(entry) or self.is_empty(entry)

    @staticmethod
    def is_number(entry: str) -> bool:
        """
        Проверка ввода на число

        :param entry: строка, которая должна содержать число.
        :return: число ли в аргументе
        """
        try:
            float(entry)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_empty(entry):
        if not entry:
            return True
        return False

    def create_bindings(self):
        """
        Привязывает события ко всем entry виджетам (полям ввода)
        """
        self.bind_class('TEntry', '<FocusIn>',
                        lambda event: self.on_focus_in(event))
        self.bind_class('TEntry', '<Return>',
                        lambda event: self.on_value_entry(event))
        self.bind_class('TEntry', '<Tab>', lambda event: self.on_tab(event))
        self.bind_class('TEntry', '<FocusOut>',
                        lambda event: self.refresh())

    @staticmethod
    def on_focus_in(event):
        """
        Выбирает содержимое поля ввода под фокусом для более простого редактирования его содержимого
        """
        event.widget.selection_range(0, tk.END)

    def on_value_entry(self, event):
        """
        Когда подходящее изменение было внесено в поле ввода,
        запрашивает обновления представления и ставит фокус на следующем подходящем виджете
        """
        self.refresh()
        self.set_next_focus(event.widget.tk_focusNext())

    def refresh(self):
        """
        Переписывает self.values и запрашивает обновление графика, но только в том случае,
        если было изменено значение в поле ввода.
        """
        if self.entry_is_changed():
            self.update_values()
            self.controller.update_view(self.values)

    def entry_is_changed(self) -> bool:
        """
        Сравнивает текущие значения в виджете полей ввода со значениями в словаре,
        который хранит предыдущие значения.

        :return изменились ли значения в entry
        """
        if self.get_current_values() != self.values:
            return True
        return False

    def get_current_values(self) -> dict:
        """
        Получает текущие значения в виджете

        :return значения base и exponent в виджете
        """
        return {'N': int(self.countN.get()),
                self.param_name: int(self.named_param.get())}

    def update_values(self):
        """
        Переписывает словарь с предыдущими значениями в поле ввода текущими значениями
        """
        self.values = self.get_current_values()

    def set_next_focus(self, next_widget):
        """
        Начиная с next_widget, перемещается по всем виджетам, пока не найдет
        Entry - поле ввода. Нужен, чтобы игнорировать все остальные matplotlib виджеты

        :param next_widget: виджет, с которого нужно начать итерацию
        """
        if type(next_widget) is not ttk.Entry:
            self.set_next_focus(next_widget.tk_focusNext())
        else:
            next_widget.focus()

    def on_tab(self, event):
        """

        Обёртка для on_value_entry; нужен, чтобы переписать стандартное поведение клавиши Tab
        """
        self.on_value_entry(event)
        return 'break'

    def create_canvas(self):
        """
        Добавляет виджет MPLgraph в нижнюю часть View.
        """
        self.figure = mpl.figure.Figure(figsize=(5, 4), dpi=100)
        self.canvas = MPLgraph(self.figure, self.parent)
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, expand=tk.YES, fill=tk.BOTH)

    # Три метода ниже предоставляют интерфейс для контроллера
    def set_values(self, values: dict):
        """
        Используется контроллером для инициализации значений по умолчанию

        :param values: значения по умолчанию
        """
        self.countN.set(values['N'])
        self.named_param.set(values[self.param_name])
        self.values = values

    def clear(self):
        """
        Очищает matplotlib canvas.
        """
        self.canvas.clear()

    def plot(self, x: np.array, y: np.array):
        """
        Рисует данные из модели на холст (canvas) matplotlib

        :param x - значения координаты x
        :param y - значения координаты y
        """
        self.canvas.plot(x, y)


if __name__ == '__main__':
    root = tk.Tk()
    app = View(root, controller=None, param_name='t')
    root.mainloop()
