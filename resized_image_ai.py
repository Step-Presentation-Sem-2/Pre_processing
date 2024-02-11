import os
from PIL import Image

ai_images_path = r"C:\\Users\\acer\Desktop\sem2 -Step\\Pre_processing\\ai_generated_images_b1"
resized_images_path = r"C:\\Users\\acer\Desktop\sem2 -Step\\Pre_processing\\Resized_images"
new_image_size = (224, 224)

os.makedirs(resized_images_path, exist_ok=True)

for file_name in os.listdir(ai_images_path):
    image_path = os.path.join(ai_images_path, file_name)
    org_image = Image.open(image_path)
    
    
    resized_image = org_image.resize(new_image_size)
    
    output_path = os.path.join(resized_images_path, file_name)
    
    
    resized_image.save(output_path)

    
    org_image.close()
    resized_image.close()

print("Resizing Complete")


