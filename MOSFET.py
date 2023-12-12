import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# константы для расчётов
q_el = 1.62e-19                 # заряд электрона
eps_0 = 8.85e-14                # диэлектрическая проницаемость вакуума
eps_si = 11.9                   # относительная проницаемость Si
eps_sio2 = 3.4                  # относительная проницаемость диэлектрика
electric_field_channel = 1.5e4  # продольное электрическое поле в канале
U_t = 1                         # пороговое напряжение

U_ds = np.linspace(0, 5, 100)   #Напряжение drain-source

def mosfet_vds (length = 5, width = 5, d_sio2 = 0.1, n_b = 10e15, nu_el = 700, n_ss = 10e11, n_max = 10e20, xj = 1, U_gsi = (U_t + 1)):
    '''Расчёт выходной характеристики МДПт с вводом параметров:
    lenght - длина канала, мкм;
    width - ширина канала, мкм;
    d_sio2 - Толщина подзатворного диэлектрика (SiO 2 ), мкм;
    n_b - Концентрация примеси в подложке, см -3;
    nu_el - Подвижность электронов в канале, см 2 /В.с;
    n_ss - Плотность поверхностных состояний, см -2;
    n_max - Концентрация примеси в контактных n+ - слоях, см -3;
    xj - Толщина контактных п + -слоев, мкм;
    u_gsi - Напряжение gate-source в данный момент, В;
    '''

    C_s = eps_0 * eps_si / d_sio2
    beta = C_s * nu_el * width / length
    I_d = [(beta * U_dsi * ((U_gsi - U_t) - U_dsi/2) if U_gsi > U_t and U_dsi <= (U_gsi - U_t) else (beta * (U_gsi - U_t)**2) / 2) for U_dsi in U_ds]
    return(I_d)

def update_plot():
    x = U_ds
    ax.clear()
    ax.set_title("Выходная характеристика")
    ax.set_xlabel("Uси, В")
    ax.set_ylabel("Iс, А")
    
    try:
        param1 = float(entry1.get() or 5)
        param2 = float(entry2.get() or 5)
        param3 = float(entry3.get() or 0.1)
        param4 = float(entry4.get() or 10e15)
        param5 = float(entry5.get() or 700)
        param6 = float(entry6.get() or 10e11)
        param7 = float(entry7.get() or 10e20)
        param8 = float(entry8.get() or 1 )

        for i in range(5, 0, -1): #Напряжение gate-source для выходной характеристики
            y = mosfet_vds(param1, param2, param3, param4, param5, param6, param7, param8, U_gsi=i)
            ax.plot(x, y, label = f'Uзи = {i}В')

    except ValueError:
        y = mosfet_vds()

    ax.grid()
    plt.legend()
    canvas.draw()

# GUI
root = tk.Tk()
root.title("MOSFET Plotter")

frame = tk.Frame(root)
frame.pack(side=tk.LEFT, padx=10, pady=10)

# Ввод параметров
label1 = tk.Label(frame, text='Введите длину канала, мкм')
label1.grid(row=0, column=0, pady=5)
entry1 = tk.Entry(frame)
entry1.grid(row=0, column=1, pady=5)

label2 = tk.Label(frame, text='Введите ширину канала, мкм')
label2.grid(row=1, column=0, pady=5)
entry2 = tk.Entry(frame)
entry2.grid(row=1, column=1, pady=5)

label3 = tk.Label(frame, text='Введите толщину подзатворного диэлектрика (SiO 2 ), мкм')
label3.grid(row=2, column=0, pady=5)
entry3 = tk.Entry(frame)
entry3.grid(row=2, column=1, pady=5)

label4 = tk.Label(frame, text='Введите концентрацию примеси в подложке, см -3')
label4.grid(row=3, column=0, pady=5)
entry4 = tk.Entry(frame)
entry4.grid(row=3, column=1, pady=5)

label5 = tk.Label(frame, text='Введите подвижность электронов в канале, см 2 /В.с')
label5.grid(row=4, column=0, pady=5)
entry5 = tk.Entry(frame)
entry5.grid(row=4, column=1, pady=5)

label6 = tk.Label(frame, text='Введите плотность поверхностных состояний, см -2')
label6.grid(row=5, column=0, pady=5)
entry6 = tk.Entry(frame)
entry6.grid(row=5, column=1, pady=5)

label7 = tk.Label(frame, text='Введите концентрацию примеси в контактных n+ - слоях, см -3')
label7.grid(row=6, column=0, pady=5)
entry7 = tk.Entry(frame)
entry7.grid(row=6, column=1, pady=5)

label8 = tk.Label(frame, text='Введите толщину контактных п + -слоев, мкм')
label8.grid(row=7, column=0, pady=5)
entry8 = tk.Entry(frame)
entry8.grid(row=7, column=1, pady=5)

# Кнопка
calculate_button = tk.Button(frame, text="Рассчитать", command=update_plot)
calculate_button.grid(row=8, column=0, columnspan=2, pady=10)

# График
canvas_frame = tk.Frame(root)
canvas_frame.pack(side=tk.RIGHT, padx=10, pady=10)

fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
canvas_widget = canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

#запуск GUI
root.mainloop()
