import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import sympy as sp
import numpy as np

# Función principal
def main():
    # Crear la ventana principal
    root = tk.Tk()
    root.title("Visualizador de Funciones de Variables Complejas")
    root.geometry("800x600")

    # Etiqueta y campo de entrada para la función
    lbl_func = tk.Label(root, text="Ingrese la función f(z):")
    lbl_func.pack(pady=10)

    entry_func = tk.Entry(root, width=50)
    entry_func.pack(pady=5)

    # Botón para generar la gráfica
    btn_plot = tk.Button(root, text="Graficar", command=lambda: plot_function(entry_func.get(), canvas))
    btn_plot.pack(pady=10)

    # Área para la gráfica
    fig, ax = plt.subplots()
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Ejecutar el loop principal
    root.mainloop()

# Función para graficar
def plot_function(func_str, canvas):
    try:
        z = sp.symbols('z')
        func = sp.sympify(func_str)

        # Crear una malla de puntos en el plano complejo
        x = np.linspace(-10, 10, 400)
        y = np.linspace(-10, 10, 400)
        X, Y = np.meshgrid(x, y)
        Z = X + 1j * Y

        # Evaluar la función
        f_Z = sp.lambdify(z, func, 'numpy')(Z)

        # Obtener partes reales e imaginarias
        U = np.real(f_Z)
        V = np.imag(f_Z)

        # Obtener módulo y fase
        magnitude = np.abs(f_Z)
        phase = np.angle(f_Z)

        # Limpiar la gráfica anterior
        ax = canvas.figure.axes[0]
        ax.clear()

        # Graficar módulo como fondo
        im = ax.imshow(magnitude, extent=[-10,10,-10,10], origin='lower', cmap='viridis', alpha=0.5)
        plt.colorbar(im, ax=ax, label='|f(z)|')

        # Graficar líneas de flujo
        ax.streamplot(X, Y, U, V, color='blue', density=1, linewidth=1, arrowsize=1.5)

        ax.set_title(f"Visualización de f(z) = {func_str}")
        ax.set_xlabel("Re(z)")
        ax.set_ylabel("Im(z)")

        # Actualizar la gráfica
        canvas.draw()
    except Exception as e:
        messagebox.showerror("Error", f"Hubo un error al procesar la función:\n{e}")

if __name__ == "__main__":
    main()
