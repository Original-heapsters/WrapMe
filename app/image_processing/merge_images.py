from PIL import Image

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
        overlay = Image.open(image)
        overlay = resize_image(overlay, size)
        base_img.paste(overlay,coords,overlay)

    base_img.show()


if __name__ == '__main__':
    merge_images('../static/images/image.png', '../static/images/basic_tattoo.png', debug=True)
    base = '../static/images/image.png'
    overlay_dict = [('../static/images/basic_tattoo.png', (0,0), (100,100)),
    ('../static/images/basic_tattoo.png', (100,100), (500,500)),
    ('../static/images/basic_tattoo.png', (200,200), (350,350)),
    ('../static/images/basic_tattoo.png', (800,800), (50,50)),
    ('../static/images/basic_tattoo.png', (2000,2000), (10,10))
    ]

    merge_set(base, overlay_dict)
