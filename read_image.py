import os
import cv2
import shutil
import easyocr
import numpy as np
import multiprocessing
import gc
import torch
#torch.cuda.set_per_process_memory_fraction(0.5, 0)
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:64"
#os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"


directory_path = "./images/produtos/"
output_path = "./images/produtos_filtrados/"
files_only = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]

def process_file(file_path):
    
    modified_image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
    new_width = 520
    (original_height, original_width) = modified_image.shape[:2]

    # Calculate the ratio of the new width to the old width
    ratio = new_width / float(original_width)
    # Calculate the new height
    new_height = int(original_height * ratio)
    # Define the new dimensions tuple
    dimensions = (new_width, new_height)

    # Determine interpolation method based on whether we are upscaling or downscaling
    if new_width < original_width:
        # Best for shrinking
        interpolation = cv2.INTER_AREA
    else:
        # Best for enlarging (LANCZOS4 is also a high quality option)
        interpolation = cv2.INTER_CUBIC
        
    modified_image = cv2.resize(modified_image, dimensions, interpolation=interpolation)
    #modified_image = cv2.threshold(modified_image, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    reader = easyocr.Reader(['pt'], gpu=True)  # Specify the language(s) you want to use

    text = reader.readtext(modified_image)
    is_only_number = False
    for bbox, text, score in text:
        
        if score < 0.5:
            continue
        tl, tr, br, bl = bbox
        
        # Calculate width and height
        width = np.linalg.norm(np.array(tl) - np.array(tr))
        height = np.linalg.norm(np.array(tl) - np.array(bl))
        area = width * height
        if area < 3000:
            continue
        
        only_number = ''.join(filter(str.isdigit, text))
        if only_number:
            is_only_number = True
            break
        
    if is_only_number:
        shutil.copy(file_path, output_path)
        print(f"Copied: {file_path} to {output_path}")
        
    torch.cuda.empty_cache()
    gc.collect()

with multiprocessing.Pool(10) as pool:
    pool.map(process_file, files_only)
