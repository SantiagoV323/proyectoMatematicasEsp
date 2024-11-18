
# Visualizador de Funciones de Variables Complejas en Python

## Índice de Contenidos

- [Visualizador de Funciones de Variables Complejas en Python](#visualizador-de-funciones-de-variables-complejas-en-python)
  - [Índice de Contenidos](#índice-de-contenidos)
  - [1. Configuración del Entorno de Desarrollo](#1-configuración-del-entorno-de-desarrollo)
    - [Herramientas:](#herramientas)
    - [Instalación de Bibliotecas:](#instalación-de-bibliotecas)
  - [2. Selección de Bibliotecas](#2-selección-de-bibliotecas)
    - [Para la Interfaz Gráfica:](#para-la-interfaz-gráfica)
    - [Para los Cálculos Matemáticos:](#para-los-cálculos-matemáticos)
  - [3. Diseño de la Interfaz Gráfica (GUI)](#3-diseño-de-la-interfaz-gráfica-gui)
      - [Código de Ejemplo para la GUI:](#código-de-ejemplo-para-la-gui)
  - [4. Implementación de la Lógica Matemática](#4-implementación-de-la-lógica-matemática)
      - [Ejemplo de procesamiento de la función:](#ejemplo-de-procesamiento-de-la-función)
  - [5. Visualización de Funciones en el Plano Complejo](#5-visualización-de-funciones-en-el-plano-complejo)
      - [Ejemplo de Visualización:](#ejemplo-de-visualización)
  - [6. Integración y Pruebas](#6-integración-y-pruebas)
  - [7. Mejoras y Funcionalidades Adicionales](#7-mejoras-y-funcionalidades-adicionales)

---

## 1. Configuración del Entorno de Desarrollo

Para comenzar, necesitas configurar tu entorno de desarrollo con las herramientas necesarias. Utilizaremos Python y algunas bibliotecas de apoyo como `matplotlib`, `sympy` y `tkinter` para la interfaz gráfica.

### Herramientas:

- **Python**: Asegúrate de tener instalada una versión actualizada de Python (3.x).
- **Editor de texto o IDE**: Puedes usar un entorno como VS Code, PyCharm o cualquier editor de tu preferencia.

### Instalación de Bibliotecas:

Ejecuta los siguientes comandos para instalar las bibliotecas necesarias:

```bash
pip install matplotlib sympy
```

---

## 2. Selección de Bibliotecas

### Para la Interfaz Gráfica:

- **Tkinter**: Biblioteca estándar de Python para crear interfaces gráficas de usuario (GUI). Es sencilla y perfecta para este tipo de proyectos pequeños.

### Para los Cálculos Matemáticos:

- **Sympy**: Una biblioteca de álgebra simbólica que nos ayudará a procesar las expresiones matemáticas y funciones de variables complejas.
- **Matplotlib**: Se encargará de la visualización gráfica, representando las funciones complejas en el plano de Argand (plano complejo).

---

## 3. Diseño de la Interfaz Gráfica (GUI)

La interfaz tendrá una estructura simple:
- Un campo de entrada para la función que el usuario quiera graficar.
- Un botón para graficar la función.
- Un área de visualización para mostrar la gráfica de la función en el plano complejo.

#### Código de Ejemplo para la GUI:

```python
import tkinter as tk
from tkinter import messagebox

# Crear la ventana principal
root = tk.Tk()
root.title("Visualizador de Funciones de Variables Complejas")

# Campo de entrada de la función
entry_label = tk.Label(root, text="Ingrese la función f(z):")
entry_label.pack()

function_entry = tk.Entry(root, width=40)
function_entry.pack()

# Botón para graficar
plot_button = tk.Button(root, text="Graficar", command=lambda: graficar_funcion(function_entry.get()))
plot_button.pack()

# Ejecutar la aplicación
root.mainloop()
```

---

## 4. Implementación de la Lógica Matemática

Para manejar funciones complejas, necesitamos que el usuario ingrese una función de \( z \) (número complejo), y con `sympy` la convertimos en una expresión simbólica para evaluar y graficar.

#### Ejemplo de procesamiento de la función:

```python
import sympy as sp

def procesar_funcion(funcion_str):
    z = sp.symbols('z')
    try:
        funcion = sp.sympify(funcion_str)
        return funcion
    except sp.SympifyError:
        messagebox.showerror("Error", "La función ingresada no es válida.")
        return None
```

---

## 5. Visualización de Funciones en el Plano Complejo

Utilizaremos `matplotlib` para representar la función compleja. La idea es graficar la magnitud y la dirección de los valores complejos en el plano.

#### Ejemplo de Visualización:

```python
import matplotlib.pyplot as plt
import numpy as np

def graficar_funcion(funcion_str):
    z = sp.symbols('z')
    funcion = procesar_funcion(funcion_str)
    
    if funcion is not None:
        x_vals = np.linspace(-10, 10, 400)
        y_vals = np.linspace(-10, 10, 400)
        X, Y = np.meshgrid(x_vals, y_vals)
        Z = X + 1j * Y  # Generar los puntos complejos
        
        # Evaluar la función para los valores de Z
        f_lambdified = sp.lambdify(z, funcion, 'numpy')
        F = f_lambdified(Z)
        
        # Crear la gráfica
        plt.figure()
        plt.streamplot(X, Y, F.real, F.imag, color=np.abs(F), cmap='plasma')
        plt.colorbar(label="|f(z)|")
        plt.title(f"Visualización de f(z) = {funcion_str}")
        plt.xlabel("Re(z)")
        plt.ylabel("Im(z)")
        plt.show()
```

---

## 6. Integración y Pruebas

En esta etapa, vamos a unir todo:
1. La interfaz gráfica que recibe la función.
2. El procesamiento matemático que convierte la entrada en una función.
3. La visualización gráfica que muestra el comportamiento de la función en el plano complejo.

Prueba ingresando diferentes funciones de \( z \), como:
- \( f(z) = z^2 + 2z + 1 \)
- \( f(z) = e^z \)
- \( f(z) = \sin(z) \)

---