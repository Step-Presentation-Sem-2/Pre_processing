import os
from PIL import Image
import numpy as np
import argparse
import boto3




# Defining the clean_file_name function to handle path and redundant extension issues
def clean_file_name(file_name):
    """
    Handle cases of mistyped file names
    Remove multiple file extensions if present
    Args:
        file_name (str) : file name as stored in S3
    """
    # Normalize the file path to ensure correct path separators
    file_name = os.path.normpath(file_name)          # normalizing the file path of the image as it is present in the S3 bucket
    base_file_name = os.path.basename(file_name)     # get the image name 
    while base_file_name.count('.jpg') > 1: base_file_name = base_file_name.rsplit('.jpg', 1)[0]    # getting file name till 1st split
    while base_file_name.count('.png') > 1: base_file_name = base_file_name.rsplit('.png', 1)[0]    # getting file name till 1st split
    return base_file_name            # returns the cleaned file name for pulling image from S3 to local folder


def download_from_S3(input_folder, temp_folder):
    """
    Access the S3 bucket to pull images
    Save these images in local folder
        
    Args:
        input_folder (str): S3 bucket where scraped images are located
        local_folder (str): name of the folder to save the images after pulling from S3    
    Returns:
        Downloads images from S3 bucket to the local directory temporarily created
    """
    session = boto3.Session(
        aws_access_key_id = os.getenv("aws_access_key_id"),
        aws_secret_access_key = os.getenv("aws_secret_access_key"),
    )
    s3 = session.client('s3')
    objects = s3.list_objects_v2(Bucket=input_folder).get('Contents', [])  # get a list of all objects in the bucket
    if not objects:
        print("No objects found in the bucket.")
        return
    
    # accessing each object in the bucket folder
    for obj in objects:
        file_name = obj['Key']             # filename for every object in that bucket
        clean_name = clean_file_name(file_name)          # returns cleaned file name uniform for all objects in bucket
        local_file_path = os.path.join(temp_folder, clean_name)  # joins this cleaned file name with path to save images to local
        os.makedirs(os.path.dirname(local_file_path), exist_ok=True)        # Ensure the directory for the file exists
        try:
            if clean_name.endswith('.jpg') or clean_name.endswith('.png') or clean_name.endswith('.jpeg'):
                s3.download_file(input_folder, file_name, local_file_path)     # download the file from bucket to local
                print(f"{file_name} downloaded to {local_file_path}")
        except Exception as e:
            print(f"Failed to download {file_name}: {e}")