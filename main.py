import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import sympy as sp
import numpy as np
import sys  # Importar sys para salir del programa

# Función para insertar texto en el campo de entrada
def insert_text(entry, text):
    entry.insert(tk.END, text)

# Función para agregar un placeholder a un Entry
def set_placeholder(entry, placeholder_text):
    entry.insert(0, placeholder_text)
    entry.config(fg='grey')

    def on_focus_in(event):
        if entry.get() == placeholder_text:
            entry.delete(0, tk.END)
            entry.config(fg='black')

    def on_focus_out(event):
        if entry.get() == "":
            entry.insert(0, placeholder_text)
            entry.config(fg='grey')

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

# Función para manejar el cierre de la ventana
def on_closing(root):
    if tk.messagebox.askokcancel("Salir", "¿Estás seguro de que quieres cerrar el programa?"):
        root.destroy()  # Destruir la ventana de Tkinter
        sys.exit()  # Detener el script de Python

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

    # Agregar el placeholder al campo de entrada
    set_placeholder(entry_func, "Ejemplo: z**2 + sqrt(z)")

    btn_plot = tk.Button(frame_input, text="Graficar", font=font_style, bg="#007BFF", fg="white",
                         command=lambda: plot_function(entry_func.get(), canvas))
    btn_plot.pack(side=tk.LEFT, padx=10)

    frame_buttons = tk.Frame(root, bg="#f0f0f0")
    frame_buttons.pack(pady=10)

    buttons = [
        ("√", "sqrt("),
        ("e^", "exp("),
        ("ln", "log("),
        ("z²", "z**2"),
        ("|z|", "abs(z)"),
        ("sin", "sin("),
        ("cos", "cos("),
        ("tan", "tan(")
    ]

    for text, value in buttons:
        btn = tk.Button(frame_buttons, text=text, font=font_style, bg="#E0E0E0", fg="black",
                        command=lambda v=value: insert_text(entry_func, v))
        btn.pack(side=tk.LEFT, padx=5)

    frame_plot = tk.Frame(root, bg="#f0f0f0")
    frame_plot.pack(pady=20, fill=tk.BOTH, expand=True)

    fig, ax = plt.subplots()
    canvas = FigureCanvasTkAgg(fig, master=frame_plot)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Interceptar el evento de cierre
    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))

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
