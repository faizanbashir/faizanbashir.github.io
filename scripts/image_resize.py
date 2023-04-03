import os
import argparse
from PIL import Image

"""Sample Usage
$ python image_resize.py path/to/image_or_directory <reduction percentage>"""

def is_supported_image_file(file_path):
    supported_extensions = ['.jpg', '.jpeg', '.png']
    file_extension = os.path.splitext(file_path)[1].lower()
    return file_extension in supported_extensions

def reduce_image_size(input_image, output_image, reduction_percent):
    if not is_supported_image_file(input_image):
        print(f"Unsupported image format. Supported formats: jpg, jpeg, png")
        return

    original_image = Image.open(input_image)
    width, height = original_image.size

    new_width = int(width * (1 - reduction_percent / 100))
    new_height = int(height * (1 - reduction_percent / 100))

    resized_image = original_image.resize((new_width, new_height), resample=Image.LANCZOS)
    resized_image.save(output_image)

def process_image_files(input_path, reduction_percent):
    if os.path.isfile(input_path):
        output_image = os.path.splitext(input_path)[0] + "_resized" + os.path.splitext(input_path)[1]
        reduce_image_size(input_path, output_image, reduction_percent)
        print(f"Image size reduced by {reduction_percent}% and saved as {output_image}.")
    elif os.path.isdir(input_path):
        for file in os.listdir(input_path):
            file_path = os.path.join(input_path, file)
            if is_supported_image_file(file_path):
                output_image = os.path.splitext(file_path)[0] + "_resized" + os.path.splitext(file_path)[1]
                reduce_image_size(file_path, output_image, reduction_percent)
                print(f"Image size reduced by {reduction_percent}% and saved as {output_image}.")
    else:
        print("Invalid input path. Please provide a valid file or directory.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reduce image size by a specified percentage.")
    parser.add_argument("input_path", help="Input file or directory containing images")
    parser.add_argument("reduction_percent", type=int, help="Percentage to reduce image size by")
    args = parser.parse_args()

    process_image_files(args.input_path, args.reduction_percent)
