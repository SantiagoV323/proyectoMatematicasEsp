import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import sympy as sp
import numpy as np
import sys

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
    if messagebox.askokcancel("Salir", "¿Estás seguro de que quieres cerrar el programa?"):
        root.destroy()
        sys.exit()

# Función para limpiar todo
def clear_all(entry, canvas):
    entry.delete(0, tk.END)
    set_placeholder(entry, "Ejemplo: z**2 + sqrt(z)")

    ax = canvas.figure.axes[0]
    ax.clear()
    ax.set_title("Visualización de Función Compleja")
    ax.set_xlabel("Re(z)")
    ax.set_ylabel("Im(z)")

    if len(canvas.figure.axes) > 1:
        canvas.figure.axes[1].remove()

    canvas.draw()

# Función para guardar la gráfica como imagen
def save_plot(canvas):
    file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("PNG files", "*.png"), ("All Files", "*.*")])
    if file_path:
        try:
            canvas.figure.savefig(file_path)
            messagebox.showinfo("Guardar", "La gráfica se ha guardado exitosamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la gráfica: {str(e)}")

# Función para verificar las ecuaciones de Cauchy-Riemann mejorada
def check_cauchy_riemann(func_str):
    try:
        # Definimos las variables simbólicas
        x, y = sp.symbols('x y', real=True)
        z = x + sp.I * y

        # Convertimos la función ingresada
        func = sp.sympify(func_str.replace('z', '(x + I*y)'))

        # Verificar si la función contiene el conjugado o abs(z)
        if 'conjugate' in func_str:
            messagebox.showinfo("Cauchy-Riemann", "La función NO cumple con las ecuaciones de Cauchy-Riemann (contiene conjugado).")
            return
        if 'Abs' in func_str or 'abs' in func_str:
            messagebox.showinfo("Cauchy-Riemann", "La función NO cumple con las ecuaciones de Cauchy-Riemann (contiene abs(z)).")
            return
        if 're' in func_str or 'im' in func_str:
            messagebox.showinfo("Cauchy-Riemann", "La función NO cumple con las ecuaciones de Cauchy-Riemann (usa re(z) o im(z)).")
            return

        # Obtenemos las partes real e imaginaria
        u = sp.re(func)
        v = sp.im(func)

        # Derivadas parciales
        du_dx = sp.diff(u, x)
        du_dy = sp.diff(u, y)
        dv_dx = sp.diff(v, x)
        dv_dy = sp.diff(v, y)

        # Comprobación de las ecuaciones de Cauchy-Riemann
        cr1 = sp.simplify(du_dx - dv_dy)
        cr2 = sp.simplify(du_dy + dv_dx)

        # Verificamos si ambas ecuaciones se cumplen
        if cr1 == 0 and cr2 == 0:
            messagebox.showinfo("Cauchy-Riemann", "La función cumple con las ecuaciones de Cauchy-Riemann.")
        else:
            messagebox.showinfo("Cauchy-Riemann", "La función NO cumple con las ecuaciones de Cauchy-Riemann.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al verificar las ecuaciones de Cauchy-Riemann: {str(e)}")

def main():
    root = tk.Tk()
    root.title("Visualizador de Funciones de Variables Complejas")
    root.geometry("900x750")
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

    # Botones principales
    frame_buttons_main = tk.Frame(root, bg="#f0f0f0")
    frame_buttons_main.pack(pady=10)

    btn_plot = tk.Button(frame_buttons_main, text="Graficar", font=font_style, bg="#007BFF", fg="white",
                         command=lambda: plot_function(entry_func.get(), canvas))
    btn_plot.pack(side=tk.LEFT, padx=5)

    btn_clear = tk.Button(frame_buttons_main, text="Limpiar Todo", font=font_style, bg="#FF5733", fg="white",
                          command=lambda: clear_all(entry_func, canvas))
    btn_clear.pack(side=tk.LEFT, padx=5)

    btn_check_cr = tk.Button(frame_buttons_main, text="Verificar Cauchy-Riemann", font=font_style, bg="#28A745", fg="white",
                             command=lambda: check_cauchy_riemann(entry_func.get()))
    btn_check_cr.pack(side=tk.LEFT, padx=5)

    btn_save = tk.Button(frame_buttons_main, text="Guardar Gráfica", font=font_style, bg="#28A745", fg="white",
                         command=lambda: save_plot(canvas))
    btn_save.pack(side=tk.LEFT, padx=5)

    # Botones para insertar funciones comunes
    frame_buttons_extra = tk.Frame(root, bg="#f0f0f0")
    frame_buttons_extra.pack(pady=10)

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
        btn = tk.Button(frame_buttons_extra, text=text, font=font_style, bg="#E0E0E0", fg="black",
                        command=lambda v=value: insert_text(entry_func, v))
        btn.pack(side=tk.LEFT, padx=5)

    frame_plot = tk.Frame(root, bg="#f0f0f0")
    frame_plot.pack(pady=20, fill=tk.BOTH, expand=True)

    fig, ax = plt.subplots()
    ax.set_title("Visualización de Función Compleja")
    ax.set_xlabel("Re(z)")
    ax.set_ylabel("Im(z)")
    canvas = FigureCanvasTkAgg(fig, master=frame_plot)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

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

        ax = canvas.figure.axes[0]
        ax.clear()

        # Utilizar colormap más suave como 'viridis' o 'coolwarm'
        im = ax.imshow(magnitude, extent=[x_min, x_max, x_min, x_max], origin='lower', cmap='Spectral', alpha=0.8)

        # Añadir la barra de color
        cbar = canvas.figure.colorbar(im, ax=ax)
        cbar.set_label('|f(z)|', fontsize=12)

        # Graficar líneas de flujo con color suave y menor grosor
        ax.streamplot(X, Y, U, V, color='darkblue', density=1.5, linewidth=1.4, arrowsize=1.5)

        # Añadir una cuadrícula tenue
        ax.grid(color='lightgrey', linestyle='--', linewidth=0.5)

        # Configurar títulos y etiquetas
        ax.set_title(f"Visualización de f(z) = {func_str}", fontsize=14)
        ax.set_xlabel("Re(z)")
        ax.set_ylabel("Im(z)")

        # Actualizar la gráfica
        canvas.draw()
    except Exception as e:
        messagebox.showerror("Error", "Por favor, revise su ecuación. Asegúrese de que sea válida.")


if __name__ == "__main__":
    main()

