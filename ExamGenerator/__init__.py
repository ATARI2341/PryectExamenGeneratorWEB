# app/main.py
from flask import Blueprint, render_template
from flask_login import login_required, current_user
import sys
import os

# --- 1. CONFIGURAR LA RUTA DE IMPORTACIÓN ---
# Esto es necesario para que Python encuentre la carpeta "ExamGenerator"
# que está fuera de la carpeta "app"

# Obtenemos la ruta absoluta de la carpeta "app"
app_dir = os.path.dirname(os.path.abspath(__file__))
# Obtenemos la ruta del proyecto (la carpeta que contiene "app")
ruta_proyecto = os.path.dirname(app_dir)

# Añadimos la ruta del proyecto al path de Python
if ruta_proyecto not in sys.path:
    sys.path.append(ruta_proyecto)

# --- 2. IMPORTAR TU SCRIPT ---
try:
    # Ahora Python puede encontrar "ExamGenerator"
    # y el archivo "LibCreateQuestion.py" que está dentro
    from ExamGenerator.LibCreateQuestion import generar_pregunta
except ImportError as e:
    # Esto falla si no existe "ExamGenerator/__init__.py"
    # o si el nombre del archivo/función es incorrecto.
    def generar_pregunta():
        print(f"ERROR DE IMPORTACIÓN: No se pudo importar 'generar_pregunta'. {e}")
        return "ruta_falsa_error_importacion.tex"
except Exception as e:
    def generar_pregunta():
        print(f"ERROR INESPERADO EN LA IMPORTACIÓN: {e}")
        return "ruta_falsa_error_inesperado.tex"

# --- FIN DE LA IMPORTACIÓN ---


main = Blueprint('main', __name__)

@main.route('/')
def index():
    # Página de inicio pública (index.html)
    return render_template('index.html')


@main.route('/dashboard')
@login_required # Protegido
def dashboard():
    
    # --- 3. EJECUTAR TU SCRIPT ---
    try:
        # Llamamos a la función que importamos
        ruta_tex = generar_pregunta()
    except Exception as e:
        # Si la función 'generar_pregunta' falla al EJECUTARSE
        pregunta_generada = f"<p><strong>Error al ejecutar generar_pregunta():</strong> {e}</p>"
        return render_template(
            'dashboard.html', 
            usuario=current_user, 
            pregunta_latex=pregunta_generada
        )

    # --- 4. LEER EL ARCHIVO .TEX GENERADO ---
    try:
        # Tu script 'generar_pregunta' debe devolver la ruta COMPLETA del archivo
        with open(ruta_tex, 'r', encoding='utf-8') as f:
            pregunta_generada = f.read()
            
    except FileNotFoundError:
        pregunta_generada = f"<p><strong>Error de Archivo:</strong> No se pudo encontrar el archivo .tex en la ruta: {ruta_tex}. (Ruta actual de trabajo: {os.getcwd()})</p>"
    except Exception as e:
        pregunta_generada = f"<p><strong>Error inesperado al leer el archivo:</strong> {e}</p>"
    
    # --- 5. MOSTRAR RESULTADO ---
    return render_template(
        'dashboard.html', 
        usuario=current_user, 
        pregunta_latex=pregunta_generada
    )