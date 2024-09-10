from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db
from app.forms import OvejaForm, ReproduccionForm, saludForm, AlimentacionForm, VentaForm, CompraForm, LoginForm, RegistrationForm
from app.models import Oveja,Reproduccion, Salud, Alimentacion, Venta, Compra, Finanzas, User
from sqlalchemy import func

@app.route('/')
@login_required
def index():
    return render_template('index.html')

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

@app.route('/listar_ovejas')
@login_required
def listar_ovejas():
    ovejas = Oveja.query.filter_by(user_id=current_user.id).all()
    return render_template('listar_ovejas.html', ovejas=ovejas)

@app.route('/registrar_oveja', methods=['GET', 'POST'])
@login_required
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
            user_id=current_user.id  # Asignar el user_id del usuario actual
        )
        db.session.add(nueva_oveja)
        db.session.commit()
        flash('Oveja registrada exitosamente!', 'success')
        return redirect(url_for('listar_ovejas'))
    return render_template('registro_oveja.html', form=form)

@app.route('/editar_oveja/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_oveja(id):
    oveja = Oveja.query.filter_by(id=id, user_id=current_user.id).first_or_404()
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
@login_required
def eliminar_oveja(id):
    oveja = Oveja.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    db.session.delete(oveja)
    db.session.commit()
    flash('Oveja eliminada correctamente', 'success')
    return redirect(url_for('listar_ovejas'))

@app.route('/registrar_reproduccion', methods=['GET', 'POST'])
@login_required
def registrar_reproduccion():
    form = ReproduccionForm()
    if form.validate_on_submit():
        nueva_reproduccion = Reproduccion(
            id_oveja=form.id_oveja.data,
            fecha_apareamiento=form.fecha_apareamiento.data,
            id_macho=form.id_macho.data if form.id_macho.data is not None else None,
            fecha_parto=form.fecha_parto.data if form.fecha_parto.data is not None else None,
            num_crias=form.num_crias.data if form.num_crias.data is not None else None,
            user_id=current_user.id  # Asignar el user_id del usuario actual
        )
        db.session.add(nueva_reproduccion)
        db.session.commit()
        flash('Evento de reproducción registrado exitosamente!', 'success')
        return redirect(url_for('listar_reproduccion'))
    return render_template('registrar_reproduccion.html', form=form)

@app.route('/listar_reproduccion')
@login_required
def listar_reproduccion():
    reproducciones = Reproduccion.query.filter_by(user_id=current_user.id).all()
    return render_template('listar_reproduccion.html', reproducciones=reproducciones)

@app.route('/editar_reproduccion/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_reproduccion(id):
    reproduccion = Reproduccion.query.filter_by(id=id, user_id=current_user.id).first_or_404()
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

@app.route('/eliminar_reproduccion/<int:id>', methods=['POST'])
@login_required
def eliminar_reproduccion(id):
    reproduccion = Reproduccion.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    db.session.delete(reproduccion)
    db.session.commit()
    flash('Reproducción eliminada correctamente', 'success')
    return redirect(url_for('listar_reproduccion'))

@app.route('/registrar_salud', methods=['GET', 'POST'])
@login_required
def registrar_salud():
    form = saludForm()
    if form.validate_on_submit():
        nuevo_registro = Salud(
            id_oveja=form.id_oveja.data,
            fecha=form.fecha.data,
            tipo_tratamiento=form.tipo_tratamiento.data,
            detalle=form.detalle.data,
            user_id=current_user.id  # Asignar el user_id del usuario actual
        )
        db.session.add(nuevo_registro)
        db.session.commit()
        flash('Registro de salud registrado exitosamente!', 'success')
        return redirect(url_for('listar_salud'))
    return render_template('registrar_salud.html', form=form)

@app.route('/listar_salud')
@login_required
def listar_salud():
    salud = Salud.query.filter_by(user_id=current_user.id).all()
    return render_template('listar_salud.html', salud=salud)

@app.route('/editar_salud/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_salud(id):
    salud = Salud.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    form = saludForm(obj=salud)
    if form.validate_on_submit():
        salud.id_oveja = form.id_oveja.data
        salud.fecha = form.fecha.data
        salud.tipo_tratamiento = form.tipo_tratamiento.data
        salud.detalle = form.detalle.data
        db.session.commit()
        flash('Registro de salud actualizado con éxito', 'success')
        return redirect(url_for('listar_salud'))
    return render_template('editar_salud.html', form=form, salud=salud)

@app.route('/eliminar_salud/<int:id>', methods=['POST'])
@login_required
def eliminar_salud(id):
    salud = Salud.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    db.session.delete(salud)
    db.session.commit()
    flash('Registro de salud eliminado correctamente', 'success')
    return redirect(url_for('listar_salud'))

@app.route('/registrar_alimentacion', methods=['GET', 'POST'])
@login_required
def registrar_alimentacion():
    form = AlimentacionForm()
    if form.validate_on_submit():
        nueva_alimentacion = Alimentacion(
            id_oveja=form.id_oveja.data,
            fecha=form.fecha.data,
            tipo_alimento=form.tipo_alimento.data,
            cantidad=form.cantidad.data,
            user_id=current_user.id  # Asignar el user_id del usuario actual
        )
        db.session.add(nueva_alimentacion)
        db.session.commit()
        flash('Alimentación registrada exitosamente!', 'success')
        return redirect(url_for('listar_alimentacion'))
    return render_template('registrar_alimentacion.html', form=form)

@app.route('/listar_alimentacion')
@login_required
def listar_alimentacion():
    alimentaciones = Alimentacion.query.filter_by(user_id=current_user.id).all()
    return render_template('listar_alimentacion.html', alimentaciones=alimentaciones)

@app.route('/editar_alimentacion/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_alimentacion(id):
    alimentacion = Alimentacion.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    form = AlimentacionForm(obj=alimentacion)
    if form.validate_on_submit():
        alimentacion.id_oveja = form.id_oveja.data
        alimentacion.fecha = form.fecha.data
        alimentacion.tipo_alimento = form.tipo_alimento.data
        alimentacion.cantidad = form.cantidad.data
        db.session.commit()
        flash('Alimentación actualizada con éxito', 'success')
        return redirect(url_for('listar_alimentacion'))
    return render_template('editar_alimentacion.html', form=form)

@app.route('/eliminar_alimentacion/<int:id>', methods=['POST'])
@login_required
def eliminar_alimentacion(id):
    alimentacion = Alimentacion.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    db.session.delete(alimentacion)
    db.session.commit()
    flash('Alimentación eliminada correctamente', 'success')
    return redirect(url_for('listar_alimentacion'))

@app.route('/registrar_venta', methods=['GET', 'POST'])
@login_required
def registrar_venta():
    form = VentaForm()
    if form.validate_on_submit():
        nueva_venta = Venta(
            id_oveja=form.id_oveja.data,
            fecha=form.fecha.data,
            cantidad=form.cantidad.data,
            precio=form.precio.data,
            user_id=current_user.id  # Asignar el user_id del usuario actual
        )
        db.session.add(nueva_venta)
        db.session.commit()
        flash('Venta registrada exitosamente!', 'success')
        return redirect(url_for('listar_venta'))
    return render_template('registrar_venta.html', form=form)

@app.route('/listar_ventas')
@login_required
def listar_venta():
    ventas = Venta.query.filter_by(user_id=current_user.id).all()
    return render_template('listar_ventas.html', ventas=ventas)

@app.route('/editar_venta/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_venta(id):
    venta = Venta.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    form = VentaForm(obj=venta)
    if form.validate_on_submit():
        venta.id_oveja = form.id_oveja.data
        venta.fecha = form.fecha.data
        venta.cantidad = form.cantidad.data
        venta.precio = form.precio.data
        db.session.commit()
        flash('Venta actualizada con éxito', 'success')
        return redirect(url_for('listar_ventas'))
    return render_template('editar_venta.html', form=form)

@app.route('/eliminar_venta/<int:id>', methods=['POST'])
@login_required
def eliminar_venta(id):
    venta = Venta.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    db.session.delete(venta)
    db.session.commit()
    flash('Venta eliminada correctamente', 'success')
    return redirect(url_for('listar_ventas'))

@app.route('/registrar_compra', methods=['GET', 'POST'])
@login_required
def registrar_compra():
    form = CompraForm()
    if form.validate_on_submit():
        nueva_compra = Compra(
            tipo_producto=form.tipo_producto.data,
            descripcion=form.descripcion.data,
            cantidad=form.cantidad.data,
            precio=form.precio.data,
            fecha=form.fecha.data,
            user_id=current_user.id  # Asignar el user_id del usuario actual
        )
        db.session.add(nueva_compra)
        db.session.commit()
        flash('Compra registrada exitosamente!', 'success')
        return redirect(url_for('listar_compra'))  # Asegúrate de que la ruta listar_compras esté definida
    return render_template('registrar_compra.html', form=form)

@app.route('/listar_compras')
@login_required
def listar_compra():
    compras = Compra.query.filter_by(user_id=current_user.id).all()
    return render_template('listar_compra.html', compras=compras)

@app.route('/editar_compra/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_compra(id):
    compra = Compra.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    form = CompraForm(obj=compra)
    if form.validate_on_submit():
        compra.fecha = form.fecha.data
        compra.proveedor = form.proveedor.data
        compra.cantidad = form.cantidad.data
        compra.precio = form.precio.data
        db.session.commit()
        flash('Compra actualizada con éxito', 'success')
        return redirect(url_for('listar_compras'))
    return render_template('editar_compra.html', form=form)

@app.route('/eliminar_compra/<int:id>', methods=['POST'])
@login_required
def eliminar_compra(id):
    compra = Compra.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    db.session.delete(compra)
    db.session.commit()
    flash('Compra eliminada correctamente', 'success')
    return redirect(url_for('listar_compras'))

@app.route('/listar_finanzas')
@login_required
def listar_finanzas():
    finanzas = Finanzas.query.order_by(Finanzas.fecha.desc()).all()
    return render_template('listar_finanzas.html', finanzas=finanzas)

@app.route('/analisis_financiero')
@login_required
def analisis_financiero():
    ventas_total = db.session.query(func.sum(Venta.precio)).scalar() or 0
    compras_total = db.session.query(func.sum(Compra.precio)).scalar() or 0
    saldo_total = ventas_total - compras_total
    return render_template('analisis_financiero.html', ventas_total=ventas_total, compras_total=compras_total, saldo_total=saldo_total)

@app.route('/informe_mensual')
@login_required
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
@login_required
def oveja ():
    return render_template('ovejas.html')

@app.route('/salud')
@login_required
def salud():
    return render_template('salud.html')

@app.route('/reproduccion')
@login_required
def reproduccion():
    return render_template('reproduccion.html')

@app.route('/alimentacion')
@login_required
def alimentacion():
    return render_template('alimentacion.html')


@app.route('/inventario')
@login_required
def inventario ():
    return render_template('inventario.html')

@app.route('/finanzas')
@login_required
def finanzas():
    return render_template('finanzas.html')

@app.route('/venta')
@login_required
def venta():
    return render_template('venta.html')

@app.route('/compra')
@login_required
def compra():
    return render_template('compra.html')


