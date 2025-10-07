# 🎓 Tutoriza - Sistema de Gestión de Asesorías

Proyecto de certificación desarrollado con Flask, MySQL y arquitectura MVC.

## 📋 Características Implementadas

### ✅ Requisitos Básicos (Aprobación)
- ✔️ Inicio de sesión y Registro con validaciones completas
- ✔️ Los errores de validación se muestran en la página
- ✔️ Cerrar sesión funcional
- ✔️ Página Principal con dashboard de asesorías
- ✔️ Enlace "Borrar" aparece solo si el usuario creó la asesoría
- ✔️ Enlace "Editar" aparece solo si el usuario creó la asesoría
- ✔️ Dashboard muestra "Bienvenido {{ nombre de usuario }}"
- ✔️ Enlace "Ver" redirecciona a página individual
- ✔️ Crear nueva asesoría (solo usuarios autenticados)
- ✔️ Validaciones: campos vacíos, duración 1-8, notas max 50 caracteres
- ✔️ Editar asesoría (solo usuario autenticado y creador)
- ✔️ Campos pre-populados en edición
- ✔️ HTML y CSS con Bootstrap (>75% precisión vs mockups)

### 🌟 Requisitos BONUS (Certificación ORO)
- ✔️ Dashboard NO muestra asesorías con fechas pasadas
- ✔️ NO se puede crear asesoría con fecha en el pasado
- ✔️ Selector de tutor en creación (todos los usuarios excepto el actual)
- ✔️ Selector de tutor en edición
- ✔️ Cambiar tutor desde vista individual (todos excepto creador)

## 🛠️ Tecnologías Utilizadas

- **Backend:** Flask 3.0.0
- **Base de Datos:** MySQL
- **Autenticación:** Flask-Bcrypt
- **Frontend:** Bootstrap 5.3.0, HTML5, CSS3
- **Arquitectura:** MVC (Model-View-Controller)

## 📁 Estructura del Proyecto

```
Certificacion/
│
├── flask_app/
│   ├── config/
│   │   ├── __init__.py
│   │   └── mysqlconnection.py
│   │
│   ├── controllers/
│   │   ├── __init__.py
│   │   ├── users.py
│   │   └── asesorias.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── asesoria.py
│   │
│   ├── static/
│   │   └── css/
│   │       └── style.css
│   │
│   ├── templates/
│   │   ├── index.html
│   │   ├── dashboard.html
│   │   ├── nueva_asesoria.html
│   │   ├── editar_asesoria.html
│   │   └── ver_asesoria.html
│   │
│   └── __init__.py
│
├── server.py
├── requirements.txt
├── schema.sql
└── README.md
```

## 🚀 Instalación y Configuración

### Prerequisitos
- Python 3.8 o superior
- MySQL Server instalado y corriendo
- pip (gestor de paquetes de Python)

### Paso 1: Clonar o descargar el proyecto

```bash
cd C:\Users\AML-Invitado\OneDrive\Documents\Certificacion
```

### Paso 2: Crear entorno virtual (opcional pero recomendado)

```powershell
python -m venv venv
.\venv\Scripts\activate
```

### Paso 3: Instalar dependencias

```powershell
pip install -r requirements.txt
```

### Paso 4: Configurar MySQL

1. Abre MySQL Workbench o línea de comandos MySQL
2. Ejecuta el archivo `schema.sql`:

```sql
mysql -u root -p < schema.sql
```

O copia y pega el contenido del archivo en MySQL Workbench.

### Paso 5: Verificar configuración de base de datos

Abre `flask_app/config/mysqlconnection.py` y verifica:

```python
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='root',  # Cambia esto si tu password es diferente
    db=db,
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor,
    autocommit=True
)
```

### Paso 6: Ejecutar la aplicación

```powershell
python server.py
```

La aplicación estará disponible en: **http://localhost:5000**

## 📊 Base de Datos

### Tabla `users`
```sql
- id (INT, AUTO_INCREMENT, PRIMARY KEY)
- nombre (VARCHAR 100)
- apellido (VARCHAR 100)
- email (VARCHAR 255, UNIQUE)
- password (VARCHAR 255, encriptado)
- created_at (DATETIME)
- updated_at (DATETIME)
```

### Tabla `asesorias`
```sql
- id (INT, AUTO_INCREMENT, PRIMARY KEY)
- tema (VARCHAR 255)
- fecha (DATE)
- duracion (INT) - entre 1 y 8 horas
- notas (TEXT) - máximo 50 caracteres
- user_id (INT, FOREIGN KEY -> users.id)
- tutor_id (INT, FOREIGN KEY -> users.id, nullable)
- created_at (DATETIME)
- updated_at (DATETIME)
```

## 🔐 Validaciones Implementadas

### Registro:
- Nombre y apellido: mínimo 3 caracteres
- Email: formato válido y único en BD
- Contraseña: mínimo 8 caracteres
- Confirmar contraseña: debe coincidir

### Login:
- Email debe estar registrado en BD
- Contraseña debe ser correcta (validación con bcrypt)

### Asesorías:
- Tema: no puede estar vacío
- Fecha: no puede estar vacía ni ser del pasado (BONUS)
- Duración: número entre 1 y 8
- Notas: máximo 50 caracteres

