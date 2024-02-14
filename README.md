# Panorama del código

## Dockerfile

El Dockerfile describe la configuración para construir una imagen Docker. Aquí hay una descripción de lo que hace cada parte:

1. **FROM python:3.9-slim**: Utiliza la imagen oficial de Python desde Docker Hub como base.
   
2. **ENV PYTHONDONTWRITEBYTECODE 1** y **ENV PYTHONUNBUFFERED 1**: Establece variables de entorno para el entorno Python dentro del contenedor.
   
3. **WORKDIR /app**: Define el directorio de trabajo dentro del contenedor como '/app'.
   
4. **COPY requirements.txt .**: Copia el archivo `requirements.txt` del directorio local al directorio de trabajo en el contenedor.
   
5. **RUN pip install --no-cache-dir -r requirements.txt**: Instala las dependencias listadas en `requirements.txt` en el entorno del contenedor.
   
6. **COPY . .**: Copia todo el contenido del directorio local al directorio de trabajo en el contenedor.
   
7. **CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]**: Especifica el comando predeterminado a ejecutar cuando se inicia el contenedor. En este caso, ejecuta Uvicorn para servir una aplicación FastAPI en el puerto 8080.

## Código Python

El código define una aplicación FastAPI que proporciona endpoints para cargar datos desde archivos CSV a una base de datos MySQL. Aquí hay un resumen de lo que hace:

1. **Conexión a la base de datos MySQL**: Se conecta a una base de datos MySQL utilizando las credenciales almacenadas en Google Cloud Secrets.
   
2. **Función `upload_csv_and_insert`**: Esta función maneja la carga de archivos CSV y la inserción de datos en la base de datos MySQL. Divide la carga del archivo en lotes y los inserta en la base de datos.

3. **Función `insert_batch_to_database`**: Inserta un lote de datos en la base de datos utilizando SQLAlchemy y Pandas DataFrame.
   
4. **Endpoints de carga de archivos**: Define tres endpoints de carga (`/upload_departments`, `/upload_jobs`, `/upload_hired_employees`) que aceptan archivos CSV y los insertan en las tablas correspondientes en la base de datos.

En resumen, el código Dockerfile se encarga de crear un entorno de contenedor y el código Python proporciona una API para cargar datos desde archivos CSV a una base de datos MySQL utilizando FastAPI.
