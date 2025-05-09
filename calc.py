import numpy as np
from constants import (
    vacuum_permittivity,
    silicon_dioxide_permittivity,
)

U_t = 0.7  # пороговое напряжение
U_ds = np.linspace(0, 5, 100)  # Напряжение drain-source

def mosfet_vds(length, width, d_sio2, n_b, nu_el, n_ss, n_max, xj, U_gsi=(U_t + 1)):
    """
    Расчёт выходной характеристики МДПт
    """
    # Преобразование единиц в СИ
    length = length * 1e-6  # мкм -> м
    width = width * 1e-6  # мкм -> м
    d_sio2 = d_sio2 * 1e-6  # мкм -> м
    nu_el = nu_el * 1e-4  # см²/(В·с) -> м²/(В·с)

    # Расчет емкости затвора
    C_ox = (vacuum_permittivity * silicon_dioxide_permittivity) / d_sio2
    beta = C_ox * nu_el * (width / length)

    I_d = [
        # Линейный режим
        beta * ((U_gsi - U_t) * U_dsi - 0.5 * U_dsi**2)
        if U_gsi > U_t and U_dsi <= (U_gsi - U_t)
        else
        # Режим насыщения
        0.5 * beta * (U_gsi - U_t) ** 2
        for U_dsi in U_ds
    ]

    return I_d
