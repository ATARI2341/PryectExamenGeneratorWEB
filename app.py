# app.py

import os
from flask import Flask, render_template

# Hacemos un pequeño truco para que Python encuentre tus librerías
# Esto es necesario porque ejecutamos el código desde la raíz del proyecto
import sys
sys.path.append('ExamGenerator')

# Ahora importamos la función que modificamos
from ExamGenerator.Preguntas.EspVec__OM__DepLin.create_question import generar_pregunta

app = Flask(__name__)

@app.route('/')
def mostrar_pregunta():
    # 1. Llamamos a la función para que cree los archivos Response.tex y Question.json
    ruta_tex = generar_pregunta()

    # 2. Leemos el contenido del archivo .tex generado
    try:
        with open(ruta_tex, 'r', encoding='utf-8') as f:
            contenido_latex = f.read()
    except FileNotFoundError:
        return "Error: No se pudo encontrar el archivo Response.tex generado.", 500

    # 3. Pasamos el contenido de LaTeX a nuestra plantilla HTML
    return render_template('index.html', pregunta_latex=contenido_latex)

if __name__ == '__main__':
    app.run(debug=True)