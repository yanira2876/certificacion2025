from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = 'clave_super_secreta_certificacion_2025'  # Cambiar en producción

bcrypt = Bcrypt(app)

# Importar controladores (esto registra las rutas)
from flask_app.controllers import users, asesorias
