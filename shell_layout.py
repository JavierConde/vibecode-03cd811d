Este código proporciona una estructura básica para un layout de shell en una aplicación de línea de comandos.  Asumiendo que tienes otros módulos (auth, users, db, crud, forms, tables) ya implementados, este código se integraría con ellos.  Necesitarás adaptarlo a tu implementación específica de esos módulos.

```python
import os
import sys
from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import clear
from prompt_toolkit.styles import Style

# Estilo para la interfaz de la linea de comandos
style = Style.from_dict({
    "title": "bg:#000080 #ffffff",
    "menu": "bg:#004080 #ffffff",
    "option": "bg:#006080 #ffffff",
    "selected": "bg:#008080 #000000",
})

def clear_screen():
    """Limpia la pantalla de la terminal."""
    clear()

def display_menu(options):
    """Muestra el menú de opciones."""
    clear_screen()
    print("\n\t--- Menú de Tareas ---\n")
    for i, option in enumerate(options):
        selected_style = "selected" if i == 0 else "option" #Highlight the first option
        print(f"\t[{i+1}] {option[0]}") # Assuming options is a list of (description, function) tuples


def get_user_choice(options):
    """Obtiene la opción elegida por el usuario."""
    while True:
        try:
            choice = int(prompt(f"\nElige una opción (1-{len(options)}): ", style=style))
            if 1 <= choice <= len(options):
                return choice - 1
            else:
                print("Opción inválida. Intenta de nuevo.")
        except ValueError:
            print("Entrada inválida. Ingresa un número.")


def run_shell():
    """Corre el shell de la aplicación."""
    options = [
        ("Crear Tarea", lambda: crear_tarea()), #Reemplazar con la función de crear tarea
        ("Listar Tareas", lambda: listar_tareas()), #Reemplazar con la función de listar tareas
        ("Marcar Completada", lambda: marcar_completada()), #Reemplazar con la función de marcar como completada
        ("Salir", lambda: sys.exit(0)),
    ]

    while True:
        display_menu(options)
        choice = get_user_choice(options)
        options[choice][1]()  # Ejecutar la función seleccionada


def crear_tarea():
    """Implementacion de crear tarea.  Reemplazar con tu lógica."""
    print("Implementa la función para crear una tarea aquí.")
    input("Presiona Enter para continuar...")

def listar_tareas():
    """Implementacion de listar tarea.  Reemplazar con tu lógica."""
    print("Implementa la función para listar tareas aquí.")
    input("Presiona Enter para continuar...")

def marcar_completada():
    """Implementacion de marcar como completa.  Reemplazar con tu lógica."""
    print("Implementa la función para marcar una tarea como completada aquí.")
    input("Presiona Enter para continuar...")

if __name__ == "__main__":
    run_shell()

```

Recuerda que este código solo proporciona la estructura del shell. Necesitas implementar la lógica para la creación, listado y marcado de tareas usando tus módulos `auth`, `users`, `db`, `crud`, `forms`, y `tables`.  Las funciones `crear_tarea`, `listar_tareas`, y `marcar_completada` son solo marcadores de posición y deben ser reemplazadas con tu código funcional.  También necesitarás instalar `prompt_toolkit`:  `pip install prompt_toolkit`