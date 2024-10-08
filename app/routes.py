from flask import render_template, redirect, url_for, session, Response
from app import app, db
from app.forms import OvejaForm, ReproduccionForm, saludForm, AlimentacionForm, VentaForm, CompraForm 
from app.models import Oveja, Reproduccion, Salud, Alimentacion, Venta, Compra, Finanzas
from flask import render_template, redirect, url_for, flash, request,send_file
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db
from app.forms import OvejaForm, ReproduccionForm, saludForm, AlimentacionForm, VentaForm, CompraForm, LoginForm, RegistrationForm, InventarioForm, ReporteForm
from app.models import Oveja,Reproduccion, Salud, Alimentacion, Venta, Compra, Finanzas, User,Inventario

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
#----------------------------------------------------------aqui empieza las ovejas --------------------


@app.route('/listar_ovejas')
@login_required
def listar_ovejas():
    search_query = request.args.get('search', '')  # Obtener el término de búsqueda desde la solicitud
    if search_query:
        # Buscar en varios campos: nombre, raza, sexo y fecha de nacimiento
        ovejas = Oveja.query.filter(
            (Oveja.nombre.contains(search_query)) |
            (Oveja.raza.contains(search_query)) |
            (Oveja.sexo.contains(search_query)) |
            (Oveja.fecha_nacimiento.contains(search_query))|
            (Oveja.id_madre.contains(search_query))|
            (Oveja.id_padre.contains(search_query))
        ).filter_by(user_id=current_user.id).all()
    else:
        # Si no hay búsqueda, muestra todas las ovejas
        ovejas = Oveja.query.filter_by(user_id=current_user.id).all()
    return render_template('listar_ovejas.html', ovejas=ovejas, search_query=search_query)

@app.route('/registrar_oveja', methods=['GET', 'POST'])
@login_required
def registrar_oveja():
    form = OvejaForm()
    # Cargar todas las ovejas existentes para seleccionar padre y madre    
    machos = Oveja.query.filter_by(sexo='Macho',user_id=current_user.id).all()
    hembras = Oveja.query.filter_by(sexo='Hembra',user_id=current_user.id).all()
    # Agregar las opciones de ovejas machos al SelectField del padre
    form.id_padre.choices = [(0, 'Ninguno')] + [(oveja.id, f'Oveja {oveja.nombre} (ID: {oveja.id})') for oveja in machos]
    # Agregar las opciones de ovejas hembras al SelectField de la madre
    form.id_madre.choices = [(0, 'Ninguno')] + [(oveja.id, f'Oveja {oveja.nombre} (ID: {oveja.id})') for oveja in hembras]
    if form.validate_on_submit():
        nueva_oveja = Oveja(
            nombre=form.nombre.data,
            fecha_nacimiento=form.fecha_nacimiento.data,
            raza=form.raza.data,
            sexo=form.sexo.data,
            id_padre=form.id_padre.data if form.id_padre.data != 0 else None,  # Verificar si seleccionó "Ninguno"
            id_madre=form.id_madre.data if form.id_madre.data != 0 else None,  # Verificar si seleccionó "Ninguno"
            user_id=current_user.id  # Asignar el user_id del usuario actual   
        )
        db.session.add(nueva_oveja)
        db.session.commit()
        flash('Oveja registrada correctamente', 'success')
        return redirect(url_for('listar_ovejas'))
    return render_template('registro_oveja.html', form=form)

