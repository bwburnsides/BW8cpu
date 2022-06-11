""" This script is used to produce VGA RGB color palettes of a specified bit depth.
"""

import itertools as it
from pprint import pprint
from PIL import Image

parts = ("00", "01", "10", "11")
hex_map = {"00": "00", "01": "55", "10": "aa", "11": "ff"}

colors = list(it.product(parts, repeat=3))

sorted_colors = sorted(colors, key=lambda x: int("".join(x), base=2))

final_colors = []

for color in sorted_colors:
    hex_color = f"{hex_map[color[0]]}{hex_map[color[1]]}{hex_map[color[2]]}"
    final_colors.append(hex_color)

cell_size = 128
images = []
for color in final_colors:
    r = int(255 * (int(color[0:2], base=16) / int("ff", base=16)))
    g = int(255 * (int(color[2:4], base=16) / int("ff", base=16)))
    b = int(255 * (int(color[4:6], base=16) / int("ff", base=16)))
    im = Image.new("RGB", (cell_size, cell_size), color=(r, g, b))
    images.append(im)

final_image = Image.new(
    "RGB", (cell_size * len(final_colors), cell_size), color=(0, 0, 0)
)
for i, im in enumerate(images):
    box = (cell_size * i, 0, cell_size, cell_size)
    Image.Image.paste(final_image, im, (cell_size * i, 0))

final_image.save("test_image.png")
