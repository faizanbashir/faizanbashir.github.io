import os
import sys
from PIL import Image

def change_aspect_ratio(filepath, aspect_ratio="16/9"):
  """
  Changes the aspect ratio of an image, saving the modified image.

  Args:
    filepath: The path to the image file.
    aspect_ratio: The desired aspect ratio as a string (e.g., "16/9" or "4/3"). 
    Defaults to 16/9 if not provided.
  """

  try:
    img = Image.open(filepath)

    # Parse the aspect ratio string
    width, height = map(int, aspect_ratio.split("/"))

    # Calculate new dimensions while maintaining aspect ratio
    current_width, current_height = img.size
    if current_width / current_height > width / height:
      new_width = current_height * width / height
      new_height = current_height
    else:
      new_width = current_width
      new_height = current_width * height / width

    # Resize the image
    resized_img = img.resize((int(new_width), int(new_height)))

    # Save the modified image (you can change the output format if needed)
    resized_img.save("resized_" + filepath) 

    print(f"Image aspect ratio changed and saved as resized_{filepath}")

  except FileNotFoundError:
    print(f"Error: File not found at {filepath}")
  except Exception as e:
    print(f"An error occurred: {e}")

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
        print("Usage: python image_aspect_ratio.py <input_path> <aspect_ratio>")
        sys.exit(1)

    input_path = sys.argv[1]

    try:
        aspect_ratio = sys.argv[2]
        numerator, denominator = map(int, aspect_ratio.split("/"))

        if numerator <= 0 or denominator <= 0:
            raise ValueError
        
    except (ValueError, IndexError):
        print("Error: aspect_ratio must be in the format 'number/number' (e.g., 16/9)")
        sys.exit(1)

    # Validate the input path (file or directory)
    input_type = validate_input(input_path)
    if not input_type:
        sys.exit(1)

    if input_type == "file":
        change_aspect_ratio(input_path, aspect_ratio)
    else:
        # Iterate over files in the input directory (including subdirectories) and convert them
        for root, _, files in os.walk(input_path):
            for file in files:
                input_image = os.path.join(root, file)
                change_aspect_ratio(input_path, aspect_ratio)
