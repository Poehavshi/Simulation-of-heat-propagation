"""
Модель - представление данных для программы
Содержит:
* generate_exp_data - функция, которая генерирует данные вида (x, y), подходящие для отображения в matplotlib.
"""

# !TODO расчёт суммы ряда

import numpy as np
from scipy.special import jv, jn_zeros
from numpy import exp


def generate_exp_data(base, exponent):
    x = np.linspace(0, 10, 800)
    y = (x * base) ** exponent
    return x, y


class SumModel:
    def __init__(self,
                 R=4,
                 l=0.5,
                 u_c=0,
                 u_b=0,
                 alpha=0.005,
                 T=150,
                 k=0.065,
                 c=1.35
                 ):
        self.c = c
        self.k = k
        self.T = T
        self.alpha = alpha
        self.u_b = u_b
        self.u_c = u_c
        self.l = l
        self.R = R

        self.mu_array = jn_zeros(0, 50)

    def _calculate_term(self, n: int, r: float, t: float) -> float:
        """
        Функция подсчёта n-ого слагаемого суммы

        :param n: порядок слагаемого.
        :param r: аргумент функции w.
        :param t: аргумент функции w.

        :return значение одного слагаемого суммы
        """
        # mu_n = jn_zeros(0, n)[n - 1]
        mu_n = self.mu_array[n - 1]
        result = (5 * self.R * jv(1, self.R / 4)) / (mu_n ** 2 * (jv(1, mu_n)) ** 2)
        result *= exp(-(t * (self.l * self.k * (mu_n / self.R) ** 2) + 2 * self.alpha) / (self.l * self.c))
        result *= jv(0, (mu_n * r) / self.R)
        return result

    def phi(self, N, t):
        result = (self.R * 5) / (1 - exp(-(t * self.k) / (self.c * self.R ** 2)))
        result *= exp((-t * self.k * (N + 1)) / (self.c * self.R ** 2))
        return result

    def calculate_number_of_iterations(self, epsilon, t):
        N = 1
        while self.phi(N, t) < epsilon:
            N += 1
        return N

    def calculate_sum(self, r: float, t: float, N: int) -> float:
        """
        Функция подсчёта значения функции w(r, t)

        :param r: аргумент функции w.
        :param t: аргумент функции w.
        :param N: количество элементов ряда

        :return значение функции w(r,t)
        """
        result = 0
        for i in range(N):
            result += self._calculate_term(i + 1, r, t)
        return result

    def generate_w_data(self, r: int, p: str, N: int, x: int):
        """
        Генерирует значения функции w(r, t)

        :param N: количество элементов (точность подсчёта функции)
        :param t: фиксированный параметр t

        :return вектор двух numpy массивов
        """
        ox = np.linspace(0, x, 800)
        w = np.zeros(800)
        if p=='r':
            for i in range(800):
                w[i] = self.calculate_sum(r, ox[i], N)
        else:
            ox = np.linspace(0, x, 800)
            w = np.zeros(800)
            for i in range(800):
                w[i] = self.calculate_sum(ox[i], r, N)
        return ox, w


if __name__ == "__main__":
    model = SumModel()
    print(model.mu_array)
    print(exp())
