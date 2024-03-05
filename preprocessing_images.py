import argparse
import numpy as np
from PIL import Image
import os
import config as cg
import boto3
from dotenv import load_dotenv
import shutil
load_dotenv()




def preprocessing(image_path, output_size, save_dir, mean_vals=cg.mean, scale_factor=1.0/255):
    """
    Resize the images, 
    perform mean subtraction, 
    scale the pixel values of an image, 
    and save the processed image to a specified directory.

    Args:
        image_path (str): Path to the image file in a certain directory.
        output_size (tuple): The target size (width, height) after resizing. Default (224,224)
        mean_vals (tuple, optional): Mean values for each channel to subtract (R, G, B).
        scale_factor (float, optional): Scale factor to apply after mean subtraction.
        save_dir (str, optional): Directory where the processed images will be saved.
    """
    # Load and resize the image
    image = Image.open(image_path)
    image = image.resize(output_size)
    image_np = np.array(image, dtype=np.float32)

    # Check if image is grayscale and convert it to RGB by duplicating the channels
    if len(image_np.shape) == 2 or image_np.shape[2] == 1:
        image_np = np.stack((image_np,) * 3, axis=-1)

    # Perform mean subtraction
    for i in range(3):  # Assuming the image is in RGB format
        image_np[:, :, i] -= mean_vals[i]

    # Scale the pixel values
    image_np *= scale_factor

    # Convert back to PIL image for saving
    image_processed = Image.fromarray(np.uint8(image_np * 255))  # Rescale back to [0,255]

    # Ensure the save directory exists
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Save the processed image
    image_name = os.path.basename(image_path)
    save_path = os.path.join(save_dir, image_name)
    image_processed.save(save_path)

    print(f"Processed image saved to: {save_path}")






def reading_images(input_directory_path,output_size,output_directory_path):
    """
    Process all images within the specified directory.
    Reads each file or image from the input directory path and then creates the image path
    image path is the path of the directory + that of the image
    passes the image path with the output size for the resizing and the directory to save the preprocessed images
    """
    for filename in os.listdir(input_directory_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(input_directory_path, filename)
            preprocessing(image_path, output_size, save_dir = output_directory_path)





# Defining the clean_file_name function to handle path and redundant extension issues
def clean_file_name(file_name):
    """
    Handle cases of mistypes]d file names
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





def download_images_from_s3(bucket_name, local_folder):
    """
    Access the S3 bucket to pull images
    Save these images in local folder
        
    Args:
        bucket_name (str): S3 bucket where scraped images are located
        local_folder (str): name of the folder to save the images after pulling from S3    
    Returns:
        Downloads images from S3 bucket to the local directory created
    """
    
    session = boto3.Session(
        aws_access_key_id = os.getenv("aws_access_key_id"),
        aws_secret_access_key = os.getenv("aws_secret_access_key"),
    )
    s3 = session.client('s3')

    objects = s3.list_objects_v2(Bucket=bucket_name).get('Contents', [])  # get a list of all objects in the bucket
    if not objects:
        print("No objects found in the bucket.")
        return

    for obj in objects:
        file_name = obj['Key']             # filename for every object in that bucket
        clean_name = clean_file_name(file_name)          # returns cleaned file name uniform for all objects in bucket
        local_file_path = os.path.join(local_folder, clean_name)  # joins this cleaned file name with path to save images to local
        os.makedirs(os.path.dirname(local_file_path), exist_ok=True)        # Ensure the directory for the file exists
        try:
            if clean_name.endswith('.jpg') or clean_name.endswith('.png') or clean_name.endswith('.jpeg'):
                s3.download_file(bucket_name, file_name, local_file_path)     # download the file from bucket to local
                print(f"{file_name} downloaded to {local_file_path}")
        except Exception as e:
            print(f"Failed to download {file_name}: {e}")





if __name__ == "__main__":
    # calling arguments necessary for preprocessing images
    parser = argparse.ArgumentParser(description="Preprocess images for modelling and then save in a separate folder.")
    parser.add_argument("--width", type=int, default=224, help="Output image width.")
    parser.add_argument("--height", type=int, default=224, help="Output image height.")
    parser.add_argument("output_directory_path_real", type=str, help="Path to save REAL preprocessed images.")
    parser.add_argument("output_directory_path_ai", type=str, help="Path to save AI GENERATED preprocessed images.")

    args = parser.parse_args()

    # Convert command-line arguments for output size into a tuple
    output_size = (args.width, args.height)
    
    local_folders = ['./scraped_images_b1','./ai_generated_images_b1']
    buckets = [os.getenv("real_bucket_name"), os.getenv("generated_bucket_name") ]        # bucket of scraped images
    output_directory_paths = [args.output_directory_path_real, args.output_directory_path_ai]

    for bucket_name, local_folder, output_directory_path in zip(buckets, local_folders, output_directory_paths):
        # Creates a local directory for images
        try:
            os.makedirs(local_folder, exist_ok=True)
        except Exception as e:
            print(f"Failed to create directory: {e}")

        # Download Images from S3 Bucket
        download_images_from_s3(bucket_name, local_folder)

        # Preprocessing images
        reading_images(local_folder,output_size,output_directory_path) 

        # Deletes the local directory of images
        shutil.rmtree(local_folder)


