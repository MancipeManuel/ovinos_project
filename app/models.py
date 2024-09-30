from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.postgresql import ENUM

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class Oveja(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    raza = db.Column(db.String(50), nullable=False)
    sexo = db.Column(db.Enum('Macho', 'Hembra', name='sexo_enum'), nullable=False)
    id_padre = db.Column(db.Integer, db.ForeignKey('oveja.id'), nullable=True)
    id_madre = db.Column(db.Integer, db.ForeignKey('oveja.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    padre = db.relationship('Oveja', remote_side=[id], foreign_keys=[id_padre], backref=db.backref('hijos_padre', uselist=True))
    madre = db.relationship('Oveja', remote_side=[id], foreign_keys=[id_madre], backref=db.backref('hijos_madre', uselist=True))

    user = db.relationship('User', backref='ovejas')

    def __repr__(self):
        return f'<Oveja {self.nombre}>'

class Salud(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_oveja = db.Column(db.Integer, db.ForeignKey('oveja.id'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    tipo_tratamiento = db.Column(db.String(100), nullable=False)
    detalle = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    oveja = db.relationship('Oveja', backref='salud')
    user = db.relationship('User', backref='salud')

class Reproduccion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_oveja = db.Column(db.Integer, db.ForeignKey('oveja.id'), nullable=False)
    fecha_apareamiento = db.Column(db.Date, nullable=False)
    id_macho = db.Column(db.Integer, db.ForeignKey('oveja.id'), nullable=True)
    fecha_parto = db.Column(db.Date, nullable=True)
    num_crias = db.Column(db.Integer, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    oveja = db.relationship('Oveja', foreign_keys=[id_oveja], backref='reproducciones')
    macho = db.relationship('Oveja', foreign_keys=[id_macho], backref='reproducciones_macho')
    user = db.relationship('User', backref='reproducciones')

class Alimentacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_oveja = db.Column(db.Integer, db.ForeignKey('oveja.id'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    tipo_alimento = db.Column(db.String(100), nullable=False)
    cantidad = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    oveja = db.relationship('Oveja', backref='alimentaciones')
    user = db.relationship('User', backref='alimentaciones')

class Inventario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    cantidad = db.Column(db.Float, nullable=False)
    fecha_adquisicion = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', backref='inventarios')

class Finanzas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(10), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    monto = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Nuevos campos para referencia a compra y venta
    compra_id = db.Column(db.Integer, db.ForeignKey('compra.id'), nullable=True)
    venta_id = db.Column(db.Integer, db.ForeignKey('venta.id'), nullable=True)

    user = db.relationship('User', backref='finanzas')
    compra = db.relationship('Compra', backref='finanzas', lazy=True)
    venta = db.relationship('Venta', backref='finanzas', lazy=True)

class Venta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_oveja = db.Column(db.Integer, db.ForeignKey('oveja.id'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    oveja = db.relationship('Oveja', backref='ventas')
    user = db.relationship('User', backref='ventas')

class Compra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo_producto = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    cantidad = db.Column(db.Float, nullable=False)
    precio = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', backref='compras')
