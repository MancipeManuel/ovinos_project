from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, IntegerField, SubmitField,FloatField,DecimalField,TextAreaField,PasswordField
from wtforms.validators import DataRequired, Optional,NumberRange,Email,EqualTo,ValidationError
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    # Validar que el nombre de usuario sea único
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Please use a different username.')

    # Validar que el correo electrónico sea único
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Please use a different email address.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class OvejaForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    fecha_nacimiento = DateField('Fecha de Nacimiento', validators=[DataRequired()])
    raza = StringField('Raza', validators=[DataRequired()])
    sexo = SelectField('Sexo', choices=[('Macho', 'Macho'), ('Hembra', 'Hembra')], validators=[DataRequired()])
    id_padre = IntegerField('ID Padre', validators=[Optional()])
    id_madre = IntegerField('ID Madre', validators=[Optional()])
    submit = SubmitField('Guardar')

class ReproduccionForm(FlaskForm):
    id_oveja = IntegerField('ID Oveja (Hembra)', validators=[DataRequired()])
    fecha_apareamiento = DateField('Fecha de Apareamiento', format='%Y-%m-%d', validators=[DataRequired()])
    id_macho = IntegerField('ID Macho', validators=[])
    fecha_parto = DateField('Fecha de Parto', format='%Y-%m-%d', validators=[], default=None)
    num_crias = IntegerField('Número de Crías', validators=[], default=None)
    submit = SubmitField('Guardar')
    
class saludForm(FlaskForm):
    id_oveja = IntegerField('ID Oveja', validators=[DataRequired()])
    fecha = DateField('Fecha del tratamiento ', format='%Y-%m-%d', validators=[DataRequired()])
    tipo_tratamiento = StringField('Tipo Tratamiento',validators= [DataRequired()])
    detalle = StringField('Detalle del Tratamiento ', validators=[Optional()])
    submit = SubmitField('Guardar')

class AlimentacionForm(FlaskForm):
    id_oveja = IntegerField('ID Oveja', validators=[DataRequired()])
    fecha = DateField('Fecha', validators=[DataRequired()])
    tipo_alimento = StringField('Tipo de Alimento', validators=[DataRequired()])
    cantidad = FloatField('Cantidad', validators=[DataRequired()])
    submit = SubmitField('Guardar')
    
class VentaForm(FlaskForm):
    id_oveja = IntegerField('ID de Oveja', validators=[DataRequired()])
    fecha = DateField('Fecha', format='%Y-%m-%d', validators=[DataRequired()])
    cantidad = IntegerField('Cantidad', validators=[DataRequired(), NumberRange(min=1)])
    precio = DecimalField('Precio', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Guardar')

class CompraForm(FlaskForm):
    tipo_producto = StringField('Tipo de Producto', validators=[DataRequired()])
    descripcion = TextAreaField('Descripción', validators=[DataRequired()])
    cantidad = FloatField('Cantidad', validators=[DataRequired()])
    precio = FloatField('Precio', validators=[DataRequired()])
    fecha = DateField('Fecha', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Guardar')
    
class FinanzasForm(FlaskForm):
    tipo = SelectField('Tipo', choices=[('Venta', 'Venta'), ('Compra', 'Compra')], validators=[DataRequired()])
    descripcion = TextAreaField('Descripción', validators=[DataRequired()])
    monto = FloatField('Monto', validators=[DataRequired()])
    fecha = DateField('Fecha', validators=[DataRequired()])
    submit = SubmitField('Registrar')