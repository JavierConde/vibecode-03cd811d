Este código proporciona una función básica para mostrar una tabla de tareas en formato de texto.  Necesitaría una base de datos y un sistema de persistencia para funcionar con datos reales.  Para una aplicación completa, se recomendaría usar un framework como Flask o Django con una base de datos como PostgreSQL o SQLite.

```python
from typing import List, Dict, Tuple

def display_tasks_table(tasks: List[Dict]) -> None:
    """
    Displays a table of tasks in the console.

    Args:
        tasks: A list of dictionaries, where each dictionary represents a task 
               and contains at least 'titulo', 'descripcion', and 'completada' keys.
    """

    if not tasks:
        print("No hay tareas.")
        return

    # Obtener el ancho máximo de cada columna para el formateo
    column_widths = get_column_widths(tasks)

    # Imprimir encabezado
    print_table_row(["Título", "Descripción", "Completada"], column_widths)
    print("-" * (sum(column_widths) + 3 * len(column_widths))) # Linea separadora

    # Imprimir filas de tareas
    for task in tasks:
        row = [task['titulo'], task['descripcion'], "Sí" if task['completada'] else "No"]
        print_table_row(row, column_widths)


def get_column_widths(tasks: List[Dict]) -> Tuple[int, int, int]:
    """
    Calculates the maximum width of each column for formatting the table.
    """
    max_titulo_width = max(len(task['titulo']) for task in tasks)
    max_descripcion_width = max(len(task['descripcion']) for task in tasks)
    max_completada_width = max(len("Sí"), len("No")) #Ancho de la columna "Completada"
    return max_titulo_width, max_descripcion_width, max_completada_width


def print_table_row(row: List[str], column_widths: Tuple[int, int, int]) -> None:
    """Prints a single row of the table with proper formatting."""
    format_string = "{:<" + str(column_widths[0]) + "} | {:<" + str(column_widths[1]) + "} | {:<" + str(column_widths[2]) + "}"
    print(format_string.format(*row))



# Ejemplo de uso:
tasks_data = [
    {'id': 1, 'titulo': 'Comprar leche', 'descripcion': 'Comprar una galona de leche descremada', 'completada': False},
    {'id': 2, 'titulo': 'Pasear al perro', 'descripcion': 'Sacar a pasear a Fido por 30 minutos', 'completada': True},
    {'id': 3, 'titulo': 'Tarea larga', 'descripcion': 'Esta es una tarea con una descripción mucho más larga que las otras', 'completada': False}
]

display_tasks_table(tasks_data)

```

Este código  es más robusto y maneja diferentes longitudes de texto en las columnas de la tabla.  Recuerda que esto solo muestra la tabla;  la obtención y gestión de datos desde una base de datos requeriría código adicional.