## 🌐 Despliegue (Para Certificación ORO)

### Opción 1: PythonAnywhere (Recomendado - Gratis)

1. **Crear cuenta en PythonAnywhere:**
   - Ve a https://www.pythonanywhere.com
   - Crea una cuenta gratuita

2. **Subir archivos:**
   - Usa la consola Bash o sube archivos desde "Files"
   - Clona tu repositorio o sube los archivos manualmente

3. **Configurar base de datos MySQL:**
   ```bash
   mysql -u USUARIO -h USUARIO.mysql.pythonanywhere-services.com -p NOMBRE_BD < schema.sql
   ```

4. **Actualizar configuración:**
   Edita `flask_app/config/mysqlconnection.py`:
   ```python
   connection = pymysql.connect(
       host='USUARIO.mysql.pythonanywhere-services.com',
       user='USUARIO',
       password='TU_PASSWORD',
       db='USUARIO$certificacion',
       ...
   )
   ```

5. **Configurar Web App:**
   - Ve a "Web" tab
   - Add a new web app
   - Selecciona Flask y Python 3.10
   - Configura WSGI file:
   ```python
   import sys
   path = '/home/USUARIO/Certificacion'
   if path not in sys.path:
       sys.path.append(path)
   
   from server import app as application
   ```

6. **Instalar dependencias:**
   ```bash
   pip install --user -r requirements.txt
   ```

7. **Recargar la aplicación**

### Opción 2: Railway (Fácil y Gratis)

1. **Instalar Railway CLI:**
   ```powershell
   npm i -g @railway/cli
   ```

2. **Inicializar proyecto:**
   ```bash
   railway login
   railway init
   ```

3. **Agregar MySQL:**
   - Ve al dashboard de Railway
   - Add MySQL database
   - Copia las credenciales

4. **Actualizar variables de entorno:**
   Crea `.env`:
   ```
   MYSQL_HOST=containers-us-west-xxx.railway.app
   MYSQL_USER=root
   MYSQL_PASSWORD=xxx
   MYSQL_DATABASE=railway
   ```

5. **Crear Procfile:**
   ```
   web: gunicorn server:app
   ```

6. **Actualizar requirements.txt:**
   ```
   Flask==3.0.0
   PyMySQL==1.1.0
   flask-bcrypt==1.0.1
   gunicorn==21.2.0
   python-dotenv==1.0.0
   ```

7. **Desplegar:**
   ```bash
   railway up
   ```

### Opción 3: Render (Moderna y Gratis)

1. **Crear cuenta en Render:** https://render.com

2. **Crear Web Service:**
   - New > Web Service
   - Conecta tu repositorio GitHub

3. **Configuración:**
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn server:app`

4. **Agregar MySQL:**
   - Dashboard > New > PostgreSQL (o usa external MySQL)

5. **Variables de entorno:**
   Configura en Render Dashboard

6. **Deploy automático** al hacer push a GitHub

## 📝 Uso de la Aplicación

### 1. Registro
- Completa el formulario de registro
- Valida que el email sea único
- Contraseña mínima de 8 caracteres

### 2. Login
- Ingresa con email y contraseña registrados

### 3. Dashboard
- Ver todas las asesorías futuras
- Crear nueva asesoría
- Editar/Borrar solo tus asesorías

### 4. Crear Asesoría
- Completa todos los campos
- Duración entre 1-8 horas
- Notas máximo 50 caracteres
- Opcional: Seleccionar tutor

### 5. Editar Asesoría
- Solo el creador puede editar
- Campos pre-populados
- Cambiar tutor asignado

### 6. Ver Asesoría
- Cualquier usuario puede ver
- Cambiar tutor desde aquí (BONUS)

## 🎯 Criterios de Certificación

### Certificación ORO (≥95%)
- ✅ Todos los requisitos básicos
- ✅ Todos los BONUS implementados
- ✅ Código limpio y organizado (MVC)
- ✅ Bootstrap para UI profesional
- ⏱️ Tiempo de ejecución: máximo 5 horas
- 🌐 **Despliegue en hosting público** (usar guía arriba)

### Puntos Clave:
- Arquitectura MVC correctamente implementada
- Validaciones completas en frontend y backend
- Sesiones y autenticación segura
- CSS con Bootstrap (>75% similar a mockups)
- Funcionalidades BONUS todas implementadas

## 🐛 Troubleshooting

### Error: "Can't connect to MySQL server"
- Verifica que MySQL esté corriendo
- Confirma usuario y contraseña en `mysqlconnection.py`

### Error: "Module not found"
- Ejecuta: `pip install -r requirements.txt`
- Verifica que estés en el directorio correcto

### Error: "Template not found"
- Verifica que la carpeta `templates/` esté en `flask_app/`
- Los nombres de archivos son case-sensitive

### Páginas no cargan CSS
- Verifica que `static/css/style.css` exista
- Limpia caché del navegador (Ctrl + F5)

## 📧 Contacto y Soporte

Para preguntas sobre el proyecto o certificación, contacta a tu instructor.

## 📄 Licencia

Este proyecto es parte del programa de certificación y está diseñado para fines educativos.

---

**¡Éxito en tu certificación! 🚀**

Recuerda: Para certificación ORO necesitas desplegar en un hosting público. Sigue la guía de despliegue arriba.
