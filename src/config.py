"""
Стандартные значения для расчёта
"""
R = 4
l = 0.5
u_c = 0
u_b = 0
alpha = 0.005
T = 150
k = 0.065
c = 1.35


def psi(r):
    if 0 <= r <= R / 4:
        return 10
    return 0
