# imports for functions in utils
from PIL import Image
import os
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

# Functions used to process images


def process_image(profile_img):
    """process profile image"""
    # Get the uploaded image from the form
    profile_image = profile_img
    # Open the uploaded image using Pillow
    image = Image.open(profile_image)
    # Resize the image to max height/width of 125px
    max_size = (125, 125)
    image.thumbnail(max_size, Image.ANTIALIAS)
    # Remove the file extension from the image name
    # os.path.splitext splits a filename into two parts: base name and extension
    # it returns a tuple (filename, extension)
    # We unpack this tuple into 2 variables (image_name = filename; _ = extension)
    image_name, _ = os.path.splitext(profile_img.name)

    # Create a BytesIO buffer to temporarily store image
    image_buffer = BytesIO()
    image.save(image_buffer, format="JPEG")
    # Create an InMemoryUploadedFile from the buffer
    image_file = InMemoryUploadedFile(
        image_buffer,
        None,
        f"{image_name}.jpg",  # use base name without file extension
        "image/jpeg",
        image_buffer.tell(),
        None,
    )
    # Return processed image
    return image_file
