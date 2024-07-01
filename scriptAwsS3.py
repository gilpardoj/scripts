import boto3
import os


def create_bucket(bucket_name, region='us-east-2'):
    try:
        s3_client = boto3.client('s3', region_name=region)
        response = s3_client.list_buckets()
        buckets = [bucket['Name'] for bucket in response['Buckets']]

        if bucket_name not in buckets:
            s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={
                'LocationConstraint': region
            })
            print(f"Bucket '{bucket_name}' creado exitosamente en la región '{region}'.")
        else:
            print(f"El bucket '{bucket_name}' ya existe.")
    except Exception as e:
        print(f"No se pudo crear el bucket '{bucket_name}': {e}")

def list_buckets(region='us-east-2'):
    try:
        s3_client = boto3.client('s3', region_name=region)
        response = s3_client.list_buckets()

        print("Lista de Buckets en AWS S3:")
        for bucket in response['Buckets']:
            print(f"- {bucket['Name']}")
    except Exception as e:
        print(f"No se pudo listar los buckets: {e}")

def upload_file(bucket_name, file_path):
    try:
        s3_client = boto3.client('s3')
        file_name = os.path.basename(file_path)
        s3_client.upload_file(file_path, bucket_name, file_name)
        print(f"Archivo '{file_name}' subido exitosamente al bucket '{bucket_name}'.")
    except Exception as e:
        print(f"No se pudo subir el archivo '{file_name}' al bucket '{bucket_name}': {e}")

def list_bucket_contents(bucket_name):
    try:
        s3_client = boto3.client('s3')
        response = s3_client.list_objects_v2(Bucket=bucket_name)

        print(f"Contenido del bucket '{bucket_name}':")
        for obj in response.get('Contents', []):
            print(f"- {obj['Key']}")
    except Exception as e:
        print(f"No se pudo listar el contenido del bucket '{bucket_name}': {e}")

def download_file(bucket_name, file_key, download_path):
    try:
        s3_client = boto3.client('s3')
        s3_client.download_file(bucket_name, file_key, download_path)
        print(f"Archivo '{file_key}' descargado exitosamente a '{download_path}' desde el bucket '{bucket_name}'.")
    except Exception as e:
        print(f"No se pudo descargar el archivo '{file_key}' del bucket '{bucket_name}': {e}")

def delete_bucket(bucket_name):
    try:
        s3_client = boto3.client('s3')
        response = s3_client.list_objects_v2(Bucket=bucket_name)

        if 'Contents' in response:
            for obj in response['Contents']:
                s3_client.delete_object(Bucket=bucket_name, Key=obj['Key'])

        s3_client.delete_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' eliminado exitosamente junto con su contenido.")
    except Exception as e:
        print(f"No se pudo eliminar el bucket '{bucket_name}': {e}")

if __name__ == "__main__":
    bucket_name1 = "probandobucket-jose1"
    bucket_name2 = "probandobucket-jose2"
    file_path = "C:\\pepitoperez\\contenido.txt"
    download_path = "C:\\descargas\\contenido.txt"


    create_bucket(bucket_name1)
    create_bucket(bucket_name2)
    list_buckets()
    upload_file(bucket_name1, file_path)
    list_bucket_contents(bucket_name1)
    download_file(bucket_name1, 'contenido.txt', download_path)
    delete_bucket(bucket_name1)
    delete_bucket(bucket_name2)
    



