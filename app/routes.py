from flask import render_template, redirect, url_for, flash
from app import app, db
from app.forms import OvejaForm
from app.models import Oveja


# @app.route('/ovejas')
# def listar_ovejas():
#     ovejas=ovejas.query.all()
#     return render_template('ovejas.html',ovejas=ovejas)
@app.route('/ovejas')
def listar_ovejas():
    ovejas = Oveja.query.all()  # Obtiene todas las ovejas de la base de datos
    return render_template('ovejas.html',ovejas=ovejas)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registrar_oveja', methods=['GET', 'POST'])
def registrar_oveja():
    form = OvejaForm()
    if form.validate_on_submit():
        nueva_oveja = Oveja(
            nombre=form.nombre.data,
            fecha_nacimiento=form.fecha_nacimiento.data,
            raza=form.raza.data,
            sexo=form.sexo.data,
            id_padre=form.id_padre.data if form.id_padre.data else None,
            id_madre=form.id_madre.data if form.id_madre.data else None
        )
        db.session.add(nueva_oveja)
        db.session.commit()
        flash('Oveja registrada exitosamente!', 'success')
        return redirect(url_for('index'))
    return render_template('registro_oveja.html', form=form)
