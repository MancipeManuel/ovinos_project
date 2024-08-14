from flask import render_template, redirect, url_for, flash
from app import app, db
from app.forms import OvejaForm,ReproduccionForm,saludForm
from app.models import Oveja,Reproduccion,Salud

@app.route('/listar_ovejas')
def listar_ovejas():
    ovejas = Oveja.query.all()  # Obtiene todas las ovejas de la base de datos
    return render_template('listar_ovejas.html',ovejas=ovejas)

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

@app.route('/registrar_reproduccion', methods=['GET', 'POST'])
def registrar_reproduccion():
    form = ReproduccionForm()
    if form.validate_on_submit():
        nueva_reproduccion = Reproduccion(
            id_oveja=form.id_oveja.data,
            fecha_apareamiento=form.fecha_apareamiento.data,
            id_macho=form.id_macho.data if form.id_macho.data is not None else None,
            fecha_parto=form.fecha_parto.data if form.fecha_parto.data is not None else None,
            num_crias=form.num_crias.data if form.num_crias.data is not None else None
        )
        db.session.add(nueva_reproduccion)
        db.session.commit()
        flash('Evento de reproducción registrado exitosamente!', 'success')
        return redirect(url_for('index'))
    return render_template('registrar_reproduccion.html', form=form)

@app.route('/listar_reproduccion')
def listar_reproduccion():
    reproducciones = Reproduccion.query.all()  # Renombra la variable
    return render_template('listar_reproduccion.html', reproducciones=reproducciones)



@app.route('/eliminar_reproduccion/<int:id>', methods=['POST'])
def eliminar_reproduccion(id):
    reproduccion = Reproduccion.query.get_or_404(id)
    db.session.delete(reproduccion)
    db.session.commit()
    flash('Reproducción eliminado correctamente', 'success')
    return redirect(url_for('listar_reproduccion'))



@app.route('/editar_reproduccion/<int:id>', methods=['GET', 'POST'])
def editar_reproduccion(id):
    reproduccion = Reproduccion.query.get_or_404(id)
    form = ReproduccionForm(obj=reproduccion)

    if form.validate_on_submit():
        reproduccion.id_oveja = form.id_oveja.data
        reproduccion.fecha_apareamiento = form.fecha_apareamiento.data
        reproduccion.id_macho = form.id_macho.data if form.id_macho.data else None
        reproduccion.fecha_parto = form.fecha_parto.data if form.fecha_parto.data else None
        reproduccion.num_crias = form.num_crias.data if form.num_crias.data else None

        db.session.commit()
        flash('Reproducción actualizada correctamente', 'success')
        return redirect(url_for('listar_reproduccion'))

    return render_template('editar_reproduccion.html', form=form)

@app.route('/editar_oveja/<int:id>', methods=['GET', 'POST'])
def editar_oveja(id):
    oveja = Oveja.query.get_or_404(id)
    form = OvejaForm(obj=oveja)
    if form.validate_on_submit():
        oveja.nombre = form.nombre.data
        oveja.fecha_nacimiento = form.fecha_nacimiento.data
        oveja.raza = form.raza.data
        oveja.sexo = form.sexo.data
        oveja.id_padre = form.id_padre.data
        oveja.id_madre = form.id_madre.data
        db.session.commit()
        flash('Oveja actualizada correctamente', 'success')
        return redirect(url_for('listar_ovejas'))
    return render_template('editar_oveja.html', form=form)

@app.route('/eliminar_oveja/<int:id>', methods=['POST'])
def eliminar_oveja(id):
    oveja = Oveja.query.get_or_404(id)
    db.session.delete(oveja)
    db.session.commit()
    flash('Oveja eliminada correctamente', 'success')
    return redirect(url_for('listar_ovejas'))

@app.route('/registrar_salud', methods=['GET', 'POST'])
def registrar_salud():
    form = saludForm()
    if form.validate_on_submit():
        nuevo_registro = Salud(
            id_oveja =form.id_oveja.data,
            fecha =form.fecha.data,
            tipo_tratamiento=form.tipo_tratamiento.data,
            detalle=form.detalle.data,   
        )
        db.session.add(nuevo_registro)
        db.session.commit()
        flash(' registrado exitosamente!', 'success')
        return redirect(url_for('index'))
    return render_template('registrar_salud.html', form=form)

@app.route('/listar_salud')
def listar_salud():
    salud = Salud.query.all()  
    print(salud)
    return render_template('listar_salud.html',salud = salud)

@app.route('/editar_salud/<int:id>', methods=['GET', 'POST'])
def editar_salud(id):
    salud = Salud.query.get_or_404(id)
    form = saludForm(obj=salud)
    
    if form.validate_on_submit(): 
        salud.id_oveja = form.id_oveja.data
        salud.fecha = form.fecha.data
        salud.tipo_tratamiento = form.tipo_tratamiento.data
        salud.detalle = form.detalle.data
        db.session.commit()
        flash('actualizado con éxito', 'success')
        return redirect(url_for('listar_salud'))
    
    return render_template('editar_salud.html', form=form , salud= salud)



@app.route('/eliminar_salud/<int:id>', methods=['POST'])
def eliminar_salud(id):
    salud = Salud.query.get_or_404(id)
    db.session.delete(salud)
    db.session.commit()
    flash('eliminado correctamente', 'success')
    return redirect(url_for('listar_salud'))