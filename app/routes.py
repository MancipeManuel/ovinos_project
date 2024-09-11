from flask import render_template, redirect, url_for, session
from app import app, db
from app.forms import OvejaForm, ReproduccionForm, saludForm, AlimentacionForm, VentaForm, CompraForm 
from app.models import Oveja, Reproduccion, Salud, Alimentacion, Venta, Compra, Finanzas
from sqlalchemy import func

@app.route('/')
def index():
    return render_template('index.html')
#----------------------------------------------------------aqui empieza las ovejas --------------------
@app.route('/listar_ovejas')
def listar_ovejas():
    ovejas = Oveja.query.all()
    return render_template('listar_ovejas.html', ovejas=ovejas)

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
            id_madre=form.id_madre.data if form.id_madre.data else None,
        )
        db.session.add(nueva_oveja)
        db.session.commit()
        session['notificacion1'] = 'Oveja registrada exitosamente.'
        return redirect(url_for('oveja'))
    return render_template('registro_oveja.html', form=form)


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
        session['notificacion2']= 'Oveja editada correctamente.'
        return redirect(url_for('oveja'))
    return render_template('editar_oveja.html', form=form)


@app.route('/eliminar_oveja/<int:id>', methods=['POST'])
def eliminar_oveja(id):
    oveja = Oveja.query.get_or_404(id)
    db.session.delete(oveja)
    db.session.commit()
    session['notificacion3'] = 'Oveja eliminada correctamente.'
    return redirect(url_for('oveja'))
#-----------------------------------------------------------------aqui termina-------------------------

#-----------------------------------------------------------------reproduccion-------------------------

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
        session['notificacion4'] = 'nuevo registro de reproduccion registrado'
        return redirect(url_for('reproduccion'))
    return render_template('registrar_reproduccion.html', form=form)

@app.route('/listar_reproduccion')
def listar_reproduccion():
    reproducciones = Reproduccion.query.all()
    return render_template('listar_reproduccion.html', reproducciones=reproducciones)

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
        session['notificacion5'] = 'regitro de reproduccion editadoco exito'
        return redirect(url_for('reproduccion'))
    return render_template('editar_reproduccion.html', form=form)

@app.route('/eliminar_reproduccion/<int:id>', methods=['POST'])
def eliminar_reproduccion(id):
    reproduccion = Reproduccion.query.get_or_404(id)
    db.session.delete(reproduccion)
    db.session.commit()
    session['notificacion6'] = 'registro de reproduccion eliminado'
    return redirect(url_for('reproduccion'))
#----------------------------------------------------------------------termina reproduccion-------------

#---------------------------------------------------------------------salud-------------------------

@app.route('/registrar_salud', methods=['GET', 'POST'])
def registrar_salud():
    form = saludForm()
    if form.validate_on_submit():
        nuevo_registro = Salud(
            id_oveja=form.id_oveja.data,
            fecha=form.fecha.data,
            tipo_tratamiento=form.tipo_tratamiento.data,
            detalle=form.detalle.data
        )
        db.session.add(nuevo_registro)
        db.session.commit()
        session['notificacion7'] = 'tratamiento registrado conexito'
        return redirect(url_for('salud'))
    return render_template('registrar_salud.html', form=form)

@app.route('/listar_salud')
def listar_salud():
    salud = Salud.query.all()
    return render_template('listar_salud.html', salud=salud)

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
        session['notificacion8'] = 'tratamiento editado con exito'
        return redirect(url_for('salud'))
    return render_template('editar_salud.html', form=form, salud=salud)

@app.route('/eliminar_salud/<int:id>', methods=['POST'])
def eliminar_salud(id):
    salud = Salud.query.get_or_404(id)
    db.session.delete(salud)
    db.session.commit()
    session['notificacion9'] = 'tratamiento eliminado correctamente'
    return redirect(url_for('salud'))
#--------------------------------------------------------------termina salud----------------------------

#--------------------------------------------------------------alimentación-----------------------------

@app.route('/registrar_alimentacion', methods=['GET', 'POST'])
def registrar_alimentacion():
    form = AlimentacionForm()
    if form.validate_on_submit():
        nueva_alimentacion = Alimentacion(
            id_oveja=form.id_oveja.data,
            fecha=form.fecha.data,
            tipo_alimento=form.tipo_alimento.data,
            cantidad=form.cantidad.data
        )
        db.session.add(nueva_alimentacion)
        db.session.commit()

        # Emitir notificación a todos los clientes
        session['notificacion10'] = 'alimento registrado exitosamente!'
        return redirect(url_for('alimentacion'))  # Redirige a la vista de notificaciones # Redirige a la vista de notificaciones
    return render_template('registrar_alimentacion.html', form=form)



