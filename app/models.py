from app import db

class Oveja(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    raza = db.Column(db.String(50), nullable=False)
    sexo = db.Column(db.Enum('Macho', 'Hembra', name='sexo_enum'), nullable=False)
    id_padre = db.Column(db.Integer, db.ForeignKey('oveja.id'), nullable=True)
    id_madre = db.Column(db.Integer, db.ForeignKey('oveja.id'), nullable=True)

    padre = db.relationship('Oveja', remote_side=[id], foreign_keys=[id_padre], post_update=True)
    madre = db.relationship('Oveja', remote_side=[id], foreign_keys=[id_madre], post_update=True)

    def _repr_(self):
        return f'<Oveja {self.nombre}>'

class Salud(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_oveja = db.Column(db.Integer, db.ForeignKey('oveja.id'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    tipo_tratamiento = db.Column(db.String(100), nullable=False)
    detalle = db.Column(db.Text, nullable=False)

class Reproduccion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_oveja = db.Column(db.Integer, db.ForeignKey('oveja.id'), nullable=False)
    fecha_apareamiento = db.Column(db.Date, nullable=False)
    id_macho = db.Column(db.Integer, db.ForeignKey('oveja.id'), nullable=True)
    fecha_parto = db.Column(db.Date, nullable=True)
    num_crias = db.Column(db.Integer, nullable=True)

class Alimentacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_oveja = db.Column(db.Integer, db.ForeignKey('oveja.id'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    tipo_alimento = db.Column(db.String(100), nullable=False)
    cantidad = db.Column(db.Float, nullable=False)

class Inventario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    cantidad = db.Column(db.Float, nullable=False)
    fecha_adquisicion = db.Column(db.Date, nullable=False)

class Finanzas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(10), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    monto = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.Date, nullable=False)

class Venta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_oveja = db.Column(db.Integer, db.ForeignKey('oveja.id'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Float, nullable=False)

class Compra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo_producto = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    cantidad = db.Column(db.Float, nullable=False)
    precio = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.Date, nullable=False)
