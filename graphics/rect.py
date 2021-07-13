""" This script is used to convert an image with the appropriate graphics mode
    resolution from square pixels, to 5x4 rectangular pixels in a 640x480 canvas.
"""

from PIL import Image

resolution = (640, 480)
final_pixel_size = (5, 4)

final_image = Image.new("RGB", resolution, color=(0, 0, 0))
finch_image = Image.open("roof-korean.png")

finch_res = finch_image.size

count = 0
for j in range(finch_res[1]):  # for every row
    for i in range(finch_res[0]):  # for every col
        pixel_color = finch_image.getpixel((i, j))
        im = Image.new("RGBA", final_pixel_size, color=pixel_color)
        Image.Image.paste(
            final_image, im, (i * final_pixel_size[0], j * final_pixel_size[1])
        )

final_image.save("roof-korean_5x4.png")