@app.route('/listar_alimentacion')
def listar_alimentacion():
    alimentaciones = Alimentacion.query.all()
    return render_template('listar_alimentacion.html', alimentaciones=alimentaciones)

@app.route('/editar_alimentacion/<int:id>', methods=['GET', 'POST'])
def editar_alimentacion(id):
    alimentacion = Alimentacion.query.get_or_404(id)
    form = AlimentacionForm(obj=alimentacion)
    if form.validate_on_submit():
        alimentacion.id_oveja = form.id_oveja.data
        alimentacion.fecha = form.fecha.data
        alimentacion.tipo_alimento = form.tipo_alimento.data
        alimentacion.cantidad = form.cantidad.data
        db.session.commit()
        session['notificacion11'] = 'alimento editado correctamente'
        return redirect(url_for('alimentacion'))
    return render_template('editar_alimentacion.html', form=form)

@app.route('/eliminar_alimentacion/<int:id>', methods=['POST'])
def eliminar_alimentacion(id):
    alimentacion = Alimentacion.query.get_or_404(id)
    db.session.delete(alimentacion)
    db.session.commit()
    session['notificacion12']= 'alimento eliminado correctamente'
    return redirect(url_for('alimentacion'))
#---------------------------------------------------------------termina alimentacion------------------

#---------------------------------------------------------------ventas-------------------------------

@app.route('/registrar_venta', methods=['GET', 'POST'])
def registrar_venta():
    form = VentaForm()
    if form.validate_on_submit():
        nueva_venta = Venta(
            id_oveja=form.id_oveja.data,
            fecha=form.fecha.data,
            cantidad=form.cantidad.data,
            precio=form.precio.data
        )
        db.session.add(nueva_venta)
        nueva_finanza = Finanzas(
            tipo='Venta',
            descripcion=f'Venta de {form.cantidad.data} oveja(s)',
            monto=form.precio.data,
            fecha=form.fecha.data
        )
        db.session.add(nueva_finanza)
        db.session.commit()
        session['notificacion13']= 'se registro la venta con exito'
        return redirect(url_for('venta'))
    return render_template('registrar_venta.html', form=form)

@app.route('/listar_venta')
def listar_venta():
    ventas = Venta.query.all()
    return render_template('listar_ventas.html', ventas=ventas)

@app.route('/editar_venta/<int:id>', methods=['GET', 'POST'])
def editar_venta(id):
    venta = Venta.query.get_or_404(id)
    form = VentaForm(obj=venta)
    if form.validate_on_submit():
        venta.id_oveja = form.id_oveja.data
        venta.fecha = form.fecha.data
        venta.cantidad = form.cantidad.data
        venta.precio = form.precio.data
        db.session.commit()
        session['notificacion14']='se edito la venta correctamente'
        return redirect(url_for('venta'))
    return render_template('editar_venta.html', form=form)

@app.route('/eliminar_venta/<int:id>', methods=['POST'])
def eliminar_venta(id):
    venta = Venta.query.get_or_404(id)
    db.session.delete(venta)
    db.session.commit()
    session['notificacion15']='se elimino la venta correctamente'
    return redirect(url_for('venta'))
#-----------------------------------------------------------------termina venta-----------------------------

#-----------------------------------------------------------------compra--------------------------------
@app.route('/registrar_compra', methods=['GET', 'POST'])
def registrar_compra():
    form = CompraForm()
    if form.validate_on_submit():
        nueva_compra = Compra(
            tipo_producto=form.tipo_producto.data,
            descripcion=form.descripcion.data,
            cantidad=form.cantidad.data,
            precio=form.precio.data,
            fecha=form.fecha.data
        )
        db.session.add(nueva_compra)
        nueva_finanza = Finanzas(
            tipo='Compra',
            descripcion=f'Compra de {form.cantidad.data} oveja(s)',
            monto=form.precio.data,
            fecha=form.fecha.data
        )
        db.session.add(nueva_finanza)
        db.session.commit()
        session['notificacion16']='se registro la compra exitosamente'
        return redirect(url_for('compra'))
    return render_template('registrar_compra.html', form=form)

@app.route('/listar_compra')
def listar_compra():
    compras = Compra.query.all()
    return render_template('listar_compra.html', compras=compras)

