# imports for utility functions for image processing
from PIL import Image
import os
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

# Functions used to process images


def process_photo(uploaded_photo):
    """
    process photos to max h/w 450px and jpeg format
    """
    photo = uploaded_photo
    # open image in Pillow to process
    image = Image.open(photo)
    # resize image to 450px max h/w
    max_size = (450, 450)
    image.thumbnail(max_size, Image.ANTIALIAS)
    # remove file extension from image name
    image_name, _ = os.path.splitext(uploaded_photo.name)
    # create a BytesIO buffer to temporarily store image
    image_buffer = BytesIO()
    image.save(image_buffer, format="JPEG")
    # create an InMemoryUploadedFile from buffer
    image_file = InMemoryUploadedFile(
        image_buffer,
        None,
        f"{image_name}.jpg",  # use base name without file extension
        "image/jpeg",
        image_buffer.tell(),
        None,
    )
    # Return processed image_file and replace the original uploaded image
    return image_file
