from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.asesoria import Asesoria
from flask_app.models.user import User

# ===== VERIFICAR SESIÓN =====
def verificar_sesion():
    if 'user_id' not in session:
        flash("Debes iniciar sesión para acceder a esta página", "error")
        return False
    return True

# ===== DASHBOARD (PÁGINA PRINCIPAL) =====
@app.route('/dashboard')
def dashboard():
    if not verificar_sesion():
        return redirect('/')
    
    # Obtener usuario actual
    data = {"id": session['user_id']}
    user = User.get_by_id(data)
    
    # BONUS: Obtener solo asesorías futuras
    asesorias = Asesoria.get_all_future()
    
    return render_template('dashboard.html', user=user, asesorias=asesorias)

# ===== MOSTRAR FORMULARIO NUEVA ASESORÍA =====
@app.route('/asesorias/nueva')
def nueva_asesoria():
    if not verificar_sesion():
        return redirect('/')
    
    # Obtener usuario actual
    data = {"id": session['user_id']}
    user = User.get_by_id(data)
    
    # BONUS: Obtener todos los usuarios excepto el actual para selector de tutor
    tutores = User.get_all_except(data)
    
    return render_template('nueva_asesoria.html', user=user, tutores=tutores)

# ===== PROCESAR CREACIÓN DE ASESORÍA =====
@app.route('/asesorias/crear', methods=['POST'])
def crear_asesoria():
    if not verificar_sesion():
        return redirect('/')
    
    # Validar datos
    if not Asesoria.validate_asesoria(request.form):
        return redirect('/asesorias/nueva')
    
    # Preparar datos
    data = {
        "tema": request.form['tema'],
        "fecha": request.form['fecha'],
        "duracion": request.form['duracion'],
        "notas": request.form['notas'],
        "user_id": session['user_id'],
        "tutor_id": request.form.get('tutor_id') if request.form.get('tutor_id') else None
    }
    
    # Guardar en BD
    Asesoria.save(data)
    
    flash("¡Asesoría creada exitosamente!", "success")
    return redirect('/dashboard')

# ===== VER ASESORÍA INDIVIDUAL =====
@app.route('/asesorias/ver/<int:id>')
def ver_asesoria(id):
    if not verificar_sesion():
        return redirect('/')
    
    # Obtener usuario actual
    data_user = {"id": session['user_id']}
    user = User.get_by_id(data_user)
    
    # Obtener asesoría
    data = {"id": id}
    asesoria = Asesoria.get_by_id(data)
    
    if not asesoria:
        flash("Asesoría no encontrada", "error")
        return redirect('/dashboard')
    
    # BONUS: Obtener todos los usuarios excepto el creador para cambiar tutor
    data_tutores = {"id": asesoria.user_id}
    tutores = User.get_all_except(data_tutores)
    
    return render_template('ver_asesoria.html', user=user, asesoria=asesoria, tutores=tutores)

# ===== MOSTRAR FORMULARIO EDITAR ASESORÍA =====
@app.route('/asesorias/editar/<int:id>')
def editar_asesoria(id):
    if not verificar_sesion():
        return redirect('/')
    
    # Obtener usuario actual
    data_user = {"id": session['user_id']}
    user = User.get_by_id(data_user)
    
    # Obtener asesoría
    data = {"id": id}
    asesoria = Asesoria.get_by_id(data)
    
    if not asesoria:
        flash("Asesoría no encontrada", "error")
        return redirect('/dashboard')
    
    # Verificar que el usuario sea el creador
    if asesoria.user_id != session['user_id']:
        flash("No tienes permiso para editar esta asesoría", "error")
        return redirect('/dashboard')
    
    # BONUS: Obtener todos los usuarios excepto el actual para selector de tutor
    tutores = User.get_all_except(data_user)
    
    return render_template('editar_asesoria.html', user=user, asesoria=asesoria, tutores=tutores)

# ===== PROCESAR ACTUALIZACIÓN DE ASESORÍA =====
@app.route('/asesorias/actualizar/<int:id>', methods=['POST'])
def actualizar_asesoria(id):
    if not verificar_sesion():
        return redirect('/')
    
    # Verificar que el usuario sea el creador
    data_asesoria = {"id": id}
    asesoria = Asesoria.get_by_id(data_asesoria)
    
    if not asesoria:
        flash("Asesoría no encontrada", "error")
        return redirect('/dashboard')
    
    if asesoria.user_id != session['user_id']:
        flash("No tienes permiso para editar esta asesoría", "error")
        return redirect('/dashboard')
    
    # Validar datos
    if not Asesoria.validate_asesoria(request.form):
        return redirect(f'/asesorias/editar/{id}')
    
    # Preparar datos
    data = {
        "id": id,
        "tema": request.form['tema'],
        "fecha": request.form['fecha'],
        "duracion": request.form['duracion'],
        "notas": request.form['notas'],
        "tutor_id": request.form.get('tutor_id') if request.form.get('tutor_id') else None
    }
    
    # Actualizar en BD
    Asesoria.update(data)
    
    flash("¡Asesoría actualizada exitosamente!", "success")
    return redirect('/dashboard')

# ===== BORRAR ASESORÍA =====
@app.route('/asesorias/eliminar/<int:id>')
def eliminar_asesoria(id):
    if not verificar_sesion():
        return redirect('/')
    
    # Verificar que el usuario sea el creador
    data = {"id": id}
    asesoria = Asesoria.get_by_id(data)
    
    if not asesoria:
        flash("Asesoría no encontrada", "error")
        return redirect('/dashboard')
    
    if asesoria.user_id != session['user_id']:
        flash("No tienes permiso para eliminar esta asesoría", "error")
        return redirect('/dashboard')
    
    # Eliminar de BD
    Asesoria.delete(data)
    
    flash("Asesoría eliminada correctamente", "success")
    return redirect('/dashboard')

# ===== BONUS: CAMBIAR TUTOR DESDE VER ASESORÍA =====
@app.route('/asesorias/cambiar_tutor/<int:id>', methods=['POST'])
def cambiar_tutor(id):
    if not verificar_sesion():
        return redirect('/')
    
    # Obtener asesoría
    data_asesoria = {"id": id}
    asesoria = Asesoria.get_by_id(data_asesoria)
    
    if not asesoria:
        flash("Asesoría no encontrada", "error")
        return redirect('/dashboard')
    
    # Verificar que el usuario sea el creador
    if asesoria.user_id != session['user_id']:
        flash("Solo el creador de la asesoría puede cambiar el tutor", "error")
        return redirect(f'/asesorias/ver/{id}')
    
    # Preparar datos
    data = {
        "id": id,
        "tutor_id": request.form.get('tutor_id') if request.form.get('tutor_id') else None
    }
    
    # Actualizar tutor
    Asesoria.update_tutor(data)
    
    flash("Tutor actualizado exitosamente", "success")
    return redirect(f'/asesorias/ver/{id}')
