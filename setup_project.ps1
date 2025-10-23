Write-Host "Iniciando configuración del proyecto ExamenGeneratorWEB..."

# 1️⃣ Crear estructura de carpetas
$folders = @(
    "app",
    "app/static",
    "app/templates",
    "app/scripts_generadores",
    "instance"
)

foreach ($folder in $folders) {
    if (-not (Test-Path $folder)) {
        New-Item -ItemType Directory -Force -Path $folder | Out-Null
        Write-Host "Carpeta creada: $folder"
    }
}

# 2️⃣ Verificar Python
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Error: Python no está instalado o no está en PATH."
    exit 1
}

# 3️⃣ Verificar o instalar SQLite
if (-not (Get-Command sqlite3.exe -ErrorAction SilentlyContinue)) {
    Write-Host "Descargando SQLite..."
    $url = "https://www.sqlite.org/2024/sqlite-tools-win-x64-3460000.zip"
    $zip = "sqlite.zip"
    Invoke-WebRequest -Uri $url -OutFile $zip -UseBasicParsing
    Expand-Archive $zip -DestinationPath ".\sqlite"
    Remove-Item $zip
    $sqliteExe = Get-ChildItem -Path ".\sqlite" -Filter "sqlite3.exe" -Recurse | Select-Object -First 1
    if ($sqliteExe) {
        Write-Host "SQLite descargado correctamente en: $($sqliteExe.FullName)"
    } else {
        Write-Host "No se encontró sqlite3.exe después de la descarga."
    }
} else {
    Write-Host "SQLite ya está instalado."
}

# 4️⃣ Crear entorno virtual
if (-not (Test-Path ".venv")) {
    Write-Host "Creando entorno virtual..."
    python -m venv .venv
}
Write-Host "Entorno virtual listo."

# Activar entorno virtual
& .\.venv\Scripts\Activate.ps1

# 5️⃣ Instalar dependencias
Write-Host "Instalando dependencias..."
pip install flask flask_sqlalchemy flask_login reportlab

# 6️⃣ Crear archivo __init__.py
$appMain = "app/__init__.py"
@"
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'supersecreto'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/ExamenGeneratorWEB.db'

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from . import models
        db.create_all()

    return app
"@ | Out-File $appMain -Encoding utf8

# 7️⃣ Crear archivo models.py
$models = "app/models.py"
@"
from . import db
from datetime import datetime

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(50), nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)

class ScriptPregunta(db.Model):
    __tablename__ = 'scripts_preguntas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    descripcion = db.Column(db.Text)
    codigo_python = db.Column(db.Text, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

class Examen(db.Model):
    __tablename__ = 'examenes'
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
    id = db.Column(db.Integer, primary_key=True)
    examen_id = db.Column(db.Integer, db.ForeignKey('examenes.id'), nullable=False)
    alumno_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    respuestas_json = db.Column(db.JSON, nullable=False)
    pdf_path = db.Column(db.String(255))
    calificacion = db.Column(db.Float)
    fecha_envio = db.Column(db.DateTime, default=datetime.utcnow)
"@ | Out-File $models -Encoding utf8

# 8️⃣ Crear run.py
$runFile = "run.py"
@"
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
"@ | Out-File $runFile -Encoding utf8

# 9️⃣ Crear base de datos
Write-Host "Creando base de datos..."

# Crear un archivo temporal de Python
$dbScriptPath = "create_db_temp.py"
@"
from app import create_app, db
app = create_app()
with app.app_context():
    db.create_all()
print('Base de datos creada correctamente en instance/ExamenGeneratorWEB.db')
"@ | Out-File $dbScriptPath -Encoding utf8

# Ejecutar el script Python
python $dbScriptPath

# Eliminar el archivo temporal
Remove-Item $dbScriptPath -Force

Write-Host "Proyecto Flask ExamenGeneratorWEB listo para usarse."
