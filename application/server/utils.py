import PIL
from PIL import Image
from io import BytesIO

from server.models import (
    DBSession,
    Banner)


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


def filter_banners_by_search(search_request: dict):
    search_title = search_request.get("title", "")
    search_url = search_request.get("url", "")
    search_visible = search_request.get("visible", 0)

    banners = DBSession.query(Banner).order_by(
            Banner.position, Banner.id).filter(Banner.title.like(f"{search_title}%"), Banner.url.like(f"{search_url}%"))

    if search_visible != 0:
        if search_visible == 1:
            visible = True
        if search_visible == 2:
            visible = False

        banners = banners.filter(Banner.visible == visible)

    return banners
