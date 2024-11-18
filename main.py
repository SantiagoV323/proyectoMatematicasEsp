
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import sympy as sp
import numpy as np

def main():
    root = tk.Tk()
    root.title("Visualizador de Funciones de Variables Complejas")
    root.geometry("900x700")
    root.configure(bg="#f0f0f0")

    font_style = ("Helvetica", 12)
    title_font = ("Helvetica", 14, "bold")

    lbl_title = tk.Label(root, text="Visualizador de Funciones Complejas", font=title_font, bg="#f0f0f0", fg="#333")
    lbl_title.pack(pady=15)

    frame_input = tk.Frame(root, bg="#f0f0f0")
    frame_input.pack(pady=10)

    lbl_func = tk.Label(frame_input, text="Ingrese la función f(z):", font=font_style, bg="#f0f0f0")
    lbl_func.pack(side=tk.LEFT, padx=5)

    entry_func = tk.Entry(frame_input, font=("Helvetica", 12), width=40)
    entry_func.pack(side=tk.LEFT, padx=5)

    btn_plot = tk.Button(frame_input, text="Graficar", font=font_style, bg="#007BFF", fg="white",
                         command=lambda: plot_function(entry_func.get(), canvas))
    btn_plot.pack(side=tk.LEFT, padx=10)

    frame_range = tk.Frame(root, bg="#f0f0f0")
    frame_range.pack(pady=10)

    lbl_range = tk.Label(frame_range, text="Rango (mínimo y máximo):", font=font_style, bg="#f0f0f0")
    lbl_range.pack(side=tk.LEFT, padx=5)

    entry_min = tk.Entry(frame_range, font=("Helvetica", 12), width=10)
    entry_min.insert(0, "-10")
    entry_min.pack(side=tk.LEFT, padx=5)

    entry_max = tk.Entry(frame_range, font=("Helvetica", 12), width=10)
    entry_max.insert(0, "10")
    entry_max.pack(side=tk.LEFT, padx=5)

    frame_plot = tk.Frame(root, bg="#f0f0f0")
    frame_plot.pack(pady=20, fill=tk.BOTH, expand=True)

    fig, ax = plt.subplots()
    canvas = FigureCanvasTkAgg(fig, master=frame_plot)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    root.mainloop()

def plot_function(func_str, canvas):
    try:
        z = sp.symbols('z')
        func = sp.sympify(func_str)

        x_min, x_max = -10, 10
        x = np.linspace(x_min, x_max, 400)
        y = np.linspace(x_min, x_max, 400)
        X, Y = np.meshgrid(x, y)
        Z = X + 1j * Y

        f_Z = sp.lambdify(z, func, 'numpy')(Z)
        U = np.real(f_Z)
        V = np.imag(f_Z)

        magnitude = np.abs(f_Z)
        phase = np.angle(f_Z)

        ax = canvas.figure.axes[0]
        ax.clear()

        im = ax.imshow(magnitude, extent=[x_min, x_max, x_min, x_max], origin='lower', cmap='viridis', alpha=0.5)
        plt.colorbar(im, ax=ax, label='|f(z)|')

        ax.streamplot(X, Y, U, V, color='blue', density=1, linewidth=1, arrowsize=1.5)

        ax.set_title(f"Visualización de f(z) = {func_str}", fontsize=14)
        ax.set_xlabel("Re(z)")
        ax.set_ylabel("Im(z)")

        canvas.draw()
    except Exception as e:
        tk.messagebox.showerror("Error", f"Hubo un error al procesar la función:\n{e}")

if __name__ == "__main__":
    main()
