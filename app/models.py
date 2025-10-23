# app/models.py

# 👇 ASEGÚRATE DE QUE "db" SE IMPORTE ASÍ:
from . import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Si tienes "from app import create_app" o "from app import app", BÓRRALO.

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True) 
    password_hash = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(50), nullable=False, default='alumno') 
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Usuario {self.nombre}>'

# --- (Pega el resto de tus clases: ScriptPregunta, Examen, RespuestaAlumno) ---
# ...
class ScriptPregunta(db.Model):
    __tablename__ = 'scripts_preguntas'
    # ... (tu código original) ...
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    descripcion = db.Column(db.Text)
    codigo_python = db.Column(db.Text, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

class Examen(db.Model):
    __tablename__ = 'examenes'
    # ... (tu código original) ...
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(120), nullable=False)
    descripcion = db.Column(db.Text)
    creador_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    json_preguntas = db.Column(db.JSON, nullable=False)
    pdf_path = db.Column(db.String(255))
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    script_id = db.Column(db.Integer, db.ForeignKey('scripts_preguntas.id'))

class RespuestaAlumno(db.Model):
    __tablename__ = 'respuestas_alumnos'
    # ... (tu código original) ...
    id = db.Column(db.Integer, primary_key=True)
    examen_id = db.Column(db.Integer, db.ForeignKey('examenes.id'), nullable=False)
    alumno_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    respuestas_json = db.Column(db.JSON, nullable=False)
    pdf_path = db.Column(db.String(255))
    calificacion = db.Column(db.Float)
    fecha_envio = db.Column(db.DateTime, default=datetime.utcnow)