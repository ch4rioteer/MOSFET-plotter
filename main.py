import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from constants import (
    vacuum_permittivity,
    silicon_permittivity,
    silicon_dioxide_permittivity,
)

U_t = 0.7  # пороговое напряжение
U_ds = np.linspace(0, 5, 100)  # Напряжение drain-source

# Изменено на списки и правильный порядок параметров
labels = {
    "length": ["Длина канала, мкм", 5],
    "width": ["Ширина канала, мкм", 5],
    "t_ox": ["Толщина подзатворного диэлектрика (SiO₂), мкм", 0.1],
    "n_d": ["Концентрация примеси в подложке, см⁻³", 1e15],
    "nu_n": ["Подвижность электронов в канале, см²/(В·с)", 1400],
    "n_ss": ["Плотность поверхностных состояний, см⁻²", 1e11],
    "n_max": ["Концентрация примеси в контактных n⁺-слоях, см⁻³", 1e20],
    "x_j": ["Толщина контактных n⁺-слоев, мкм", 1],
}


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


def update_plot():
    x = U_ds
    ax.clear()
    ax.set_title("Выходная характеристика")
    ax.set_xlabel("Uси, В")
    ax.set_ylabel("Iс, А")

    # Получение значений из полей ввода
    params = [float(entry[1].get()) for entry in labels.values()]

    for i in range(5, 0, -1):  # U_gsi от 5 до 1 В
        y = mosfet_vds(*params, U_gsi=i)
        ax.plot(x, y, label=f"Uзи = {i}В")

    ax.grid()
    ax.legend()
    canvas.draw()


# Создание GUI
root = tk.Tk()
root.title("MOSFET Plotter")

frame = tk.Frame(root)
frame.pack(side=tk.LEFT, padx=10, pady=10)

# Создание полей ввода
row_num = 0
for key, value in labels.items():
    label_text, default_value = value[0], value[1]
    tk.Label(frame, text=label_text).grid(row=row_num, column=0, sticky=tk.W)
    entry = tk.Entry(frame)
    entry.insert(0, str(default_value))
    entry.grid(row=row_num, column=1)
    labels[key][1] = entry
    row_num += 1

# Кнопка расчета
tk.Button(frame, text="Рассчитать", command=update_plot).grid(
    row=row_num, column=0, columnspan=2, pady=10
)

# Область для графика
canvas_frame = tk.Frame(root)
canvas_frame.pack(side=tk.RIGHT, padx=10, pady=10)

fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

root.mainloop()