@app.route('/editar_oveja/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_oveja(id):
    oveja = Oveja.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    form = OvejaForm(obj=oveja)

    # Cargar todas las ovejas existentes para seleccionar padre y madre
    machos = Oveja.query.filter_by(sexo='Macho', user_id=current_user.id).all()
    hembras = Oveja.query.filter_by(sexo='Hembra', user_id=current_user.id).all()
    # Agregar las opciones de ovejas machos al SelectField del padre
    form.id_padre.choices = [(0, 'Ninguno')] + [(oveja.id, f'Oveja {oveja.nombre} (ID: {oveja.id})') for oveja in machos]
    # Agregar las opciones de ovejas hembras al SelectField de la madre
    form.id_madre.choices = [(0, 'Ninguno')] + [(oveja.id, f'Oveja {oveja.nombre} (ID: {oveja.id})') for oveja in hembras]
    if form.validate_on_submit():
        oveja.nombre = form.nombre.data
        oveja.fecha_nacimiento = form.fecha_nacimiento.data
        oveja.raza = form.raza.data
        oveja.sexo = form.sexo.data
        oveja.id_padre = form.id_padre.data if form.id_padre.data != 0 else None
        oveja.id_madre = form.id_madre.data if form.id_madre.data != 0 else None  
        db.session.commit()
        flash('Oveja editada correctamente!', 'success')
        return redirect(url_for('listar_ovejas'))
    return render_template('editar_oveja.html', form=form)

@app.route('/eliminar_oveja/<int:id>', methods=['POST'])
@login_required
def eliminar_oveja(id):
    oveja = Oveja.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    try:
        # Eliminar referencias de la oveja como padre o madre en otras ovejas
        for hijo in oveja.hijos_padre:
            hijo.id_padre = None
        for hijo in oveja.hijos_madre:
            hijo.id_madre = None
        # Finalmente, eliminar la oveja
        db.session.delete(oveja)
        db.session.commit()
        flash('Oveja eliminada correctamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar la oveja: {str(e)}', 'danger')
    
    return redirect(url_for('listar_ovejas'))
#-----------------------------------------------------------------aqui termina-------------------------

#-----------------------------------------------------------------reproduccion-------------------------

@app.route('/registrar_reproduccion', methods=['GET', 'POST'])
@login_required
def registrar_reproduccion():
    form = ReproduccionForm()

    # Cargar las ovejas (hembras) y machos desde la base de datos
    hembras = Oveja.query.filter_by(sexo='Hembra', user_id=current_user.id).all()
    machos = Oveja.query.filter_by(sexo='Macho', user_id=current_user.id).all()

    # Agregar las opciones de ovejas hembras al SelectField
    form.id_oveja.choices = [(hembra.id, f'Oveja {hembra.nombre} (ID: {hembra.id})') for hembra in hembras]
    
    # Agregar las opciones de ovejas machos al SelectField con opción "Ninguno"
    form.id_macho.choices = [(0, 'Ninguno')] + [(macho.id, f'Oveja {macho.nombre} (ID: {macho.id})') for macho in machos]

    if form.validate_on_submit():
        nueva_reproduccion = Reproduccion(
            id_oveja=form.id_oveja.data,
            fecha_apareamiento=form.fecha_apareamiento.data,
            id_macho=form.id_macho.data if form.id_macho.data != 0 else None,  # Verificar si seleccionó "Ninguno"
            fecha_parto=form.fecha_parto.data if form.fecha_parto.data else None,
            num_crias=form.num_crias.data if form.num_crias.data else None,
            user_id=current_user.id  # Asignar el user_id del usuario actual
        )
        db.session.add(nueva_reproduccion)
        db.session.commit()
        flash('Registro de reproducción creado exitosamente!', 'success')
        return redirect(url_for('listar_reproduccion'))

    return render_template('registrar_reproduccion.html', form=form)
#-----------------------------------------------------------------------------------------------------------termina--------

@app.route('/listar_reproduccion')
@login_required
def listar_reproduccion():
    search_query = request.args.get('search', '')  # Obtener el término de búsqueda desde la solicitud
    # Filtrar las reproducciones según el término de búsqueda
    if search_query:
        # Buscar por id_oveja, id_macho, o cualquier otro campo que desees
        reproducciones = Reproduccion.query.filter(
            (Reproduccion.id_oveja.contains(search_query)) |
            (Reproduccion.id_macho.contains(search_query)) |
            (Reproduccion.fecha_apareamiento.contains(search_query)) |
            (Reproduccion.fecha_parto.contains(search_query))
        ).filter_by(user_id=current_user.id).all()
    else:
        # Si no hay búsqueda, muestra todas las reproducciones
        reproducciones = Reproduccion.query.filter_by(user_id=current_user.id).all()

    return render_template('listar_reproduccion.html', reproducciones=reproducciones)



@app.route('/editar_reproduccion/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_reproduccion(id):
    reproduccion = Reproduccion.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    form = ReproduccionForm(obj=reproduccion)
    # Cargar todas las ovejas existentes para seleccionar id_oveja y id_macho
    ovejas = Oveja.query.filter_by(user_id=current_user.id).all()
    # Agregar las opciones de ovejas al SelectField para id_oveja
    form.id_oveja.choices = [(oveja.id, f'Oveja {oveja.nombre} (ID: {oveja.id})') for oveja in ovejas]
    # Agregar las opciones de ovejas machos al SelectField para id_macho
    machos = Oveja.query.filter_by(sexo='Macho', user_id=current_user.id).all()
    form.id_macho.choices = [(0, 'Ninguno')] + [(oveja.id, f'Oveja {oveja.nombre} (ID: {oveja.id})') for oveja in machos]
    if form.validate_on_submit():
        reproduccion.id_oveja = form.id_oveja.data
        reproduccion.fecha_apareamiento = form.fecha_apareamiento.data
        reproduccion.id_macho = form.id_macho.data if form.id_macho.data != 0 else None
        reproduccion.fecha_parto = form.fecha_parto.data if form.fecha_parto.data else None
        reproduccion.num_crias = form.num_crias.data if form.num_crias.data else None
        db.session.commit()
        flash('Registro editado!', 'success')
        return redirect(url_for('listar_reproduccion'))
    return render_template('editar_reproduccion.html', form=form)

@app.route('/eliminar_reproduccion/<int:id>', methods=['POST'])
@login_required
def eliminar_reproduccion(id):
    reproduccion = Reproduccion.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    db.session.delete(reproduccion)
    db.session.commit()
    flash('registro eliminado!', 'success')
    return redirect(url_for('listar_reproduccion'))
#----------------------------------------------------------------------termina reproduccion-------------

#---------------------------------------------------------------------salud-------------------------

@app.route('/registrar_salud', methods=['GET', 'POST'])
@login_required
def registrar_salud():
    form = saludForm()
    ovejas = Oveja.query.filter_by(user_id=current_user.id).all()
    form.id_oveja.choices =[(oveja.id, f'Oveja {oveja.nombre} (ID: {oveja.id})') for oveja in ovejas]
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
        flash('tratamiento registrado!', 'success')
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
        flash('tratamiento editado!', 'success')
        return redirect(url_for('listar_salud'))
    return render_template('editar_salud.html', form=form, salud=salud)

@app.route('/eliminar_salud/<int:id>', methods=['POST'])
@login_required
def eliminar_salud(id):
    salud = Salud.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    db.session.delete(salud)
    db.session.commit()
    flash('tratamiento eliminado!', 'success')
    return redirect(url_for('listar_salud'))
#--------------------------------------------------------------termina salud----------------------------

#--------------------------------------------------------------alimentación-----------------------------

@app.route('/registrar_alimentacion', methods=['GET', 'POST'])
@login_required
def registrar_alimentacion():
    form = AlimentacionForm()
    oveja = Oveja.query.filter_by(user_id=current_user.id).all()
    form.id_oveja.choices = [(0, 'Ninguno')] + [(oveja.id, f'Oveja {oveja.nombre} (ID: {oveja.id})') for oveja in oveja]
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

        # Emitir notificación a todos los clientes
        flash('alimento registrado!', 'success')
        return redirect(url_for('listar_alimentacion'))  # Redirige a la vista de notificaciones # Redirige a la vista de notificaciones
    return render_template('registrar_alimentacion.html', form=form)

@app.route('/listar_alimentacion')
@login_required
def listar_alimentacion():
    search_query = request.args.get('search', '')  # Obtener el término de búsqueda desde la solicitud
    if search_query:
        # Buscar en varios campos: tipo de alimento, fecha, cantidad
        alimentaciones = Alimentacion.query.filter(
            (Alimentacion.tipo_alimento.contains(search_query)) |
            (Alimentacion.fecha.contains(search_query)) |
            (Alimentacion.cantidad.contains(search_query)) |
            (Oveja.nombre.contains(search_query))  # Filtrar por nombre de la oveja también
        ).join(Oveja).filter(Alimentacion.user_id == current_user.id).all()  # Solo alimentaciones del usuario actual
    else:
        # Si no hay búsqueda, muestra todas las alimentaciones
        alimentaciones = Alimentacion.query.filter_by(user_id=current_user.id).all()
    
    return render_template('listar_alimentacion.html', alimentaciones=alimentaciones, search_query=search_query)


@app.route('/editar_alimentacion/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_alimentacion(id):
    alimentacion = Alimentacion.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    form = AlimentacionForm(obj=alimentacion)
    oveja = Oveja.query.filter_by(user_id=current_user.id).all()
    form.id_oveja.choices = [(0, 'Ninguno')] + [(oveja.id, f'Oveja {oveja.nombre} (ID: {oveja.id})') for oveja in oveja]
    if form.validate_on_submit():
        alimentacion.id_oveja = form.id_oveja.data
        alimentacion.fecha = form.fecha.data
        alimentacion.tipo_alimento = form.tipo_alimento.data
        alimentacion.cantidad = form.cantidad.data
        db.session.commit()

        flash('alimento editado!', 'success')
        return redirect(url_for('listar_alimentacion'))

    return render_template('editar_alimentacion.html', form=form)

@app.route('/eliminar_alimentacion/<int:id>', methods=['POST'])
@login_required
def eliminar_alimentacion(id):
    alimentacion = Alimentacion.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    db.session.delete(alimentacion)
    db.session.commit()
    flash('alimento eliminado!', 'success')
    return redirect(url_for('listar_alimentacion'))
#---------------------------------------------------------------termina alimentacion------------------

#---------------------------------------------------------------ventas-------------------------------

#--
@app.route('/registrar_venta', methods=['GET', 'POST'])
@login_required
def registrar_venta():
    form = VentaForm()
    ovejas = Oveja.query.filter_by(user_id=current_user.id).all()
    form.id_oveja.choices = [(0, 'Ninguno')] + [(oveja.id, f'Oveja {oveja.nombre} (ID: {oveja.id})') for oveja in ovejas]
    if form.validate_on_submit():
        nueva_venta = Venta(
            id_oveja=form.id_oveja.data,
            fecha=form.fecha.data,
            cantidad=form.cantidad.data,
            precio=form.precio.data,
            user_id=current_user.id
        )
        db.session.add(nueva_venta)
        db.session.commit()

        # Crear una nueva transacción en Finanzas con referencia a la nueva venta
        nueva_finanza = Finanzas(
            tipo="Venta",
            descripcion=f'Venta de oveja {form.id_oveja.data}',
            monto=form.cantidad.data * form.precio.data,
            fecha=form.fecha.data,
            user_id=current_user.id,
            venta_id=nueva_venta.id  # Establecer la referencia de la venta
        )
        db.session.add(nueva_finanza)
        db.session.commit()

        flash('Venta registrada exitosamente!', 'success')
        return redirect(url_for('listar_venta'))
    
    return render_template('registrar_venta.html', form=form)

@app.route('/listar_ventas', methods=['GET'])
@login_required
def listar_venta():
    search_query = request.args.get('search', '')

    if search_query:
        ventas = Venta.query.filter(
            (Venta.id.like(f'%{search_query}%')) |
            (Venta.id_oveja.like(f'%{search_query}%')) |
            (Venta.precio.like(f'%{search_query}%'))
        ).filter_by(user_id=current_user.id).all()
    else:
        ventas = Venta.query.filter_by(user_id=current_user.id).all()

    return render_template('listar_ventas.html', ventas=ventas)

@app.route('/editar_venta/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_venta(id):
    venta = Venta.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    form = VentaForm(obj=venta)
    ovejas = Oveja.query.filter_by(user_id=current_user.id).all()
    form.id_oveja.choices = [(0, 'Ninguno')] + [(oveja.id, f'Oveja {oveja.nombre} (ID: {oveja.id})') for oveja in ovejas]
    if form.validate_on_submit():
        venta.id_oveja = form.id_oveja.data
        venta.fecha = form.fecha.data
        venta.cantidad = form.cantidad.data
        venta.precio = form.precio.data
        db.session.commit()

        # Actualizar la entrada correspondiente en Finanzas
        finanza = Finanzas.query.filter_by(venta_id=venta.id, user_id=current_user.id).first_or_404()
        finanza.monto = form.cantidad.data * form.precio.data
        finanza.fecha = form.fecha.data
        finanza.descripcion = f'Venta de oveja {venta.id_oveja}'
        db.session.commit()

        flash('Venta actualizada con éxito', 'success')
        return redirect(url_for('listar_venta'))

    return render_template('editar_venta.html', form=form, venta=venta)

@app.route('/eliminar_venta/<int:id>', methods=['POST'])
@login_required
def eliminar_venta(id):
    venta = Venta.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    finanza = Finanzas.query.filter_by(venta_id=venta.id, user_id=current_user.id).first()
    
    if finanza:
        db.session.delete(finanza)  # Eliminar la entrada de Finanzas si existe
    
    db.session.delete(venta)  # Eliminar la venta
    db.session.commit()
    flash('Venta eliminada!', 'success')
    return redirect(url_for('listar_venta'))
  
#-----------------------------------------------------------------termina venta-----------------------------

#-----------------------------------------------------------------compra--------------------------------
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
            user_id=current_user.id
        )
        db.session.add(nueva_compra)
        db.session.commit()
        # Crear una nueva transacción en Finanzas con compra_id
        nueva_finanza = Finanzas(
            tipo="Compra",
            descripcion=f'Compra de {form.descripcion.data}',
            monto=form.cantidad.data * form.precio.data,
            fecha=form.fecha.data,
            user_id=current_user.id,
            compra_id=nueva_compra.id  # Guardar el ID de la compra
        )
        db.session.add(nueva_finanza)
        db.session.commit()
        flash('Compra registrada exitosamente!', 'success')
        return redirect(url_for('listar_compra'))
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
        # Actualizar compra
        compra.tipo_producto = form.tipo_producto.data
        compra.descripcion = form.descripcion.data
        compra.cantidad = form.cantidad.data
        compra.precio = form.precio.data
        compra.fecha = form.fecha.data
        db.session.commit()
        # Actualizar la entrada en Finanzas
        finanza = Finanzas.query.filter_by(compra_id=compra.id, user_id=current_user.id).first()
        if not finanza:
            flash('No se encontró la entrada en Finanzas para actualizar.', 'error')
            return redirect(url_for('listar_compra'))
        finanza.monto = form.cantidad.data * form.precio.data
        finanza.fecha = form.fecha.data
        finanza.descripcion = f'Compra de {form.descripcion.data}'  # Puedes ajustar esto si es necesario
        db.session.commit()
        flash('Compra editada!', 'success')
        return redirect(url_for('listar_compra'))
    return render_template('editar_compra.html', form=form, compra=compra)

@app.route('/eliminar_compra/<int:id>', methods=['POST'])
@login_required
def eliminar_compra(id):
    compra = Compra.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    finanza = Finanzas.query.filter_by(compra_id=compra.id, user_id=current_user.id).first() 
    if finanza:
        db.session.delete(finanza)
    # Eliminar la compra
    db.session.delete(compra)
    db.session.commit()
    flash('Compra eliminada!', 'success')
    return redirect(url_for('listar_compra'))
#--------------------------------------------------finaliza compra---------------------------------------

#-----------------------------------------------------finanzas-------------------------------------
@app.route('/listar_finanzas')
@login_required
def listar_finanzas():
    search_query = request.args.get('search', '')  # Obtener el término de búsqueda desde la solicitud
    # Filtrar las finanzas según el término de búsqueda
    if search_query:
        # Buscar en los campos tipo, descripción, monto y fecha
        finanzas = Finanzas.query.filter(
            (Finanzas.tipo.contains(search_query)) |
            (Finanzas.descripcion.contains(search_query)) |
            (Finanzas.monto.like(f"%{search_query}%")) |  # Para buscar por monto, aunque sea float
            (Finanzas.fecha.like(f"%{search_query}%"))    # Para buscar por fecha
        ).filter_by(user_id=current_user.id).order_by(Finanzas.fecha.desc()).all()
    else:
        # Si no hay búsqueda, mostrar todas las finanzas
        finanzas = Finanzas.query.filter_by(user_id=current_user.id).order_by(Finanzas.fecha.desc()).all()
    return render_template('listar_finanzas.html', finanzas=finanzas)
#----------------------------------------------------------------------analisis financiero------------

@app.route('/analisis_financiero')
@login_required
def analisis_financiero():
    ventas_total = db.session.query(func.sum(Venta.precio)).filter(Venta.user_id == current_user.id).scalar() or 0
    compras_total = db.session.query(func.sum(Compra.precio)).filter(Compra.user_id == current_user.id).scalar() or 0
    saldo_total = ventas_total - compras_total
    return render_template('analisis_financiero.html', ventas_total=ventas_total, compras_total=compras_total, saldo_total=saldo_total)

@app.route('/informe_mensual')
@login_required
def informe_mensual():
    # Consultar el total de ventas por mes
    ventas_por_mes = db.session.query(
        db.func.strftime('%Y-%m', Finanzas.fecha).label('mes'),
        db.func.sum(Finanzas.monto).filter(Finanzas.tipo == 'Venta', Finanzas.user_id == current_user.id).label('total_ventas')
    ).filter(Finanzas.user_id == current_user.id).group_by(db.func.strftime('%Y-%m', Finanzas.fecha)).all()
    # Consultar el total de compras por mes
    compras_por_mes = db.session.query(
        db.func.strftime('%Y-%m', Finanzas.fecha).label('mes'),
        db.func.sum(Finanzas.monto).filter(Finanzas.tipo == 'Compra', Finanzas.user_id == current_user.id).label('total_compras')
    ).filter(Finanzas.user_id == current_user.id).group_by(db.func.strftime('%Y-%m', Finanzas.fecha)).all()
    return render_template('informe_mensual.html', ventas_por_mes=ventas_por_mes, compras_por_mes=compras_por_mes)
#-----------------------------------------------------------------------------inventario---------------------
@app.route('/listar_inventario', methods=['GET'])
@login_required
def listar_inventario():
    # Captura el término de búsqueda de los parámetros de la URL
    search_query = request.args.get('search', '')
    print(f"buscar {search_query}")
    # Filtra los elementos de inventario según el término de búsqueda
    if search_query:
        print("entra al if")
        inventario_items = Inventario.query.filter(
            (Inventario.descripcion.like(f'%{search_query}%')) |
            (Inventario.cantidad.like(f'%{search_query}%'))
        ).all()
        print(f"Finaliza el if {inventario_items}")
    else:
        # Si no hay término de búsqueda, muestra todos los elementos de inventario
        inventario_items = Inventario.query.filter_by(user_id=current_user.id).all()

    return render_template('listar_inventario.html', inventario=inventario_items)

@app.route('/inventario_nuevo', methods=['GET', 'POST'])
@login_required
def insertar_inventario():
    form = InventarioForm()
    if form.validate_on_submit():
        nuevo_item = Inventario(
            tipo=form.tipo.data,
            descripcion=form.descripcion.data,
            cantidad=form.cantidad.data,
            fecha_adquisicion=form.fecha_adquisicion.data,
            user_id=current_user.id  # Asigna el ID del usuario actual
        )
        db.session.add(nuevo_item)
        db.session.commit()
        flash('nuevo producto agregado al inenario','success')
        return redirect(url_for('listar_inventario'))
    return render_template('insertar_inventario.html', form=form)

@app.route('/inventario_editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_inventario(id):
    item = Inventario.query.get_or_404(id)
    form = InventarioForm(obj=item) 
    
    if form.validate_on_submit():
        item.tipo = form.tipo.data
        item.descripcion = form.descripcion.data
        item.cantidad = form.cantidad.data
        item.fecha_adquisicion = form.fecha_adquisicion.data
        item.user_id = current_user.id  # Actualiza el ID del usuario actual
        db.session.commit()
        flash('producto actualizado correctamente','success')
        return redirect(url_for('listar_inventario'))
    
    return render_template('editar_inventario.html', form=form, item=item)


@app.route('/inventario_eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_inventario(id):
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


@app.route('/venta')
def venta():
    return render_template('venta.html')

@app.route('/compra')
def compra():
    return render_template('compra.html')


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




 









