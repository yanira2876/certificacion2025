from flask import render_template, redirect, request, session, flash
from flask_app import app, bcrypt
from flask_app.models.user import User

# ===== PÁGINA DE REGISTRO/LOGIN =====
@app.route('/')
def index():
    # Si ya tiene sesión, redirigir al dashboard
    if 'user_id' in session:
        return redirect('/dashboard')
    return render_template('index.html')

# ===== PROCESAR REGISTRO =====
@app.route('/register', methods=['POST'])
def register():
    # Validar datos del formulario
    if not User.validate_register(request.form):
        return redirect('/')
    
    # Encriptar contraseña
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    
    # Crear diccionario con datos
    data = {
        "nombre": request.form['nombre'],
        "apellido": request.form['apellido'],
        "email": request.form['email'],
        "password": pw_hash
    }
    
    # Guardar usuario en la BD
    user_id = User.save(data)
    
    # Guardar en sesión
    session['user_id'] = user_id
    
    flash("¡Registro exitoso! Bienvenido", "success")
    return redirect('/dashboard')

# ===== PROCESAR LOGIN =====
@app.route('/login', methods=['POST'])
def login():
    # Validar credenciales
    if not User.validate_login(request.form):
        return redirect('/')
    
    # Buscar usuario por email
    data = {"email": request.form['email']}
    user_in_db = User.get_by_email(data)
    
    # Guardar en sesión
    session['user_id'] = user_in_db.id
    
    flash("¡Inicio de sesión exitoso!", "success")
    return redirect('/dashboard')

# ===== CERRAR SESIÓN =====
@app.route('/logout')
def logout():
    session.clear()
    flash("Has cerrado sesión correctamente", "info")
    return redirect('/')
