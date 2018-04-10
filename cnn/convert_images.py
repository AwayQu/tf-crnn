from glob import glob

try:
    from StringIO import StringIO
except ImportError:
    from io import BytesIO as StringIO
from PIL import Image, ImageOps
from os.path import dirname

size = (28, 28)


def file_name(file_path):
    return file_path.split('/')[-1]


img_p = "../data_extract/output/*.png"


def save_img(file_path, thumb):
    thumb_buffer = StringIO()
    thumb.save(thumb_buffer, format=img.format)
    fp = open("../data_extract/aspect_ratio_fill_imgs/{}".format(file_name(file_path)), "wb")
    fp.write(thumb_buffer.getvalue())
    fp.close()


def write_img(file_path):
    img = Image.open(file_path)
    thumb = ImageOps.fit(img, size, Image.ANTIALIAS)
    save_img(file_path, thumb)


for file_count, file_path in enumerate(sorted(glob(img_p))):
    img = Image.open(file_path)
    x, y = img.size

    m = max(x, y)

    factor = 28.0 / m

    size = (int(round(factor * x)),
            int(round(factor * y)))

    image = img.resize(size, Image.ANTIALIAS)
    x, y = image.size

    new_im = Image.new('RGBA', (28, 28), (255, 255, 255, 255))
    new_im.paste(image, (int((28 - x) / 2), int((28 - y) / 2)))

    save_img(file_path, new_im)
