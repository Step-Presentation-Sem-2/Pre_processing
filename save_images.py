import boto3
from botocore.exceptions import NoCredentialsError
import io
import os



def upload_to_S3(image, output_folder):
    # Upload the file
    session = boto3.Session(
        aws_access_key_id = os.getenv("aws_access_key_id"),
        aws_secret_access_key = os.getenv("aws_secret_access_key"),
    )
    s3 = session.client('s3')

    # creates an in memory file for the image 
    in_mem_file = io.BytesIO()

    # Save the image to the in-memory file
    image.save(in_mem_file, format='JPEG')
    in_mem_file.seek(0)
    
    # upload the image to S3 bucket
    s3.upload_fileobj(in_mem_file, output_folder, image)