from preprocessing import preprocess_input
import os
from PIL import Image
import numpy as np

import boto3
from read_images import download_from_S3
from save_images import upload_to_S3
import shutil


def processing_images(input_directory_path, output_folder):
    """
    Process all images within the specified local temporary folder.
    Reads each file or image from the input directory path and then create the image path
    image path is the path of the directory + that of the image
    passes the image path with the output size for the resizing and the directory to save the preprocessed images
    """
    for filename in os.listdir(input_directory_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(input_directory_path, filename)
            image = Image.open(image_path)
            image_np = np.array(image, dtype=np.float32)
            processed_array = preprocess_input(image_np, data_format= None)


            # Save the processed image to S3 bucket
            image = Image.fromarray(np.clip(processed_array, 0, 255).astype('uint8'))
            upload_to_S3(image, output_folder)





if __name__ == "_main_":
    temp_folders = ['./scraped_images_b1','./ai_generated_images_b1']
    input_folders = [os.getenv('real_bucket_name'),os.getenv('generated_bucket_name')]
    output_folders = [os.getenv('processed_real_bucket_name'),os.getenv('processed_generated_bucket_name')]

    for input_folder, temp_folder, output_folder in zip(input_folders, temp_folders, output_folders):
        # Creates a local directory for storing images temporarily
        try:
            os.makedirs(temp_folder,exist_ok=True)
        except Exception as e:
            print(f'Failed to create directory: {e}')

        # Download images from S3 bucket
        # this function downloads images into local
        download_from_S3(input_folder,temp_folder)

        # Read each image in the local folder
        processing_images(temp_folder, output_folder)

        # Deletes the local directory of images
        shutil.rmtree(temp_folder)