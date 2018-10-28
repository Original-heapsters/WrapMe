import os
import random
from PIL import Image

tattoo_dir = 'tattoos'

def merge_images(base, overlay, coords=(0,0), debug=False):
    print(base)
    print(overlay)
    background = Image.open(base)
    foreground = Image.open(overlay)

    background.paste(foreground, coords, foreground)
    if debug:
        background.show()
    return background

def get_image_size(input_img):
    w, h = input_img.size
    return { 'width': w, 'height': h }

def resize_image(input_img, new_size):
    input_img.thumbnail(new_size, Image.ANTIALIAS)

    return input_img

def merge_set(base, overlays):
    tmp = base
    base_img = Image.open(base)
    for (image, coords, size) in overlays:
        top,left = coords
        w,h = size
        new_coord = (random.randint(300,450), random.randint(145,294))
        new_size = (random.randint(10,50),random.randint(10,50))
        overlay = Image.open(image).convert("RGBA")
        overlay = resize_image(overlay, new_size)
        base_img.paste(overlay,new_coord,overlay)

    base_img.show()

def choose_random_tattoo():
    file_name = random.choice(os.listdir(tattoo_dir))
    path = os.path.join(tattoo_dir, file_name)

    return path


if __name__ == '__main__':
    # merge_images('../static/images/image.png', '../static/images/basic_tattoo.png', debug=True)
    base = '../static/images/image.png'

    overlay_dict = [#('../static/images/basic_tattoo.png', (0,0), (100,100)),
    ('../static/images/basic_tattoo.png', (327,145), (149,149))
    # ('../static/images/basic_tattoo.png', (200,200), (350,350)),
    # ('../static/images/basic_tattoo.png', (800,800), (50,50)),
    # ('../static/images/basic_tattoo.png', (2000,2000), (10,10))
    ]

    for i in range(0,50):
        image = choose_random_tattoo()
        coord = (327,145)
        size = (149,149)
        overlay_dict.append((image, coord, size))

    merge_set(base, overlay_dict)
