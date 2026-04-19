import os
import cv2
import numpy as np
from PIL import Image


def get_dominant_color(image_path):
    
    img = Image.open(image_path)

    # Get all colors and their frequencies
    # getcolors() returns a list of (count, pixel) tuples
    colors_with_counts = img.getcolors(img.size[0] * img.size[1]) 

    most_frequent_color = None
    # Find the most frequent color (likely the background if solid)
    if colors_with_counts:
        most_frequent_color = max(colors_with_counts, key=lambda x: x[0])[1]
    
    return most_frequent_color


def remove_background_hsv(image_path, output_path, color_rgb, tolerance=80):
    # Load the image
    img = cv2.imread(image_path)
   
    target_color_np = np.array(color_rgb)
    
    # Define tolerance for color matching
    lower_bound = np.array([max(0, target_color_np[2] - tolerance), max(0, target_color_np[1] - tolerance), max(0, target_color_np[0] - tolerance)])
    upper_bound = np.array([min(255, target_color_np[2] + tolerance), min(255, target_color_np[1] + tolerance), min(255, target_color_np[0] + tolerance)])
    
    mask = cv2.inRange(img, lower_bound, upper_bound)
    
    # Invert the mask to select everything that is *not* green
    mask_inv = cv2.bitwise_not(mask)
    
    # Use the inverted mask to keep the foreground subject
    result = cv2.bitwise_and(img, img, mask=mask_inv)
    
    # Convert result to BGRA to add a real alpha channel
    result = cv2.cvtColor(result, cv2.COLOR_BGR2BGRA)
    
    result[mask_inv == 0] = [0, 0, 0, 0] 
    
    cv2.imwrite(output_path, result)
    print(f"Background removed. Image saved at {output_path}")

directory_path = "./images/" # Replace with your path
files_only = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]

file_path = directory_path + "image_3_xref34.jpeg"


for file_path in files_only:
    if file_path.endswith(('.jpg', '.jpeg', '.png')):
        output_path = "./images/removed/"
        file_output_name = os.path.basename(file_path).split('.')[0] + "_hsv_removed.jpeg"
        output_path = os.path.join(output_path, file_output_name)
        
        dominant_color = get_dominant_color(file_path)
        # dominant_color = [10, 133, 200]
        remove_background_hsv(file_path, output_path, dominant_color)
