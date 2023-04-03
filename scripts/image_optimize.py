import os
import argparse
from PIL import Image

"""Sample Usage
$ python image_optimize.py path/to/image_or_directory <reduction percentage>"""

def is_supported_image_file(file_path):
    supported_extensions = ['.jpg', '.jpeg', '.png']
    file_extension = os.path.splitext(file_path)[1].lower()
    return file_extension in supported_extensions

def reduce_image_size(input_image, output_image, quality):
    if not is_supported_image_file(input_image):
        print(f"Unsupported image format. Supported formats: jpg, jpeg, png")
        return

    original_image = Image.open(input_image)
    file_extension = os.path.splitext(input_image)[1].lower()

    if file_extension in ['.jpg', '.jpeg']:
        original_image.save(output_image, format="JPEG", quality=quality, optimize=True, progressive=True)
    elif file_extension == '.png':
        original_image.save(output_image, format="PNG", optimize=True, compress_level=9-quality//10)

def process_image_files(input_path, quality):
    if os.path.isfile(input_path):
        output_image = os.path.splitext(input_path)[0] + "_compressed" + os.path.splitext(input_path)[1]
        reduce_image_size(input_path, output_image, quality)
        print(f"Image compressed and saved as {output_image}.")
    elif os.path.isdir(input_path):
        for file in os.listdir(input_path):
            file_path = os.path.join(input_path, file)
            if is_supported_image_file(file_path):
                output_image = os.path.splitext(file_path)[0] + "_compressed" + os.path.splitext(file_path)[1]
                reduce_image_size(file_path, output_image, quality)
                print(f"Image compressed and saved as {output_image}.")
    else:
        print("Invalid input path. Please provide a valid file or directory.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reduce image size while maintaining resolution.")
    parser.add_argument("input_path", help="Input file or directory containing images")
    parser.add_argument("quality", type=int, help="Quality level (1-100) for JPEG or (10-90) for PNG compression", choices=range(1, 101))
    args = parser.parse_args()

    process_image_files(args.input_path, args.quality)