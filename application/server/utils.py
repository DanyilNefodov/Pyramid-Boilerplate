import PIL
from PIL import Image
from io import BytesIO


def crop_image(image: bytes, image_title: str, image_type: str):
    im = Image.open(image)

    width, height = im.size

    size = width if width < height else height

    left = width / 2 - size / 2
    top = height / 2 - size / 2
    right = width / 2 + size / 2
    bottom = height / 2 + size / 2

    croped_image = im.crop((left, top, right, bottom))

    im.save(f"server/static/raw_img/{image_title}{image_type}")
    croped_image.resize((600, 600), Image.ANTIALIAS).save(f"server/static/banner_img/{image_title}{image_type}")


def get_size(image: bytes):
    try:
        return Image.open(BytesIO(image)).size
    except PIL.UnidentifiedImageError:
        return (0, 0)
