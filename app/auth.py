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
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        usuario = Usuario.query.filter_by(email=email).first()

        if not usuario or not usuario.check_password(password):
            flash('Email o contraseña incorrectos. Por favor, intenta de nuevo.', 'error')
            return redirect(url_for('auth.login'))

        login_user(usuario)
        return redirect(url_for('main.dashboard'))

    return render_template('login.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        nombre = request.form.get('nombre')
        password = request.form.get('password')

        usuario_existente = Usuario.query.filter_by(email=email).first()
        if usuario_existente:
            flash('Ese email ya está registrado.', 'error')
            return redirect(url_for('auth.register'))

        nuevo_usuario = Usuario(email=email, nombre=nombre)
        nuevo_usuario.set_password(password)
        
        db.session.add(nuevo_usuario)
        db.session.commit()

        flash('¡Registro exitoso! Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))