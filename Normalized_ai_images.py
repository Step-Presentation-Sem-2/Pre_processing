#Normalization of images(AI generated)
import os
from PIL import Image
import numpy as np

resized_ai_images=r"C:\Users\\acer\Desktop\sem2 -Step\Pre_processing\Resized_images"
normalized_ai_images=r"C:\Users\\acer\Desktop\sem2 -Step\Pre_processing\\normalized_images_ai"
os.makedirs(normalized_ai_images, exist_ok=True)
for image in os.listdir(resized_ai_images):
    image_path = os.path.join(resized_ai_images,image)
    resized_image = Image.open(image_path)
    img_array = np.array(resized_image)
    norm_image=img_array/255.0

    output_path = os.path.join(normalized_ai_images, image)
    Image.fromarray((norm_image * 255).astype('uint8')).save(output_path)

    resized_image.close()
