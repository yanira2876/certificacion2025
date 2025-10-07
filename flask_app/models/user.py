from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Importación tardía para evitar importaciones circulares
def get_bcrypt():
    from flask_app import bcrypt
    return bcrypt

class User:
    DB = "certificacion"
    
    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    # ===== CREAR USUARIO =====
    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO users (nombre, apellido, email, password)
            VALUES (%(nombre)s, %(apellido)s, %(email)s, %(password)s)
        """
        return connectToMySQL(cls.DB).query_db(query, data)
    
    # ===== OBTENER USUARIO POR EMAIL =====
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL(cls.DB).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])
    
    # ===== OBTENER USUARIO POR ID =====
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL(cls.DB).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])
    
    # ===== OBTENER TODOS LOS USUARIOS =====
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users ORDER BY nombre, apellido"
        results = connectToMySQL(cls.DB).query_db(query)
        users = []
        for row in results:
            users.append(cls(row))
        return users
    
    # ===== OBTENER TODOS MENOS UNO (PARA SELECTOR DE TUTOR) =====
    @classmethod
    def get_all_except(cls, data):
        query = "SELECT * FROM users WHERE id != %(id)s ORDER BY nombre, apellido"
        results = connectToMySQL(cls.DB).query_db(query, data)
        users = []
        for row in results:
            users.append(cls(row))
        return users
    
    # ===== VALIDACIÓN DE REGISTRO =====
    @staticmethod
    def validate_register(user):
        is_valid = True
        
        # Validar nombre (mínimo 2 caracteres)
        if len(user['nombre']) < 2:
            flash("El nombre debe tener al menos 2 caracteres", "error_registro")
            is_valid = False
        
        # Validar apellido (mínimo 2 caracteres)
        if len(user['apellido']) < 2:
            flash("El apellido debe tener al menos 2 caracteres", "error_registro")
            is_valid = False
        
        # Validar email
        if not EMAIL_REGEX.match(user['email']):
            flash("Email debe tener un formato válido", "error_registro")
            is_valid = False
        else:
            # Verificar si el email ya existe
            data = {"email": user['email']}
            user_in_db = User.get_by_email(data)
            if user_in_db:
                flash("El email ya está registrado en la BD", "error_registro")
                is_valid = False
        
        # Validar contraseña
        if len(user['password']) < 8:
            flash("La contraseña debe tener al menos 8 caracteres", "error_registro")
            is_valid = False
        
        # Validar que las contraseñas coincidan
        if user['password'] != user['confirm_password']:
            flash("La contraseña debe ser la correspondiente a la BD", "error_registro")
            is_valid = False
        
        return is_valid
    
    # ===== VALIDACIÓN DE LOGIN =====
    @staticmethod
    def validate_login(user):
        is_valid = True
        
        # Validar email
        if not EMAIL_REGEX.match(user['email']):
            flash("El email debe estar ya registrado en BD", "error_login")
            is_valid = False
            return is_valid
        
        # Buscar usuario por email
        data = {"email": user['email']}
        user_in_db = User.get_by_email(data)
        
        if not user_in_db:
            flash("El email debe estar ya registrado en BD", "error_login")
            is_valid = False
            return is_valid
        
        # Validar contraseña
        bcrypt = get_bcrypt()
        if not bcrypt.check_password_hash(user_in_db.password, user['password']):
            flash("La contraseña debe ser la correspondiente a la BD", "error_login")
            is_valid = False
        
        return is_valid
