from preprocessing import preprocess_input
import os
from PIL import Image
import numpy as np


def get_image(input_directory_path,output_directory_path):
    """
    Process all images within the specified directory.
    Reads each file or image from the input directory path and then creates the image path
    image path is the path of the directory + that of the image
    passes the image path with the output size for the resizing and the directory to save the preprocessed images
    """
    for filename in os.listdir(input_directory_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(input_directory_path, filename)
            image = Image.open(image_path)
            # image = image.resize(output_size)     # Load and resize the image
            image_np = np.array(image, dtype=np.float32)
            processed_array = preprocess_input(image_np, data_format= None)

            if not os.path.exists(output_directory_path): os.makedirs(output_directory_path)
            # Save the processed image
            image_name = os.path.basename(image_path)
            save_path = os.path.join(output_directory_path, image_name)
            Image.fromarray(np.clip(processed_array, 0, 255).astype('uint8')).save(save_path)

            print(f"Processed image saved to: {save_path}")


if __name__ == "__main__":
    input_folders = ['scraped_images/scraped_images_b1','scraped_images/ai_generated_images_b1']
    output_folders = ['preprocessed_images/processed_real_images_b1','preprocessed_images/processed_ai_images_b1']
    for input_folder, output_folder in zip(input_folders,output_folders):
        get_image(input_folder,output_folder)