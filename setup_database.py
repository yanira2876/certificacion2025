# Script para configurar la base de datos MySQL
import pymysql

# Configuración de conexión
config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'charset': 'utf8mb4'
}

try:
    # Conectar a MySQL
    connection = pymysql.connect(**config)
    cursor = connection.cursor()
    
    print("✓ Conectado a MySQL")
    
    # Crear base de datos
    cursor.execute("CREATE DATABASE IF NOT EXISTS certificacion")
    print("✓ Base de datos 'certificacion' creada")
    
    # Usar la base de datos
    cursor.execute("USE certificacion")
    
    # Crear tabla users
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            apellido VARCHAR(100) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
    """)
    print("✓ Tabla 'users' creada")
    
    # Crear tabla asesorias
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS asesorias (
            id INT AUTO_INCREMENT PRIMARY KEY,
            tema VARCHAR(255) NOT NULL,
            fecha DATE NOT NULL,
            duracion INT NOT NULL,
            notas TEXT,
            user_id INT NOT NULL,
            tutor_id INT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (tutor_id) REFERENCES users(id) ON DELETE SET NULL
        )
    """)
    print("✓ Tabla 'asesorias' creada")
    
    connection.commit()
    print("\n✅ Base de datos configurada exitosamente!")
    print("   Puedes ejecutar el proyecto con: python server.py")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\nVerifica que:")
    print("1. MySQL esté corriendo")
    print("2. El usuario 'root' con password 'root' existe")
    print("3. PyMySQL esté instalado: pip install PyMySQL")
finally:
    if 'connection' in locals():
        cursor.close()
        connection.close()
