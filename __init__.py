import numpy as np
from PIL import Image
import os
import sys

char_ramp_10 = " .:-=+*#%@"
char_ramp_70 = " .'`^\",:;Il!i><~+_-?][}{1)(|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"


def get_image(image_path):
    """
    return 2D ay of RGB values of each pixel
    """
    im = Image.open(image_path, 'r')
    width, height = im.size
    pixel_values = np.array(im).reshape((height, width, 3))
    return pixel_values


def rgb_sum(pixel):
    """
    calculate sum of RGB values of pixel
    """
    return int(pixel[0]) + int(pixel[1]) + int(pixel[2])


def average_rgb_sum(start_x, start_y, width, height, pixels):
    """
    calculate average sum of RGB values in an area of specified width and height
    """
    sum = 0
    for y in range(start_y, start_y + height):
        for x in range(start_x, start_x + width):
            sum += rgb_sum(pixels[y][x])
    return sum / (width * height)


def rgb_sum_to_char(rgb_sum, char_ramp):
    """
    determine character from given RGB sum
    """
    rgb_ratio = rgb_sum / (255 * 3)
    index = int(rgb_ratio * (len(char_ramp) - 1))
    return char_ramp[index]


def image_to_characters(image, width, height, char_ramp, row_factor):
    """
    return image as characters in string
    """
    res = ""
    pixels = get_image(image)
    x, y = 0, 0
    while y + height < len(pixels):
        x = 0
        while x + width < len(pixels[0]):
            block_average_sum = average_rgb_sum(x, y, width, height, pixels)
            res += rgb_sum_to_char(block_average_sum, char_ramp)
            x += width
        res += "\n"
        y += height * row_factor
    return res


def write_to_file(s, input_file):
    """
    write string to output file in output folder, 
    create output folder if doesn't exist
    """
    if not os.path.isdir("output"):
        os.mkdir("output")
    last_slash = input_file.rfind("/")
    last_dot = input_file.rfind(".")
    output_file = "output/" + input_file[last_slash + 1:last_dot] + ".txt"
    with open(output_file, "w") as text_file:
        text_file.write(s)


if __name__ == "__main__":
    input_file = "images/sleepy.jpg"
    pix_sample_width = 5
    pix_sample_height = 5
    row_factor = 2
    char_ramp = char_ramp_10

    image_str = image_to_characters(
        input_file, pix_sample_width, pix_sample_height, char_ramp, row_factor)
    write_to_file(image_str, input_file)
