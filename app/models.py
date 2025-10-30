# app/models.py

from . import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model, UserMixin):
    """
    Modelo para los usuarios (Alumnos y Docentes).
    """
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True) 
    password_hash = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(50), nullable=False, default='alumno') 
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)

    # --- Relaciones ---
    # 1. Un docente puede crear múltiples exámenes.
    #    El 'backref' nos permite llamar a 'examen.creador' para obtener el objeto Usuario.
    examenes_creados = db.relationship('Examen', backref='creador', lazy='dynamic')
    
    # 2. Un alumno puede enviar múltiples respuestas.
    #    El 'backref' nos permite llamar a 'respuesta.alumno' para obtener el objeto Usuario.
    respuestas_enviadas = db.relationship('RespuestaAlumno', backref='alumno', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Usuario {self.nombre} ({self.rol})>'


class ScriptPregunta(db.Model):
    """
    Almacena la información sobre un script de Python que genera preguntas.
    """
    __tablename__ = 'scripts_preguntas'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    descripcion = db.Column(db.Text)
    # Tu campo original para guardar el código (en lugar de una ruta)
    codigo_python = db.Column(db.Text, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    # --- Relación ---
    # 1. Un script puede ser usado para generar múltiples exámenes.
    examenes_generados = db.relationship('Examen', backref='script_usado', lazy='dynamic')

    def __repr__(self):
        return f'<ScriptPregunta: {self.nombre}>'


class Examen(db.Model):
    """
    Define un examen formal creado por un docente.
    Contiene un JSON con la lista de preguntas generadas.
    """
    __tablename__ = 'examenes'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(120), nullable=False)
    descripcion = db.Column(db.Text)
    creador_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    # Almacena la lista de preguntas (enunciado, opciones, respuesta)
    json_preguntas = db.Column(db.JSON, nullable=False)
    pdf_path = db.Column(db.String(255))
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    script_id = db.Column(db.Integer, db.ForeignKey('scripts_preguntas.id'))

    # --- Relación ---
    # 1. Un examen puede tener muchas respuestas de alumnos.
    respuestas_de_alumnos = db.relationship('RespuestaAlumno', backref='examen', lazy='dynamic')

    def __repr__(self):
        return f'<Examen: {self.titulo}>'


class RespuestaAlumno(db.Model):
    """
    Almacena las respuestas de un alumno, ya sea a un examen formal
    o a un examen de práctica (generado automáticamente).
    """
    __tablename__ = 'respuestas_alumnos'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # --- MODIFICACIÓN CLAVE ---
    # 'examen_id' es opcional (nullable=True) porque un examen de práctica
    # no tiene un 'Examen' formal asociado.
    examen_id = db.Column(db.Integer, db.ForeignKey('examenes.id'), nullable=True)
    # --- FIN DE MODIFICACIÓN ---
    
    # El alumno que envió la respuesta (siempre requerido)
    alumno_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    
    # Almacena las respuestas que el alumno seleccionó (ej: {"0": "A", "1": "C"})
    respuestas_json = db.Column(db.JSON, nullable=False)
    
    # --- NUEVO CAMPO ---
    # Para exámenes de práctica, guardamos las preguntas que se generaron
    preguntas_json = db.Column(db.JSON, nullable=True) 
    # --- FIN DE NUEVO CAMPO ---
    
    pdf_path = db.Column(db.String(255))
    calificacion = db.Column(db.Float)
    fecha_envio = db.Column(db.DateTime, default=datetime.utcnow)

    # Las relaciones 'examen' y 'alumno' ya están definidas
    # por los 'backref' en las otras tablas.

    def __repr__(self):
        return f'<Respuesta de Alumno {self.alumno_id} (ID: {self.id})>'