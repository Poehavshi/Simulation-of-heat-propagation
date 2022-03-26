"""
Модель - представление данных для программы
Содержит:
* generate_exp_data - функция, которая генерирует данные вида (x, y), подходящие для отображения в matplotlib.
"""

import numpy as np


def generate_exp_data(base, exponent):
    x = np.linspace(0, 10, 800)
    y = (x * base) ** exponent
    return x, y
