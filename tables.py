Este código proporciona una función para generar una tabla HTML que representa la lista de tareas.  Asume que se recibe una lista de diccionarios, donde cada diccionario representa una tarea con los campos 'titulo', 'descripcion', y 'completada'.  Necesitará una librería para manejar HTML, como `html` o `BeautifulSoup`, pero este ejemplo es lo suficientemente simple como para no necesitarlas para una representación básica.

```python
def generate_task_table(tasks):
    """Genera una tabla HTML para mostrar una lista de tareas.

    Args:
        tasks: Una lista de diccionarios, donde cada diccionario representa una tarea 
               con los campos 'titulo', 'descripcion', y 'completada'.

    Returns:
        Una cadena de texto que contiene el código HTML de la tabla.  Retorna una cadena vacía si la lista de tareas está vacía.
    """

    if not tasks:
        return ""

    table_html = "<table>\n"
    table_html += "<thead><tr><th>Título</th><th>Descripción</th><th>Completada</th></tr></thead>\n"
    table_html += "<tbody>\n"

    for task in tasks:
        completed_status = "Sí" if task['completada'] else "No"
        table_html += f"<tr><td>{task['titulo']}</td><td>{task['descripcion']}</td><td>{completed_status}</td></tr>\n"

    table_html += "</tbody>\n"
    table_html += "</table>"
    return table_html


# Ejemplo de uso:
tasks_data = [
    {'titulo': 'Tarea 1', 'descripcion': 'Descripción de la tarea 1', 'completada': True},
    {'titulo': 'Tarea 2', 'descripcion': 'Descripción de la tarea 2', 'completada': False},
    {'titulo': 'Tarea 3', 'descripcion': 'Descripción de la tarea 3', 'completada': True}
]

html_table = generate_task_table(tasks_data)
print(html_table)

# Para usar con una librería HTML:
# from html import escape # Para evitar problemas con caracteres especiales

# ... dentro de la función generate_task_table ...
# table_html += f"<tr><td>{escape(task['titulo'])}</td><td>{escape(task['descripcion'])}</td><td>{completed_status}</td></tr>\n"
# ...

```

Este código genera una tabla HTML básica.  Para una aplicación real,  se debería considerar el uso de un framework web como Flask o Django para manejar la generación del HTML y la interacción con el usuario, así como una base de datos para persistir los datos.  Además,  la función `escape` de la librería `html` se recomienda para prevenir vulnerabilidades XSS al mostrar datos de usuario en el HTML.