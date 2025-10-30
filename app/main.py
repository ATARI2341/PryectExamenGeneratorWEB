# app/main.py
from flask import (
    Blueprint, render_template, abort, redirect, url_for, flash, 
    session, request
)
import json
from flask_login import login_required, current_user
import sys
import os
from . import db
from .models import Examen, Usuario, RespuestaAlumno

main = Blueprint('main', __name__)

# --- IMPORTACIÓN DEL SCRIPT GENERADOR ---
try:
    # 1. Importamos tu script real
    from app.ExamGenerator.Preguntas.EspVec__OM__DepLin.create_question import generar_pregunta
    
    # 2. El wrapper AHORA SÍ LLAMA AL SCRIPT IMPORTADO
    def generar_pregunta_dict():
        """
        Wrapper para tu script. 
        ¡Llama a 'generar_pregunta()' y espera que devuelva un dict!
        """
        # --- ¡ESTA ES LA LLAMADA REAL! ---
        # (Asegúrate de que tu 'create_question.py' devuelva un dict)
        return generar_pregunta() 

except ImportError as e:
    print(f"ADVERTENCIA: No se pudo importar el script generador. Se usará un simulador. Error: {e}")
    # Definimos un simulador si la importación falla
    def generar_pregunta_dict():
        import random
        num = random.randint(1, 100)
        
        # Este es el simulador que se usa SI LA IMPORTACIÓN FALLA
        enunciado = rf"ERROR DE IMPORTACIÓN: No se pudo cargar la pregunta real. Usando simulador N°{num}."
        opciones = [
            rf"Opción A ({num*3})", 
            rf"Opción B ({num*2})", 
            rf"Opción C ($\mathbb{R}^3$)"
        ]
        respuesta_idx = 1
        return {"enunciado_latex": enunciado, "opciones": opciones, "respuesta_correcta": respuesta_idx}
# --- FIN DE IMPORTACIÓN ---


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/dashboard')
@login_required
def dashboard():
    """
    Dashboard Principal.
    Para Alumnos: Muestra un examen de práctica automático.
    Para Docentes: (Redirige por ahora)
    """
    
    if current_user.rol == 'alumno':
        try:
            preguntas_generadas = []
            for i in range(10): 
                preguntas_generadas.append(generar_pregunta_dict())
            
            session['practice_exam'] = preguntas_generadas
            
            return render_template(
                'dashboard_alumno_practice.html', 
                usuario=current_user,
                preguntas=preguntas_generadas
            )
            
        except Exception as e:
            # Si el error 'name 'R' is not defined' ocurre AHORA,
            # es porque está en tu SCRIPT 'create_question.py'
            flash(f'Error al generar el examen de práctica: {e}', 'danger')
            return render_template('dashboard_alumno_practice.html', usuario=current_user, preguntas=[])
            
    # --- Lógica para Docentes ---
    elif current_user.rol == 'docente':
        flash('Estás en el dashboard de práctica de alumno.', 'info')
        return redirect(url_for('main.index')) 
    else:
        return redirect(url_for('main.index'))

# --- NUEVA RUTA PARA GUARDAR EL EXAMEN ---
@main.route('/submit-practice', methods=['POST'])
@login_required
def submit_practice():
    """
    Recibe las respuestas del examen de práctica,
    lo califica y lo guarda en la BD.
    """
    if current_user.rol != 'alumno':
        abort(403)
    
    try:
        respuestas_enviadas = request.form.to_dict()
        preguntas_originales = session.pop('practice_exam', None)
        
        if not preguntas_originales:
            flash('Tu sesión ha expirado. Por favor, inténtalo de nuevo.', 'warning')
            return redirect(url_for('main.dashboard'))

        score = 0
        total = len(preguntas_originales)
        
        for i, pregunta in enumerate(preguntas_originales):
            respuesta_correcta_idx = str(pregunta['respuesta_correcta'])
            respuesta_alumno_idx = respuestas_enviadas.get(f'pregunta-{i}')
            
            if respuesta_correcta_idx == respuesta_alumno_idx:
                score += 1
        
        calificacion_final = (score / total) * 10.0
        
        nueva_respuesta = RespuestaAlumno(
            examen_id=None, 
            alumno_id=current_user.id,
            respuestas_json=json.dumps(respuestas_enviadas),
            preguntas_json=json.dumps(preguntas_originales),
            calificacion=calificacion_final
        )
        
        db.session.add(nueva_respuesta)
        db.session.commit()
        
        flash(f'Examen enviado. Tu calificación: {score} / {total}', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error al guardar tus respuestas: {e}', 'danger')

    return redirect(url_for('main.dashboard'))