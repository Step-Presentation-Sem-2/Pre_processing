import argparse
import numpy as np
from PIL import Image
import os
import config as cg

def preprocessing(image_path, output_size, mean_vals=cg.mean, scale_factor=1.0/255, save_dir="processed_real_images_b1"):
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



def reading_images(directory_path, output_size, save_dir="processed_real_images_b1"):
    """
    Process all images within the specified directory.
    """
    for filename in os.listdir(directory_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(directory_path, filename)
            preprocessing(image_path, output_size, cg.mean)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Preprocess images for modelling and then save in a separate folder.")
    parser.add_argument("directory_path", type=str, help="Path to the directory containing images to be preprocessed.")
    parser.add_argument("--width", type=int, default=224, help="Output image width.")
    parser.add_argument("--height", type=int, default=224, help="Output image height.")

    args = parser.parse_args()

    # Convert command-line arguments for output size into a tuple
    output_size = (args.width, args.height)

    # process all images in that directory
    reading_images(args.directory_path, output_size)

