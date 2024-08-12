from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Optional

class OvejaForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    fecha_nacimiento = DateField('Fecha de Nacimiento', validators=[DataRequired()])
    raza = StringField('Raza', validators=[DataRequired()])
    sexo = SelectField('Sexo', choices=[('Macho', 'Macho'), ('Hembra', 'Hembra')], validators=[DataRequired()])
    id_padre = IntegerField('ID Padre', validators=[Optional()])
    id_madre = IntegerField('ID Madre', validators=[Optional()])
    submit = SubmitField('Registrar Oveja')

class ReproduccionForm(FlaskForm):
    id_oveja = IntegerField('ID Oveja (Hembra)', validators=[DataRequired()])
    fecha_apareamiento = DateField('Fecha de Apareamiento', format='%Y-%m-%d', validators=[DataRequired()])
    id_macho = IntegerField('ID Macho', validators=[])
    fecha_parto = DateField('Fecha de Parto', format='%Y-%m-%d', validators=[], default=None)
    num_crias = IntegerField('Número de Crías', validators=[], default=None)
    submit = SubmitField('Registrar')