@app.route('/editar_compra/<int:id>', methods=['GET', 'POST'])
def editar_compra(id):
    compra = Compra.query.get_or_404(id)
    form = CompraForm(obj=compra)
    if form.validate_on_submit():
        compra.fecha = form.fecha.data
        compra.cantidad = form.cantidad.data
        compra.precio = form.precio.data
        db.session.commit()
        session['notificacion17']='se edito la compra correctamente'
        return redirect(url_for('compra'))
    return render_template('editar_compra.html', form=form)

@app.route('/eliminar_compra/<int:id>', methods=['POST'])
def eliminar_compra(id):
    compra = Compra.query.get_or_404(id)
    db.session.delete(compra)
    db.session.commit()
    session['notificacion18']='se elimino correctamente la compra'
    return redirect(url_for('compra'))
#--------------------------------------------------finaliza compra---------------------------------------

#-----------------------------------------------------finanzas-------------------------------------

@app.route('/listar_finanzas')
def listar_finanzas():
    finanzas = Finanzas.query.order_by(Finanzas.fecha.desc()).all()
    return render_template('listar_finanzas.html', finanzas=finanzas)
#----------------------------------------------------------------------analisis financiero------------

@app.route('/analisis_financiero')
def analisis_financiero():
    ventas_total = db.session.query(func.sum(Venta.precio)).scalar() or 0
    compras_total = db.session.query(func.sum(Compra.precio)).scalar() or 0
    saldo_total = ventas_total - compras_total
    return render_template('analisis_financiero.html', ventas_total=ventas_total, compras_total=compras_total, saldo_total=saldo_total)

@app.route('/informe_mensual')
def informe_mensual():

    # Consultar el total de ventas por mes
    ventas_por_mes = db.session.query(
        db.func.strftime('%Y-%m', Finanzas.fecha).label('mes'),
        db.func.sum(Finanzas.monto).filter(Finanzas.tipo == 'Venta').label('total_ventas')
    ).group_by(db.func.strftime('%Y-%m', Finanzas.fecha)).all()
    # Consultar el total de compras por mes
    compras_por_mes = db.session.query(
        db.func.strftime('%Y-%m', Finanzas.fecha).label('mes'),
        db.func.sum(Finanzas.monto).filter(Finanzas.tipo == 'Compra').label('total_compras')
    ).group_by(db.func.strftime('%Y-%m', Finanzas.fecha)).all()

    return render_template('informe_mensual.html', ventas_por_mes=ventas_por_mes, compras_por_mes=compras_por_mes)


# index vacios------------------------------------------------------------------------------------------------------

@app.route('/oveja')
def oveja():
    mensaje1 = session.pop('notificacion1', None)
    mensaje2 = session.pop('notificacion2', None)
    mensaje3 = session.pop('notificacion3', None)
    
    return render_template('ovejas.html',mensaje1=mensaje1 ,mensaje2=mensaje2, mensaje3=mensaje3)

@app.route('/salud')
def salud():
    mensaje7 = session.pop('notificacion7', None)
    mensaje8 = session.pop('notificacion8', None)
    mensaje9 = session.pop('notificacion9', None)

    return render_template('salud.html',mensaje7=mensaje7,mensaje8=mensaje8,mensaje9=mensaje9)

@app.route('/reproduccion')
def reproduccion():
    mensaje4 = session.pop('notificacion4', None)
    mensaje5 = session.pop('notificacion5', None)
    mensaje6 = session.pop('notificacion6', None) 

    return render_template('reproduccion.html',mensaje4=mensaje4,mensaje5=mensaje5,mensaje6=mensaje6)

@app.route('/alimentacion')
def alimentacion():
    mensaje10 = session.pop('notificacion10', None)
    mensaje11 = session.pop('notificacion11', None)
    mensaje12 = session.pop('notificacion12', None)

    return render_template('alimentacion.html',mensaje10=mensaje10,mensaje11=mensaje11,mensaje12=mensaje12)


@app.route('/venta')
def venta():
    mensaje13 = session.pop('notificacion13', None)
    mensaje14 = session.pop('notificacion14', None)
    mensaje15 = session.pop('notificacion15', None)

    return render_template('venta.html',mensaje13=mensaje13,mensaje14=mensaje14,mensaje15=mensaje15)

@app.route('/compra')
def compra():

    mensaje16 = session.pop('notificacion16', None)
    mensaje17 = session.pop('notificacion17', None)
    mensaje18 = session.pop('notificacion18', None)


    return render_template('compra.html',mensaje16=mensaje16,mensaje17=mensaje17,mensaje18=mensaje18)

@app.route('/finanzas')
def finanzas():
    return render_template('finanzas.html')

@app.route('/recetas')
def recetas():
    return render_template('recetas.html')

@app.route('/catalogo')
def catalogo():
    return render_template('catalogo.html')


 









