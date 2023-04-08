import os
import sys
from PIL import Image

def convert_to_webp(input_file, quality):
    """
    Convert an image file (PNG, JPEG, JPG) to WebP format and save it in the same directory
    with the same name.

    :param input_file: Path to the input image file
    :type input_file: str
    :param quality: Quality setting for the WebP conversion, integer between 1 and 100
    :type quality: int
    """
    file_name, file_extension = os.path.splitext(input_file)
    file_extension = file_extension.lower()

    if file_extension not in ['.png', '.jpeg', '.jpg']:
        print(f"Skipping {input_file}: Unsupported file type")
        return

    output_file = f"{file_name}.webp"
    try:
        img = Image.open(input_file).convert('RGBA')

        # Set the lossless parameter based on the quality
        lossless = False
        if quality == 100:
            lossless = True

        img.save(output_file, 'webp', quality=quality, lossless=lossless)
        print(f"Converted {input_file} to {output_file}")
    except Exception as e:
        print(f"Error converting {input_file}: {e}")


def validate_input(input_path):
    """
    Validate if the input path is an existing file or directory.

    :param input_path: Path to the input file or directory
    :type input_path: str
    :return: "file" if it's a file, "directory" if it's a directory, or False if invalid
    :rtype: str or bool
    """
    if os.path.isfile(input_path):
        return "file"
    elif os.path.isdir(input_path):
        return "directory"
    else:
        print(f"Error: Invalid input path: {input_path}")
        return False


if __name__ == "__main__":
    # Check if the correct number of command-line arguments are provided
    if len(sys.argv) != 3:
        print("Usage: python convert_to_webp.py <input_path> <quality>")
        sys.exit(1)

    input_path = sys.argv[1]
    try:
        quality = int(sys.argv[2])
        if quality < 1 or quality > 100:
            raise ValueError
    except ValueError:
        print("Error: Quality must be an integer between 1 and 100")
        sys.exit(1)

    # Validate the input path (file or directory)
    input_type = validate_input(input_path)
    if not input_type:
        sys.exit(1)

    if input_type == "file":
        convert_to_webp(input_path, quality)
    else:
        # Iterate over files in the input directory (including subdirectories) and convert them
        for root, _, files in os.walk(input_path):
            for file in files:
                input_file = os.path.join(root, file)
                convert_to_webp(input_file, quality)
