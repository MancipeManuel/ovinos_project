from flask import render_template, redirect, url_for, flash
from app import app, db
from app.forms import OvejaForm,saludForm
from app.models import Oveja,Salud


# @app.route('/ovejas')
# def listar_ovejas():
#     ovejas=ovejas.query.all()
#     return render_template('ovejas.html',ovejas=ovejas)
@app.route('/ovejas')
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


@app.route('/salud')
def listar_salud():
    salud = Salud.query.all()  
    print(salud)
    return render_template('vista_salud.html',salud = salud)

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

    
    
    

        