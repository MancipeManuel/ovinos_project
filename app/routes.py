from flask import render_template, redirect, url_for, session
from app import app, db
from app.forms import OvejaForm, ReproduccionForm, saludForm, AlimentacionForm, VentaForm, CompraForm 
from app.models import Oveja, Reproduccion, Salud, Alimentacion, Venta, Compra, Finanzas
from sqlalchemy import func




import os
from app.reportes import (
    generate_ovejas_report,
    generate_salud_report,
    generate_reproduccion_report,
    generate_alimentacion_report,
    generate_inventario_report,
    generate_finanzas_report,
    generate_ovejas_pdf_report,
    generate_salud_pdf_report,
    generate_reproduccion_pdf_report,
    generate_alimentacion_pdf_report,
    generate_inventario_pdf_report,
    generate_finanzas_pdf_report
)

# Directorio para archivos temporales
TMP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tmp')

# Crear el directorio si no existe
if not os.path.exists(TMP_DIR):
    os.makedirs(TMP_DIR)

@app.route('/reportes', methods=['GET'])
def reportes_view():
    form = ReporteForm()  # Crea una instancia del formulario
    return render_template('reportes.html', form=form)

@app.route('/generar_reporte', methods=['POST'])
def generar_reporte():
    tipo_reporte = request.form.get('tipo_reporte')
    formato = request.form.get('formato')

    filename = None
    file_path = None

    if formato == 'excel':
        if tipo_reporte == 'ovejas':
            filename = 'reporte_ovejas.xlsx'
            file_path = os.path.join(TMP_DIR, filename)
            generate_ovejas_report(file_path)
        elif tipo_reporte == 'salud':
            filename = 'reporte_salud.xlsx'
            file_path = os.path.join(TMP_DIR, filename)
            generate_salud_report(file_path)
        elif tipo_reporte == 'reproduccion':
            filename = 'reporte_reproduccion.xlsx'
            file_path = os.path.join(TMP_DIR, filename)
            generate_reproduccion_report(file_path)
        elif tipo_reporte == 'alimentacion':
            filename = 'reporte_alimentacion.xlsx'
            file_path = os.path.join(TMP_DIR, filename)
            generate_alimentacion_report(file_path)
        elif tipo_reporte == 'inventario':
            filename = 'reporte_inventario.xlsx'
            file_path = os.path.join(TMP_DIR, filename)
            generate_inventario_report(file_path)
        elif tipo_reporte == 'finanzas':
            filename = 'reporte_finanzas.xlsx'
            file_path = os.path.join(TMP_DIR, filename)
            generate_finanzas_report(file_path)
    elif formato == 'pdf':
        if tipo_reporte == 'ovejas':
            filename = 'reporte_ovejas.pdf'
            file_path = os.path.join(TMP_DIR, filename)
            generate_ovejas_pdf_report(file_path)
        elif tipo_reporte == 'salud':
            filename = 'reporte_salud.pdf'
            file_path = os.path.join(TMP_DIR, filename)
            generate_salud_pdf_report(file_path)
        elif tipo_reporte == 'reproduccion':
            filename = 'reporte_reproduccion.pdf'
            file_path = os.path.join(TMP_DIR, filename)
            generate_reproduccion_pdf_report(file_path)
        elif tipo_reporte == 'alimentacion':
            filename = 'reporte_alimentacion.pdf'
            file_path = os.path.join(TMP_DIR, filename)
            generate_alimentacion_pdf_report(file_path)
        elif tipo_reporte == 'inventario':
            filename = 'reporte_inventario.pdf'
            file_path = os.path.join(TMP_DIR, filename)
            generate_inventario_pdf_report(file_path)
        elif tipo_reporte == 'finanzas':
            filename = 'reporte_finanzas.pdf'
            file_path = os.path.join(TMP_DIR, filename)
            generate_finanzas_pdf_report(file_path)
    else:
        return "Formato no válido", 400
    
    # Verificar que el archivo se haya generado y enviar el archivo
    if os.path.exists(file_path):
        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename
        )
    else:
        return "Archivo no encontrado", 404




@app.route('/')
def index():
    return render_template('index.html')

#----------------------------------------------------------aqui empieza las ovejas --------------------




@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)  # Generar la contraseña hash
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('login'))  # Redirigir al login después del registro
    return render_template('registro.html', form=form,)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)  # Inicia sesión del usuario
            next_page = request.args.get('next')  # Redirige a la página solicitada después del login
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out!', 'success')
    return redirect(url_for('login'))
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
        flash('oveja registrada ', 'success')
        return redirect(url_for('listar_ovejas'))
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
        flash('oveja editada correctamente!', 'success')
        return redirect(url_for('listar_ovejas'))
    return render_template('editar_oveja.html', form=form)


@app.route('/eliminar_oveja/<int:id>', methods=['POST'])
def eliminar_oveja(id):
    oveja = Oveja.query.get_or_404(id)
    db.session.delete(oveja)
    db.session.commit()
    flash('oveja eliminada!', 'success')
    return redirect(url_for('listar_ovejas'))
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
        flash('registro nuevo de reproduccion registrado!', 'success')
        return redirect(url_for('listar_reproduccion'))
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
        flash('registro editado!', 'success')
        return redirect(url_for('listar_reproduccion'))
    return render_template('editar_reproduccion.html', form=form)

