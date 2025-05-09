import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import calc

class Gui:
    def __init__(self):
        # Параметры
        self.parameters = {
            "length": ["Длина канала, мкм", 5],
            "width": ["Ширина канала, мкм", 5],
            "t_ox": ["Толщина подзатворного диэлектрика (SiO₂), мкм", 0.1],
            "n_d": ["Концентрация примеси в подложке, см⁻³", 1e15],
            "nu_n": ["Подвижность электронов в канале, см²/(В·с)", 1400],
            "n_ss": ["Плотность поверхностных состояний, см⁻²", 1e11],
            "n_plus": ["Концентрация примеси в контактных n⁺-слоях, см⁻³", 1e20],
            "x_j": ["Толщина контактных n⁺-слоев, мкм", 1],
        }
        # Создание GUI
        self.root = tk.Tk()
        self.root.title("MOSFET Plotter")

        # Конфигурация стилей
        self.style = ttk.Style()
        self.style.configure("TLabel", padding=6)
        self.style.configure("TEntry", padding=4)

        self.params_frame = ttk.Labelframe(self.root, text="Ввод параметров", relief="flat", borderwidth=1)
        self.params_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)

        self.frame = ttk.Frame(self.params_frame)
        self.frame.pack(padx=5, pady=5)

        # Создание полей ввода
        self.entries = {}
        for row, (key, (text, default)) in enumerate(self.parameters.items()):
            ttk.Label(self.frame, text=text).grid(row=row, column=0, sticky=tk.W, padx=5, pady=2)
            entry = ttk.Entry(self.frame)
            entry.insert(0, str(default))
            entry.grid(row=row, column=1, padx=5, pady=2)
            self.entries[key] = entry


        # Кнопка расчета
        ttk.Button(self.frame, text="Рассчитать", command=self.update_plot).grid(
            row=len(self.parameters)+1, column=0, columnspan=2, pady=10
        )

        # Область для графика
        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.pack(side=tk.RIGHT, padx=5, pady=5, fill=tk.BOTH)

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.canvas_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.ax.set_title("Выходная характеристика")
        self.ax.set_xlabel("Uси, В")
        self.ax.set_ylabel("Iс, мА")
        
        self.root.mainloop()

    def update_plot(self):
        x = calc.U_ds
        self.ax.clear()
        
        # Получение значений из полей 
        try:
            params = [float(entry[1]) for entry in self.parameters.values()]

            for i in range(5, 0, -1):  # U_gsi от 5 до 1 В
                y = [x * 1000 for x in calc.mosfet_vds(*params, U_gsi=i)]
                self.ax.plot(x, y, label=f"Uзи = {i}В")

        except ValueError as e:
            tk.messagebox.showerror("Ошибка ввода", f"Некорректное значение: {str(e)}")
        else:
            self.ax.set_title("Выходная характеристика")
            self.ax.set_xlabel("Uси, В")
            self.ax.set_ylabel("Iс, мА")
            self.ax.grid(axis='both')
            self.ax.legend()
            self.canvas.draw()


if __name__ == "__main__":
    Gui()
