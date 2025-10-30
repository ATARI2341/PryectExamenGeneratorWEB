# app/auth.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from .models import Usuario
from . import db
from flask_login import login_user, logout_user, login_required, current_user

# --- ¡NUEVA IMPORTACIÓN! ---
from .forms import LoginForm, RegistrationForm

# Creamos un Blueprint llamado 'auth'
auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Maneja el inicio de sesión del usuario usando Flask-WTF."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    # --- CORRECCIÓN ---
    # 1. Creamos una instancia del formulario
    form = LoginForm()
    
    # 2. Reemplazamos 'request.method' con 'form.validate_on_submit()'
    if form.validate_on_submit():
        # 3. Obtenemos datos desde 'form.data' en lugar de 'request.form'
        email = form.email.data
        password = form.password.data
        remember = form.remember_me.data
        
        usuario = Usuario.query.filter_by(email=email).first()

        if not usuario or not usuario.check_password(password):
            flash('Email o contraseña incorrectos. Por favor, intenta de nuevo.', 'danger')
            return redirect(url_for('auth.login'))

        login_user(usuario, remember=remember)
        flash(f'¡Bienvenido de vuelta, {usuario.nombre}!', 'success')
        return redirect(url_for('main.dashboard'))

    # 4. Pasamos el 'form' a la plantilla en CUALQUIER caso (GET o POST fallido)
    #    ¡Esto soluciona el error 'form is undefined'!
    return render_template('login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """Maneja el registro de un nuevo usuario usando Flask-WTF."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    # --- CORRECCIÓN ---
    # 1. Creamos una instancia del formulario
    form = RegistrationForm()
    
    # 2. Reemplazamos 'request.method' con 'form.validate_on_submit()'
    if form.validate_on_submit():
        # 3. Obtenemos datos desde 'form.data'
        email = form.email.data
        nombre = form.nombre.data
        password = form.password.data
        rol = form.rol.data
        
        # 4. La validación (email duplicado, contraseñas no coinciden)
        #    ¡YA SE HIZO! Se hace automáticamente por los validadores en 'forms.py'
        
        nuevo_usuario = Usuario(
            email=email, 
            nombre=nombre, 
            rol=rol
        )
        nuevo_usuario.set_password(password)
        
        try:
            db.session.add(nuevo_usuario)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear la cuenta: {e}', 'danger')
            return redirect(url_for('auth.register'))

        flash('¡Registro exitoso! Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('auth.login'))

    # 4. Pasamos el 'form' a la plantilla en CUALQUIER caso (GET o POST fallido)
    #    ¡Esto soluciona el error 'form is undefined'!
    return render_template('register.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    """Maneja el cierre de sesión del usuario."""
    logout_user()
    return redirect(url_for('main.index'))