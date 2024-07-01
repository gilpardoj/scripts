import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError

# Cadena de conexión para el servicio de Blob Storage de Azure
connection_string = 'credenciales_almacenamientoAzure'
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

def crear_contenedor(nombre_contenedor):
    try:
        container_client = blob_service_client.create_container(nombre_contenedor)
        print(f'Contenedor {nombre_contenedor} creado exitosamente.')
    except ResourceExistsError:
        print(f'El contenedor {nombre_contenedor} ya existe.')

def listar_contenedores():
    containers = blob_service_client.list_containers()
    containers_list = list(containers)  # Convierte el iterador en una lista para poder contar sus elementos

    if containers_list:
        print("Contenedores dentro:")
        for container in containers_list:
            print(container['name'])
    else:
        print("No hay contenedores.")

def cargar_blob(nombre_contenedor, ruta_archivo):
    try:
        blob_client = blob_service_client.get_blob_client(container=nombre_contenedor, blob=os.path.basename(ruta_archivo))
        with open(ruta_archivo, 'rb') as data:
            blob_client.upload_blob(data)
        print(f'Archivo {ruta_archivo} cargado en {nombre_contenedor}.')
    except ResourceNotFoundError:
        print(f'Contenedor {nombre_contenedor} no encontrado.')

def listar_blobs(nombre_contenedor):
    try:
        container_client = blob_service_client.get_container_client(nombre_contenedor)
        blobs = container_client.list_blobs()
        for blob in blobs:
            print(blob.name)
    except ResourceNotFoundError:
        print(f'Contenedor {nombre_contenedor} no encontrado.')

def descargar_blob(nombre_contenedor, nombre_blob, ruta_descarga):
    try:
        blob_client = blob_service_client.get_blob_client(container=nombre_contenedor, blob=nombre_blob)
        with open(ruta_descarga, 'wb') as download_file:
            download_file.write(blob_client.download_blob().readall())
        print(f'Blob {nombre_blob} descargado en {ruta_descarga}.')
    except ResourceNotFoundError:
        print(f'Blob {nombre_blob} o contenedor {nombre_contenedor} no encontrado.')

def eliminar_contenedor(nombre_contenedor):
    try:
        blob_service_client.delete_container(nombre_contenedor)
        print(f'Contenedor {nombre_contenedor} eliminado exitosamente.')
    except ResourceNotFoundError:
        print(f'Contenedor {nombre_contenedor} no encontrado.')

# Uso del ejemplo
if __name__ == "__main__":
    crear_contenedor('contenedorjose3')
    crear_contenedor('contenedorjose4')
    listar_contenedores()
    cargar_blob('contenedorjose3', 'C:\\archivoAzure\\archivo1.txt')
    listar_blobs('contenedorjose3')
    descargar_blob('contenedorjose3', 'archivo1.txt', 'C:\\descargas\\archivo1.txt')
    eliminar_contenedor('contenedorjose2')
