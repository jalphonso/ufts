from wand.image import Image
from wand.color import Color
from django.utils.crypto import get_random_string


def create_image_from_pdf(pdfpath):
    """Generate image from pdf.

    Saves the image to the MEDIA_ROOT/images directory

    Args
    ----
        pdfpath (str)
            path to pdf

    Returns
    -------
        path to the saved image
    """
    randname = get_random_string()
    imgtemp = os.path.join(settings.TEMP_DIR, '{}.png'.format(randname))
    imgsaved = os.path.join(settings.MEDIA_ROOT, 'images', '{}.png'.format(randname))

    # generate temporary image first
    with Image(filename='{}[0]'.format(pdfpath), resolution=300) as img:
        img.background_color = Color('white')
        img.alpha_channel = 'remove'
        if not os.path.exists(settings.TEMP_DIR):
            os.makedirs(settings.TEMP_DIR)
        img.save(filename=imgtemp)

    # resize temporary image
    with Image(filename=imgtemp) as img:
        width, height = img.size
        if width > 500:
            ratio = width * 1.0 / 500
            new_width = 500
            new_height = height / ratio
        else:
            new_width = width
            new_height = height
        img.resize(int(new_width), int(new_height))
        img.save(filename=imgsaved)
    # delete temp image file
    os.remove(imgtemp)

    return imgsaved