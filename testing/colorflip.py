import os
from PIL import Image, ImageOps

def invert_image_colors(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            with Image.open(file_path) as img:
                inverted_image = ImageOps.invert(img)
                name, ext = os.path.splitext(filename)
                new_file_path = os.path.join(folder_path, f"{name}_i{ext}")
                inverted_image.save(new_file_path)
                print(f"Inverted colors for {filename} and saved to {new_file_path}")
        except Exception as e:
            print(f"Skipping {filename}: {e}")

if __name__ == "__main__":
    folder_path = input("Enter the folder path containing images: ")
    invert_image_colors(folder_path)
