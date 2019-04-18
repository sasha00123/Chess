from PIL import Image


def transparency(ﬁlename1, ﬁlename2):
    im1 = Image.open(ﬁlename1)
    im2 = Image.open(ﬁlename2)
    z, y = im1.size

    for x in range(z):
        for y in range(y):
            r, g, b = im1.getpixel(pix_cords)
            r1, g1, b1 = im2.getpixel(pix_cords)
            new_col = (int(0.5 * r + 0.5 * r), int(0.5 * g + 0.5 * g), int(0.5 * b + 0.5 * b))
            pix_cords = (int(0.5 * r1 + 0.5 * r1), int(0.5 * g1 + 0.5 * g1), int(0.5 * b1 + 0.5 * b1))
            im1.putpixel = pix_cords + new_col
    im1.save('res.jpg')