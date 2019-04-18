from PIL import Image


def transparency(image1, image2):
    res = jpg
    imagee = Image.open(image1)
    imagee2 = Image.open(image2)

    w, h = imagee.size

    for x in range(w):
        for y in range(h):
            pix_coord = (x, y)
            r, g, b = imagee.getpixel(pix_coord)
            r1, g1, b1 = imagee2.getpixel(pix_coord)
            new_col = (int(0.5 * r + 0.5 * r1), int(0.5 * g + 0.5 * g1), int(0.5 * b + 0.5 * b1))
            imagee.putpixel(pix_coord, new_col)
            res.jpg = imagee