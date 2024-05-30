from io import BytesIO

from PIL import Image
from PIL.ExifTags import TAGS
from django.utils import timezone


def get_metadata_from_img(path):
    """
    Function get latitude, longitude, height and image_creation_date metadata from JPG file
    """
    image_creation_date = latitude = longitude = height = None

    # Open the image file
    image = Image.open(path)
    print(image)

    # Get EXIF data
    exif_data = image._getexif()
    if exif_data:
        for tag, value in exif_data.items():
            tag_name = TAGS.get(tag)
            if tag_name == 'DateTimeOriginal':
                image_creation_date = timezone.datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
                break

    # Get GPS data
    gps_info = exif_data.get(34853) if exif_data else None
    if gps_info:
        # Extract latitude, longitude, and height
        latitude_ref = gps_info.get(1)
        latitude = gps_info.get(2)
        longitude_ref = gps_info.get(3)
        longitude = gps_info.get(4)
        if latitude and longitude:
            latitude = latitude[0] + latitude[1] / 60 + latitude[2] / 3600
            longitude = longitude[0] + longitude[1] / 60 + longitude[2] / 3600
            if latitude_ref == 'S':
                latitude = -latitude
            if longitude_ref == 'W':
                longitude = -longitude
            latitude = latitude
            longitude = longitude
        # Extract height if available
        altitude = gps_info.get(6)
        if altitude:
            height = float(altitude)

    return image_creation_date, latitude, longitude, height


def image_compression(image_field, quality: int, resize_percent=None):
    """
    Compresses the given image with the specified quality and returns the compressed image.
    Optionally resizes the image by the given percentage.
    """
    # Opening an image using Pillow
    image = Image.open(image_field)
    # Creating a Buffer for a Compressed Image
    compressed_img_buffer = BytesIO()

    # Compressing an image and saving it to a buffer
    img = image.copy()
    if resize_percent:
        # Calculate new image dimensions
        width, height = img.size
        new_width = int(width * (resize_percent / 100))
        new_height = int(height * (resize_percent / 100))

        # Resize Image
        img = img.resize((new_width, new_height), Image.LANCZOS)

    # Compressing an image and saving it to a buffer
    img.save(compressed_img_buffer, format=image.format, quality=quality)

    return compressed_img_buffer


def get_youtube_for_iframe_from_youtube(youtube: str):
    """
        Function transfer YouTube link to YouTube link for InfoSpot iframe
    """
    video_id = youtube.split('v=')[1]
    return f'https://www.youtube.com/embed/{video_id}?&amp;autoplay=1&mute=1&disablekb=1&loop=1&playlist={video_id}&controls=0&iv_load_policy=3'
