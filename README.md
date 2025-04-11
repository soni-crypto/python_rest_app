
# Proyecto Python

## Instalación

### Crear Base de Datos

Crear una base de datos con el nombre: proyecto_python

### Configuración del Proyecto

Acceder al proyecto, abrir la terminal o CMD y ejecutar:

1 => pip install -r requirements.txt
2 => flask db init
3 => flask db migrate
4 => py app.py

### Configuración Final

Una vez tengas tu base de datos con todas las tablas creadas, ve al archivo: archivo application/main.py y comenta la siguiente línea de código::
```python
# Restaurant.createDB(app)

    