@app.route('/eliminar_reproduccion/<int:id>', methods=['POST'])
def eliminar_reproduccion(id):
    reproduccion = Reproduccion.query.get_or_404(id)
    db.session.delete(reproduccion)
    db.session.commit()
    flash('registro eliminado!', 'success')
    return redirect(url_for('listar_reproduccion'))
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
        flash('tratamiento registrado!', 'success')
        return redirect(url_for('listar_salud'))
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
        flash('tratamiento editado!', 'success')
        return redirect(url_for('listar_salud'))
    return render_template('editar_salud.html', form=form, salud=salud)

@app.route('/eliminar_salud/<int:id>', methods=['POST'])
def eliminar_salud(id):
    salud = Salud.query.get_or_404(id)
    db.session.delete(salud)
    db.session.commit()
    flash('tratamiento eliminado!', 'success')
    return redirect(url_for('listar_salud'))
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
        flash('alimento registrado!', 'success')
        return redirect(url_for('listar_alimentacion'))  # Redirige a la vista de notificaciones # Redirige a la vista de notificaciones
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


        flash('alimento editado!', 'success')
        return redirect(url_for('listar_alimentacion'))


    return render_template('editar_alimentacion.html', form=form)

@app.route('/eliminar_alimentacion/<int:id>', methods=['POST'])
def eliminar_alimentacion(id):
    alimentacion = Alimentacion.query.get_or_404(id)
    db.session.delete(alimentacion)
    db.session.commit()
    flash('alimento eliminado!', 'success')
    return redirect(url_for('listar_alimentacion'))
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
        flash('venta registrada!', 'success')
        return redirect(url_for('listar_ventas'))
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


        flash('venta editada!', 'success')
        return redirect(url_for('listar_ventas'))

    return render_template('editar_venta.html', form=form)

@app.route('/eliminar_venta/<int:id>', methods=['POST'])
def eliminar_venta(id):
    venta = Venta.query.get_or_404(id)
    db.session.delete(venta)
    db.session.commit()

    session['notificacion15']='se elimino la venta correctamente'
    return redirect(url_for('venta'))

    flash('venta eliminada!', 'success')
    return redirect(url_for('listar_ventas'))   

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


        flash('compra registrada!', 'success')
        return redirect(url_for('listar_compra'))
     # Asegúrate de que la ruta listar_compras esté definida


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


        flash('compra editada!', 'success')
        return redirect(url_for('listar_compra'))


    return render_template('editar_compra.html', form=form)

@app.route('/eliminar_compra/<int:id>', methods=['POST'])
def eliminar_compra(id):
    compra = Compra.query.get_or_404(id)
    db.session.delete(compra)
    db.session.commit()

    session['notificacion18']='se elimino correctamente la compra'


    flash('compra eliminada !', 'success')

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


@app.route('/listar_inventario', methods=['GET'])
def listar_inventario():
    inventario = Inventario.query.all()
    return render_template('listar_inventario.html', inventario=inventario)
#-----------------------------------------------------------------------------inventario---------------------

@app.route('/inventario_nuevo', methods=['GET', 'POST'])
def insertar_inventario():
    form = InventarioForm()
    if form.validate_on_submit():
        nuevo_item = Inventario(
            tipo=form.tipo.data,
            descripcion=form.descripcion.data,
            cantidad=form.cantidad.data,
            fecha_adquisicion=form.fecha_adquisicion.data
        )
        db.session.add(nuevo_item)
        db.session.commit()
        flash('nuevo producto agregado al inenario','success')
        return redirect(url_for('listar_inventario'))
    return render_template('insertar_inventario.html', form=form)

@app.route('/inventario_editar/<int:id>', methods=['GET', 'POST'])
def editar_inventario(id):
    item = Inventario.query.get_or_404(id)
    form = InventarioForm(obj=item)
    
    if form.validate_on_submit():
        item.tipo = form.tipo.data
        item.descripcion = form.descripcion.data
        item.cantidad = form.cantidad.data
        item.fecha_adquisicion = form.fecha_adquisicion.data
        db.session.commit()
        flash('producto actualizado correctamente','success')
        return redirect(url_for('listar_inventario'))
    
    return render_template('editar_inventario.html', form=form, item=item)

@app.route('/inventario_eliminar/<int:id>', methods=['POST'])
def eliminar_inventario(id):
    print(request.form)  # Imprime los datos del formulario para depuración
    item = Inventario.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('producto eliminado correctamente','success')
    return redirect(url_for('listar_inventario'))


# index vacios------------------------------------------------------------------------------------------------------

@app.route('/oveja')
def oveja():
 
    
    return render_template('ovejas.html',)



@app.route('/salud')
def salud():
  

    return render_template('salud.html')

@app.route('/reproduccion')
def reproduccion():
    

    return render_template('reproduccion.html')

@app.route('/alimentacion')
def alimentacion():
    return render_template('alimentacion.html')



@app.route('/venta')
def venta():
   


    return render_template('venta.html')

@app.route('/compra')
def compra():



    return render_template('compra.html')

@app.route('/finanzas')
def finanzas():
    return render_template('finanzas.html')


@app.route('/recetas')
def recetas():
    return render_template('recetas.html')


@app.route('/catalogo')
def catalogo():
    return render_template('catalogo.html')

@app.route('/finanzas')
def finanzas():
    return render_template('finanzas.html')
 
@app.route('/inventario')
def inventario():
    return render_template('inventario.html')


@app.route('/catalogo')
def catalogo():
    return render_template('catalogo.html')

@app.route('/recetas')
def recetas():
    return render_template('recetas.html')
#-------------------------------------------------funcion para mostrar las ovejas hembras-------------------
# @app.route('/hembras')
# def listar_reproduccion():
#     reproducciones = Reproduccion.query.filter_by(user_id=current_user.id).all()
#     return render_template('listar_reproduccion.html', reproducciones=reproducciones)

 
 










