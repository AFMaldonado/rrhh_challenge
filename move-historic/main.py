from google.cloud import storage
import requests
import tempfile
from api.secret_manager import SecretManagerGCP

# Crear una instancia del cliente de Cloud Storage
cliente_storage = storage.Client()
project_id = "proyect-pma"

# Initialize SecretManagerGCP with project_id
secret_manager = SecretManagerGCP(project_id)
key = secret_manager.get_secret("api-key-rrhh")

def enviar_archivo_csv_a_api(url, nombre_bucket, nombre_archivo):
    # Obtener el bucket
    bucket = cliente_storage.bucket(nombre_bucket)

    # Descargar el archivo CSV desde Cloud Storage a un archivo temporal
    with tempfile.NamedTemporaryFile() as temp_file:
        blob = bucket.blob(nombre_archivo)
        blob.download_to_filename(temp_file.name)

        # Crear un diccionario con los parámetros de la solicitud
        parametros = {'key': key}

        # Abrir el archivo temporal en modo lectura binaria
        with open(temp_file.name, 'rb') as archivo:
            # Crear un diccionario con los archivos que deseas enviar
            archivos = {'file': archivo}

            # Enviar la solicitud POST con los parámetros y el archivo
            respuesta = requests.post(url, files=archivos, params=parametros)

    # Verificar la respuesta de la API
    if respuesta.status_code == 200:
        print(f'Archivo CSV "{nombre_archivo}" enviado exitosamente a la API.')
    else:
        print(f'Error al enviar el archivo CSV "{nombre_archivo}" a la API:', respuesta.text)

def move_historic():
    # Definir la información del bucket y el nombre de los archivos CSV en Cloud Storage
    archivos_para_enviar = [
        {'nombre_bucket': 'historic-data-rrhh', 'nombre_archivo': 'departments.csv', 'url_api': 'https://gat-v1-4o7dri9w.uc.gateway.dev/upload_departments'},
        {'nombre_bucket': 'historic-data-rrhh', 'nombre_archivo': 'jobs.csv', 'url_api': 'https://gat-v1-4o7dri9w.uc.gateway.dev/upload_jobs'},
        {'nombre_bucket': 'historic-data-rrhh', 'nombre_archivo': 'hired_employees.csv', 'url_api': 'https://gat-v1-4o7dri9w.uc.gateway.dev/upload_hired_employees'},
    ]

    # Iterar sobre la lista de archivos y enviar cada uno a la API
    for archivo_info in archivos_para_enviar:
        enviar_archivo_csv_a_api(archivo_info['url_api'], archivo_info['nombre_bucket'], archivo_info['nombre_archivo'])


move_historic()

