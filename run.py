# run.py
# Este script importa la 'fábrica' de aplicaciones (create_app)
# desde nuestra carpeta 'app' y la ejecuta.

from app import create_app

# Creamos la instancia de la aplicación
app = create_app()

if __name__ == '__main__':
    # Corremos el servidor en modo DEBUG.
    # Esto es vital para que:
    # 1. Veamos los errores en el navegador.
    # 2. El servidor se reinicie solo cada vez que guardamos un archivo .py.
    app.run(debug=True)