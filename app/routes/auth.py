# app/auth.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from .models import Usuario
from . import db
from flask_login import login_user, logout_user, login_required, current_user

# Creamos un Blueprint llamado 'auth'
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard')) # 'main' será nuestro otro blueprint

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Buscamos al usuario por email
        usuario = Usuario.query.filter_by(email=email).first()

        # Verificamos al usuario y su contraseña
        if not usuario or not usuario.check_password(password):
            flash('Email o contraseña incorrectos. Por favor, intenta de nuevo.', 'error')
            return redirect(url_for('auth.login'))

        # Si todo está bien, iniciamos sesión
        login_user(usuario)
        return redirect(url_for('main.dashboard')) # Lo redirigimos al dashboard

    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        nombre = request.form.get('nombre')
        password = request.form.get('password')

        # Verificamos si el email ya existe
        usuario_existente = Usuario.query.filter_by(email=email).first()
        if usuario_existente:
            flash('Ese email ya está registrado.', 'error')
            return redirect(url_for('auth.register'))

        # Creamos el nuevo usuario
        nuevo_usuario = Usuario(email=email, nombre=nombre)
        nuevo_usuario.set_password(password) # Usamos el método para hashear
        
        db.session.add(nuevo_usuario)
        db.session.commit()

        flash('¡Registro exitoso! Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth.route('/logout')
@login_required # Solo usuarios logueados pueden desloguearse
def logout():
    logout_user()
    return redirect(url_for('main.index'))