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
# Importamos todos los modelos que usaremos
from .models import Examen, Usuario, RespuestaAlumno

main = Blueprint('main', __name__)

# --- IMPORTACIÓN DEL SCRIPT GENERADOR ---
try:
    # 1. Importamos tu script real (el de la ruta larga)
    from app.ExamGenerator.Preguntas.EspVec__OM__DepLin.create_question import generar_pregunta
    
    # 2. El wrapper llama al script real
    def generar_pregunta_dict():
        """
        Wrapper que llama al script real 'generar_pregunta()'.
        (Asegúrate de que 'create_question.py' devuelva un dict)
        """
        # --- ¡ESTA ES LA LLAMADA REAL! ---
        return generar_pregunta() 

except ImportError as e:
    # Si la importación falla, imprime un aviso y usa el simulador
    print(f"ADVERTENCIA: No se pudo importar 'create_question.py'. Se usará un simulador. Error: {e}")
    
    def generar_pregunta_dict():
        # --- SIMULADOR DE RESPALDO ---
        import random
        num = random.randint(1, 100)
        
        enunciado = rf"ERROR DE IMPORTACIÓN: Usando simulador N°{num}."
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
    """Ruta para la página de inicio pública."""
    return render_template('index.html')


@main.route('/dashboard')
@login_required
def dashboard():
    """
    Dashboard Principal.
    Muestra una vista diferente basada en el rol del usuario.
    """
    
    # --- Lógica para Alumnos ---
    if current_user.rol == 'alumno':
        try:
            preguntas_generadas = []
            for i in range(10): # Genera 10 preguntas
                preguntas_generadas.append(generar_pregunta_dict())
            
            # Guarda las preguntas (con respuestas) en la sesión segura
            session['practice_exam'] = preguntas_generadas
            
            # Muestra la plantilla del examen de práctica
            return render_template(
                'dashboard_alumno_practice.html', 
                usuario=current_user,
                preguntas=preguntas_generadas
            )
            
        except Exception as e:
            flash(f'Error al generar el examen de práctica: {e}', 'danger')
            return render_template('dashboard_alumno_practice.html', usuario=current_user, preguntas=[])
            
    # --- LÓGICA PARA DOCENTES (CORREGIDA) ---
    elif current_user.rol == 'docente':
        try:
            # 1. Busca en la BD todas las respuestas de exámenes de práctica
            respuestas_practica = RespuestaAlumno.query.filter_by(examen_id=None)\
                                                        .order_by(RespuestaAlumno.fecha_envio.desc())\
                                                        .all()
            
            # 2. Renderiza la plantilla del docente con la lista de respuestas
            return render_template(
                'dashboard_docente.html', 
                usuario=current_user,
                respuestas=respuestas_practica
            )
        except Exception as e:
            flash(f'Error al cargar las respuestas de los alumnos: {e}', 'danger')
            return render_template('dashboard_docente.html', usuario=current_user, respuestas=[])
    
    # --- Redirección por si acaso ---
    else:
        flash('Rol de usuario no reconocido.', 'warning')
        return redirect(url_for('main.index'))


@main.route('/submit-practice', methods=['POST'])
@login_required
def submit_practice():
    """
    Recibe las respuestas del examen de práctica del alumno,
    lo califica y lo guarda en la BD.
    """
    if current_user.rol != 'alumno':
        abort(403) # Solo alumnos pueden enviar
    
    try:
        respuestas_enviadas = request.form.to_dict()
        preguntas_originales = session.pop('practice_exam', None)
        
        if not preguntas_originales:
            flash('Tu sesión ha expirado. Por favor, inténtalo de nuevo.', 'warning')
            return redirect(url_for('main.dashboard'))

        # Calificar el examen
        score = 0
        total = len(preguntas_originales)
        
        for i, pregunta in enumerate(preguntas_originales):
            respuesta_correcta_idx = str(pregunta['respuesta_correcta'])
            respuesta_alumno_idx = respuestas_enviadas.get(f'pregunta-{i}')
            
            if respuesta_correcta_idx == respuesta_alumno_idx:
                score += 1
        
        calificacion_final = (score / total) * 10.0
        
        # Guardar en la Base de Datos
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


# --- NUEVA RUTA PARA "VER DETALLES" ---
@main.route('/respuesta/<int:respuesta_id>')
@login_required
def ver_respuesta(respuesta_id):
    """
    Página para que un docente vea los detalles
    de una respuesta de examen de práctica.
    """
    # 1. Solo los docentes pueden ver esto
    if current_user.rol != 'docente':
        abort(403)
        
    # 2. Busca la respuesta en la BD usando el ID de la URL
    respuesta = db.session.get(RespuestaAlumno, respuesta_id)
    if not respuesta:
        abort(404) # Si no se encuentra, error 404
        
    # 3. Carga los datos JSON
    try:
        preguntas = json.loads(respuesta.preguntas_json)
        respuestas_alumno = json.loads(respuesta.respuestas_json)
    except TypeError:
        # Si ya eran dicts (porque tu db.JSON funciona bien), solo asígnalos
        preguntas = respuesta.preguntas_json
        respuestas_alumno = respuesta.respuestas_json
    
    # 4. Renderiza la nueva plantilla y le pasa todos los datos
    return render_template(
        'ver_respuesta.html',
        usuario=current_user,
        respuesta=respuesta,          # El objeto 'RespuestaAlumno' (para la nota, alumno, etc.)
        preguntas=preguntas,          # La lista de preguntas que se hicieron
        respuestas_alumno=respuestas_alumno # El dict de las respuestas del alumno
    )