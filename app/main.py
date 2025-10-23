# app/main.py
from flask import Blueprint, render_template
from flask_login import login_required, current_user
import sys
import os

ruta_proyecto = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ruta_proyecto)

try:
    from ExamGenerator.LibCreateQuestion import generar_pregunta
except ImportError as e:
    def generar_pregunta():
        print(f"ERROR: No se pudo importar 'generar_pregunta'. Verifica la ruta. {e}")
        return "ruta_falsa_error.tex"
except Exception as e:
    def generar_pregunta():
        print(f"ERROR INESPERADO: {e}")
        return "ruta_falsa_error_inesperado.tex"

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/dashboard')
@login_required
def dashboard():
    
    try:
        ruta_tex = generar_pregunta()
    except Exception as e: 
        
        pregunta_generada = f"<p><strong>Error al ejecutar generar_pregunta():</strong> {e}</p>"
        return render_template(
            'dashboard.html', 
            usuario=current_user, 
            pregunta_latex=pregunta_generada
        )

    try:
        with open(ruta_tex, 'r', encoding='utf-8') as f:
            pregunta_generada = f.read()
            
    except FileNotFoundError:
        pregunta_generada = f"<p><strong>Error:</strong> No se pudo encontrar el archivo generado en la ruta: {ruta_tex}. (Ruta actual de trabajo: {os.getcwd()})</p>"
    except Exception as e:
        pregunta_generada = f"<p><strong>Error inesperado al leer el archivo:</strong> {e}</p>"
    
    return render_template(
        'dashboard.html', 
        usuario=current_user, 
        pregunta_latex=pregunta_generada
    )