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

# Función para alternar entre módulo y fase
def toggle_plot_type(plot_type_var, canvas, ax, func_str):
    z = sp.symbols('z')
    func = sp.sympify(func_str)

    x_min, x_max = -10, 10
    x = np.linspace(x_min, x_max, 400)
    y = np.linspace(x_min, x_max, 400)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y

    f_Z = sp.lambdify(z, func, 'numpy')(Z)
    magnitude = np.abs(f_Z)
    phase = np.angle(f_Z)

    ax.clear()

    if plot_type_var.get() == "Módulo":
        im = ax.imshow(magnitude, extent=[x_min, x_max, x_min, x_max], origin='lower', cmap='viridis', alpha=0.8)
        ax.set_title(f"Módulo de f(z) = {func_str}")
    elif plot_type_var.get() == "Fase":
        im = ax.imshow(phase, extent=[x_min, x_max, x_min, x_max], origin='lower', cmap='twilight', alpha=0.8)
        ax.set_title(f"Fase de f(z) = {func_str}")

    ax.set_xlabel("Re(z)")
    ax.set_ylabel("Im(z)")

    canvas.figure.colorbar(im, ax=ax, orientation='vertical', label="|f(z)|" if plot_type_var.get() == "Módulo" else "Arg(f(z))")
    canvas.draw()

# Función para exportar la gráfica
def export_plot(canvas, filename="grafica_funcion.png"):
    canvas.figure.savefig(filename, dpi=300)
    tk.messagebox.showinfo("Exportar", f"La gráfica se ha guardado como {filename}")

# Función para detectar clics en el gráfico
def on_click(event, func_str):
    z = sp.symbols('z')
    try:
        x, y = event.xdata, event.ydata
        if x is not None and y is not None:
            func = sp.sympify(func_str)
            value = func.evalf(subs={z: complex(x, y)})
            real_part = sp.re(value)
            imag_part = sp.im(value)
            tk.messagebox.showinfo(
                "Punto seleccionado",
                f"Coordenadas:\nRe(z): {x:.2f}, Im(z): {y:.2f}\n\n"
                f"Valor de f(z):\nRe(f(z)): {real_part:.2f}, Im(f(z)): {imag_part:.2f}"
            )
    except Exception as e:
        tk.messagebox.showerror(
            "Error",
            f"Error al procesar el punto:\n{e}"
        )

# Función principal
def main():
    root = tk.Tk()
    root.title("Visualizador de Funciones de Variables Complejas")
    root.geometry("1000x750")
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

    set_placeholder(entry_func, "Ejemplo: z**2 + sqrt(z)")

    btn_plot = tk.Button(frame_input, text="Graficar", font=font_style, bg="#007BFF", fg="white",
                         command=lambda: toggle_plot_type(plot_type_var, canvas, ax, entry_func.get()))
    btn_plot.pack(side=tk.LEFT, padx=10)

    btn_export = tk.Button(frame_input, text="Exportar", font=font_style, bg="#28a745", fg="white",
                           command=lambda: export_plot(canvas))
    btn_export.pack(side=tk.LEFT, padx=10)

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

    frame_menu = tk.Frame(root, bg="#f0f0f0")
    frame_menu.pack(pady=10)

    plot_type_var = tk.StringVar(value="Módulo")
    tk.Radiobutton(frame_menu, text="Módulo", variable=plot_type_var, value="Módulo", bg="#f0f0f0",
                   font=font_style).pack(side=tk.LEFT, padx=5)
    tk.Radiobutton(frame_menu, text="Fase", variable=plot_type_var, value="Fase", bg="#f0f0f0",
                   font=font_style).pack(side=tk.LEFT, padx=5)

    frame_plot = tk.Frame(root, bg="#f0f0f0")
    frame_plot.pack(pady=20, fill=tk.BOTH, expand=True)

    fig, ax = plt.subplots()
    canvas = FigureCanvasTkAgg(fig, master=frame_plot)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    canvas.mpl_connect('button_press_event', lambda event: on_click(event, entry_func.get()))

    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))

    root.mainloop()

if __name__ == "__main__":
    main()
