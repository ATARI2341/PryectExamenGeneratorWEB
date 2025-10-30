# app/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from .models import Usuario

class LoginForm(FlaskForm):
    """Formulario para el inicio de sesión."""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Recuérdame')
    submit = SubmitField('Iniciar Sesión')

class RegistrationForm(FlaskForm):
    """Formulario para el registro de nuevos usuarios."""
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=2, max=120)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(
        'Confirmar Contraseña', 
        validators=[DataRequired(), EqualTo('password', message='Las contraseñas no coinciden.')]
    )
    rol = RadioField(
        'Registrarse como', 
        choices=[('alumno', 'Alumno'), ('docente', 'Docente')], 
        default='alumno',
        validators=[DataRequired()]
    )
    submit = SubmitField('Crear Cuenta')

    def validate_email(self, email):
        """Validador personalizado para asegurar que el email no exista."""
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('Ese email ya está registrado. Por favor, elige otro.')