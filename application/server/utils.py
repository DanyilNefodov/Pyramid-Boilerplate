from PIL import Image 
from io import BytesIO

def crop_image(image: bytes, path_to_save: str):
    im = Image.open(image) 
 
    width, height = im.size 

    left = width / 2 - 300
    top = height / 2 - 300
    right = width / 2 + 300
    bottom = height / 2 + 300

    croped_image = im.crop((left, top, right, bottom)) 

    croped_image.save(path_to_save)


def get_size(image: bytes):
    return Image.open(BytesIO(image)).size
