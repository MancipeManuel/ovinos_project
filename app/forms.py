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
