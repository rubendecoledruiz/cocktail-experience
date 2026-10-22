# Cocktail Experience Privada

Web de una página para la experiencia de coctelería privada de Rubén Ruiz. Está hecha con Flask, HTML, CSS y JavaScript. Las solicitudes del formulario se guardan en `instance/reservas.csv`; no necesita base de datos.

## Estructura

```text
mi-python/
├── app.py
├── requirements.txt
├── README.md
├── templates/
│   └── index.html
├── static/
│   ├── css/
│   │   └── styles.css
│   └── js/
│       └── script.js
└── instance/                 # Se crea automáticamente al recibir una reserva
    └── reservas.csv
```

## Ejecutar en Visual Studio Code

1. Abre la carpeta del proyecto en VS Code.
2. Abre **Terminal > New Terminal**.
3. Crea un entorno virtual:
   - Windows: `py -m venv .venv`
   - macOS/Linux: `python3 -m venv .venv`
4. Actívalo:
   - PowerShell: `.\.venv\Scripts\Activate.ps1`
   - Símbolo del sistema: `.\.venv\Scripts\activate.bat`
   - macOS/Linux: `source .venv/bin/activate`
5. Instala las dependencias: `python -m pip install -r requirements.txt`
6. En VS Code, selecciona el intérprete de `.venv` con **Python: Select Interpreter**.
7. Inicia el sitio: `python app.py`. Abre `http://127.0.0.1:5000`.

El modo de depuración está desactivado por defecto. Para activarlo localmente en PowerShell antes de iniciar Flask:

```powershell
$env:FLASK_DEBUG = "1"
python app.py
```

## Personalizar textos, precios, imágenes y contacto

- Edita textos y precios directamente en `templates/index.html`.
- Cambia las URLs de las imágenes de la sección hero y la galería por tus fotografías.
- Actualiza el Instagram en el enlace del pie de página.
- Añade tu teléfono de WhatsApp y email de contacto en `app.py`, en los valores por defecto `WHATSAPP_NUMBER` y `CONTACT_EMAIL`. El teléfono se escribe con prefijo internacional y solo dígitos, por ejemplo `34600111222`.
- También puedes definirlos como variables de entorno `WHATSAPP_NUMBER` y `CONTACT_EMAIL` en el servicio de alojamiento, sin modificar el código.
- Las reservas se guardan en `instance/reservas.csv`. Puedes elegir otra ruta con la variable de entorno `RESERVATIONS_FILE`.

## Publicar gratis en Render

1. Sube el proyecto a un repositorio GitHub.
2. En Render, crea un **New > Web Service** y conecta ese repositorio.
3. Selecciona el plan gratuito, si está disponible para tu cuenta/región.
4. Configura **Build Command** como `pip install -r requirements.txt`.
5. Configura **Start Command** como `gunicorn app:app`.
6. Añade las variables `WHATSAPP_NUMBER` y `CONTACT_EMAIL` desde **Environment**.
7. Pulsa **Create Web Service**. Render mostrará una URL pública al terminar el despliegue.

**Importante sobre el CSV:** el almacenamiento local de los servicios gratuitos puede ser efímero. El CSV puede perderse al reiniciar o volver a desplegar. Descárgalo con regularidad o configura un disco persistente (normalmente de pago) antes de usar el sitio para reservas reales.

## Publicar en PythonAnywhere

1. Crea una cuenta y sube el proyecto a PythonAnywhere, por ejemplo mediante la pestaña **Files** o clonando tu repositorio desde una consola Bash.
2. En **Web**, crea una aplicación Flask seleccionando una versión de Python disponible.
3. En una consola Bash, crea un entorno virtual e instala dependencias:

   ```bash
   cd ~/mi-python
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

4. En la configuración de la aplicación web, indica la ruta del entorno virtual (`/home/USUARIO/mi-python/.venv`) y edita el archivo WSGI para cargar tu aplicación:

   ```python
   import sys
   project_home = "/home/USUARIO/mi-python"
   if project_home not in sys.path:
       sys.path.insert(0, project_home)

   from app import app as application
   ```

   Sustituye `USUARIO` por tu nombre de usuario real.
5. Pulsa **Reload** en la pestaña **Web**. La web gratuita usa un subdominio de PythonAnywhere.
6. Añade las variables de contacto en el entorno de la aplicación si tu plan lo permite; si no, cambia los valores por defecto en `app.py`.

El CSV queda en `instance/reservas.csv`; revisa el espacio disponible y descarga una copia de seguridad periódicamente.

## Envío de reservas

El formulario valida y guarda cada solicitud en CSV sin una base de datos. Para recibir aviso por email, conecta el endpoint `/reservar` a un proveedor SMTP o de email transaccional y guarda sus credenciales como variables de entorno; nunca las publiques en el repositorio. Las respuestas guardadas contienen datos personales: limita su acceso y elimínalas cuando ya no sean necesarias.
