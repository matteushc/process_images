import cv2
import numpy as np
import os


def detect_and_draw_contours(image_path, output_folder, output_filename):
    # 1. Read the image
    img = cv2.imread(image_path)
    #img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        print(f"Error: Could not read image at {image_path}")
        return

    # Create a copy of the original image to draw contours on
    img_with_contours = img.copy()

    # 2. Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 3. Apply binary thresholding or Canny edge detection
    # Thresholding works well for images with clear contrast between objects and background
    # The first value is the threshold, the second is the max value (white)
    # The result is a binary image where objects are white and background is black
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    
    # Optional: Apply Canny edge detection instead of thresholding
    # edges = cv2.Canny(gray, 100, 200)

    # 4. Find the contours
    # cv2.findContours returns the contours and the hierarchy
    # cv2.RETR_EXTERNAL retrieves only the extreme outer contours
    # cv2.CHAIN_APPROX_SIMPLE compresses horizontal, vertical, and diagonal segments into their endpoints
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    print(f"Number of contours found: {len(contours)}")

    # 5. Draw the contours on the original image copy
    # The arguments are: image, contours list, contour index (-1 for all), color (BGR), thickness
    cv2.drawContours(img_with_contours, contours, -1, (0, 255, 0), 2) # Green color, thickness 2
    
    for i, contour in enumerate(contours):
        # Filter out small areas that might be noise
        if cv2.contourArea(contour) > 100: # Adjust min area as needed
            # Get the bounding rectangle coordinates
            x, y, w, h = cv2.boundingRect(contour)

            # Draw a bounding box on the contour image (optional, for visualization)
            cv2.rectangle(img_with_contours, (x, y), (x + w, y + h), (255, 0, 0), 2) # Blue rectangle

            # Extract the sub-image (crop from the original)
            extracted_image = img[y:y+h, x:x+w]
            if w > 50 and h > 50: # Filter out very small contours
                print(f"Extracted contour {i+1}: x={x}, y={y}, w={w}, h={h}")

                # Save the extracted image
                output_path = os.path.join(output_folder, f"{output_filename}_{i+1}.png")
                cv2.imwrite(output_path, extracted_image)
                print(f"Saved: {output_path}")


directory_path = "./images/removed/"
files_only = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]

output_path = "./images/produtos/"

for file_path in files_only:
    if file_path.endswith(('.jpg', '.jpeg', '.png')):
        file_output_name = os.path.basename(file_path).split('.')[0] + "_extracted"
        detect_and_draw_contours(file_path, output_path, file_output_name)