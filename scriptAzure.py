import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError

# Connection string for Azure Blob Storage service
connection_string = 'your_azure_storage_credentials'
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

def create_container(container_name):
    try:
        container_client = blob_service_client.create_container(container_name)
        print(f'Container {container_name} created successfully.')
    except ResourceExistsError:
        print(f'The container {container_name} already exists.')

def list_containers():
    containers = blob_service_client.list_containers()
    containers_list = list(containers)  # Convert iterator to list to count its elements

    if containers_list:
        print("Containers inside:")
        for container in containers_list:
            print(container['name'])
    else:
        print("No containers found.")

def upload_blob(container_name, file_path):
    try:
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=os.path.basename(file_path))
        with open(file_path, 'rb') as data:
            blob_client.upload_blob(data)
        print(f'File {file_path} uploaded to {container_name}.')
    except ResourceNotFoundError:
        print(f'Container {container_name} not found.')

def list_blobs(container_name):
    try:
        container_client = blob_service_client.get_container_client(container_name)
        blobs = container_client.list_blobs()
        for blob in blobs:
            print(blob.name)
    except ResourceNotFoundError:
        print(f'Container {container_name} not found.')

def download_blob(container_name, blob_name, download_path):
    try:
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        with open(download_path, 'wb') as download_file:
            download_file.write(blob_client.download_blob().readall())
        print(f'Blob {blob_name} downloaded to {download_path}.')
    except ResourceNotFoundError:
        print(f'Blob {blob_name} or container {container_name} not found.')

def delete_container(container_name):
    try:
        blob_service_client.delete_container(container_name)
        print(f'Container {container_name} deleted successfully.')
    except ResourceNotFoundError:
        print(f'Container {container_name} not found.')

# Example usage
if __name__ == "__main__":
    create_container('containerjose1')
    create_container('containerjose2')
    list_containers()
    upload_blob('containerjose1', 'C:\\archivoAzure\\archivo1.txt')
    list_blobs('containerjose1')
    download_blob('containerjose1', 'archivo1.txt', 'C:\\descargas\\archivo1.txt')
    delete_container('containerjose1')
