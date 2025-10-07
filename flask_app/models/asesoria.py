from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from datetime import datetime, date

class Asesoria:
    DB = "certificacion"
    
    def __init__(self, data):
        self.id = data['id']
        self.tema = data['tema']
        self.fecha = data['fecha']
        self.duracion = data['duracion']
        self.notas = data['notas']
        self.user_id = data['user_id']
        self.tutor_id = data.get('tutor_id')
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
        # Información del creador (solicitante)
        self.solicitante_nombre = data.get('solicitante_nombre')
        self.solicitante_apellido = data.get('solicitante_apellido')
        
        # Información del tutor
        self.tutor_nombre = data.get('tutor_nombre')
        self.tutor_apellido = data.get('tutor_apellido')
    
    # ===== CREAR ASESORÍA =====
    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO asesorias (tema, fecha, duracion, notas, user_id, tutor_id)
            VALUES (%(tema)s, %(fecha)s, %(duracion)s, %(notas)s, %(user_id)s, %(tutor_id)s)
        """
        return connectToMySQL(cls.DB).query_db(query, data)
    
    # ===== OBTENER TODAS LAS ASESORÍAS CON INFO DE USUARIOS =====
    @classmethod
    def get_all(cls):
        query = """
            SELECT asesorias.*, 
                   users.nombre as solicitante_nombre, 
                   users.apellido as solicitante_apellido,
                   tutores.nombre as tutor_nombre,
                   tutores.apellido as tutor_apellido
            FROM asesorias
            LEFT JOIN users ON asesorias.user_id = users.id
            LEFT JOIN users as tutores ON asesorias.tutor_id = tutores.id
            ORDER BY asesorias.fecha DESC
        """
        results = connectToMySQL(cls.DB).query_db(query)
        asesorias = []
        for row in results:
            asesorias.append(cls(row))
        return asesorias
    
    # ===== OBTENER SOLO ASESORÍAS FUTURAS (BONUS) =====
    @classmethod
    def get_all_future(cls):
        query = """
            SELECT asesorias.*, 
                   users.nombre as solicitante_nombre, 
                   users.apellido as solicitante_apellido,
                   tutores.nombre as tutor_nombre,
                   tutores.apellido as tutor_apellido
            FROM asesorias
            LEFT JOIN users ON asesorias.user_id = users.id
            LEFT JOIN users as tutores ON asesorias.tutor_id = tutores.id
            WHERE asesorias.fecha >= CURDATE()
            ORDER BY asesorias.fecha ASC
        """
        results = connectToMySQL(cls.DB).query_db(query)
        asesorias = []
        for row in results:
            asesorias.append(cls(row))
        return asesorias
    
    # ===== OBTENER UNA ASESORÍA POR ID =====
    @classmethod
    def get_by_id(cls, data):
        query = """
            SELECT asesorias.*, 
                   users.nombre as solicitante_nombre, 
                   users.apellido as solicitante_apellido,
                   tutores.nombre as tutor_nombre,
                   tutores.apellido as tutor_apellido
            FROM asesorias
            LEFT JOIN users ON asesorias.user_id = users.id
            LEFT JOIN users as tutores ON asesorias.tutor_id = tutores.id
            WHERE asesorias.id = %(id)s
        """
        result = connectToMySQL(cls.DB).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])
    
    # ===== ACTUALIZAR ASESORÍA =====
    @classmethod
    def update(cls, data):
        query = """
            UPDATE asesorias 
            SET tema = %(tema)s, 
                fecha = %(fecha)s, 
                duracion = %(duracion)s, 
                notas = %(notas)s,
                tutor_id = %(tutor_id)s
            WHERE id = %(id)s
        """
        return connectToMySQL(cls.DB).query_db(query, data)
    
    # ===== ACTUALIZAR SOLO EL TUTOR (BONUS) =====
    @classmethod
    def update_tutor(cls, data):
        query = """
            UPDATE asesorias 
            SET tutor_id = %(tutor_id)s
            WHERE id = %(id)s
        """
        return connectToMySQL(cls.DB).query_db(query, data)
    
    # ===== ELIMINAR ASESORÍA =====
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM asesorias WHERE id = %(id)s"
        return connectToMySQL(cls.DB).query_db(query, data)
    
    # ===== VALIDACIÓN DE ASESORÍA =====
    @staticmethod
    def validate_asesoria(asesoria):
        is_valid = True
        
        # Validar que el tema no esté vacío
        if len(asesoria['tema'].strip()) == 0:
            flash("Tema no puede estar vacío", "error_asesoria")
            is_valid = False
        
        # Validar que la fecha no esté vacía
        if not asesoria['fecha'] or asesoria['fecha'] == '':
            flash("Fecha no puede estar vacía", "error_asesoria")
            is_valid = False
        else:
            # BONUS: Validar que la fecha no sea del pasado
            try:
                fecha_asesoria = datetime.strptime(asesoria['fecha'], '%Y-%m-%d').date()
                if fecha_asesoria < date.today():
                    flash("No puede ingresar una fecha en el pasado", "error_asesoria")
                    is_valid = False
            except ValueError:
                flash("Fecha no válida", "error_asesoria")
                is_valid = False
        
        # Validar duración (debe ser un número entre 1 y 8)
        try:
            duracion = int(asesoria['duracion'])
            if duracion < 1 or duracion > 8:
                flash("La duración debe ser un número entre 1 y 8", "error_asesoria")
                is_valid = False
        except (ValueError, KeyError):
            flash("Duración debe ser un número válido", "error_asesoria")
            is_valid = False
        
        # Validar notas (máximo 50 caracteres)
        if len(asesoria['notas']) > 50:
            flash("Notas no puede tener más de 50 caracteres", "error_asesoria")
            is_valid = False
        
        return is_valid
