# Peluquería Olimpus

Sistema web para gestionar una peluquería con Django. Este proyecto está pensado para administrar operaciones básicas del negocio, incluyendo vista principal, estructura del proyecto y configuración segura mediante variables de entorno.

## Tecnologías

- Python
- Django
- SQLite (configuración local por defecto)
- python-dotenv

## Requisitos

- Python 3.10 o superior
- pip
- Git

## Estructura del proyecto

- `core/`: lógica principal de la aplicación
- `prjolimpus/`: configuración del proyecto Django
- `manage.py`: comando principal para ejecutar la app
- `.env`: variables sensibles locales (no se sube a Git)
- `.env.example`: plantilla de variables necesarias

## Instalación

1. Cloná el repositorio:

```bash
git clone https://github.com/santifigu/peluqueria-olimpus.git
cd peluqueria-olimpus
```

2. Creá un entorno virtual:

```bash
python -m venv venv
```

3. Activá el entorno virtual:

Windows:
```powershell
venv\Scripts\activate
```

Linux/macOS:
```bash
source venv/bin/activate
```

4. Instalá las dependencias:

```bash
pip install -r requirements.txt
```

5. Configurá el archivo de entorno:

Copia el ejemplo y completá los valores locales:

```bash
copy .env.example .env
```

Contenido esperado en `.env`:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
```

6. Ejecutá las migraciones:

```bash
python manage.py migrate
```

7. Iniciá el servidor:

```bash
python manage.py runserver
```

Abre la app en tu navegador en:

```text
http://127.0.0.1:8000/
```

## Variables de entorno

El proyecto usa variables de entorno para evitar guardar claves y configuraciones sensibles dentro del código fuente. El archivo `.env` queda local y no debe subirse a Git.

## Seguridad

- Nunca compartas el archivo `.env`.
- Usa valores distintos en producción.
- Cambiá `DEBUG=False` al desplegar.
- Configurá `ALLOWED_HOSTS` con los dominios reales.

## Estado del proyecto

Este proyecto está configurado como una base Django con entorno seguro y lista para desarrollo local.
