import math
import os

import numpy as numpy
from PIL import Image, ImageChops


def find_coefficients(source_coords, target_coords):
    matrix = []
    for s, t in zip(source_coords, target_coords):
        matrix.append([t[0], t[1], 1, 0, 0, 0, -s[0]*t[0], -s[0]*t[1]])
        matrix.append([0, 0, 0, t[0], t[1], 1, -s[1]*t[0], -s[1]*t[1]])
    A = numpy.matrix(matrix, dtype=numpy.float64)
    B = numpy.array(source_coords).reshape(8)
    res = numpy.dot(numpy.linalg.inv(A.T * A) * A.T, B)
    return numpy.array(res).reshape(8)

def perform_perspective_transform(img, direction=False):
    # Some terrifying matrix math
    if not direction:
        transform_corners = [
            (0 * img.width, 0.2 * img.height),  # Top left
            (0.6 * img.width, 0 * img.height),  # Top right
            (0.6 * img.width, 1 * img.height),  # Bottom right
            (0 * img.width, 0.8 * img.height)  # Bottom left
        ]
    else:
        transform_corners = [
            (0 * img.width, 0 * img.height),  # Top left
            (0.6 * img.width, 0.2 * img.height),  # Top right
            (0.6 * img.width, 0.8 * img.height),  # Bottom right
            (0 * img.width, 1 * img.height)  # Bottom left
        ]
    coefficients = find_coefficients([
        (0, 0), # Top left
        (img.width, 0), # Top right
        (img.width, img.height), # Bottom right
        (0, img.height) # Bottom right
    ], transform_corners)

    # Perform transformation based on coords
    return img.transform((math.ceil(0.6*img.width),img.height), Image.Transform.PERSPECTIVE, coefficients, Image.Resampling.BICUBIC)

def multiply_alpha_gradient(img, direction=False):
    # Create a linear, grayscale gradient
    alpha = Image.linear_gradient('L').rotate(-90 if direction else 90).resize((img.width, img.height))
    # Mask the gradient to the image
    img_alpha = img.split()[-1]
    # Set the masked gradient as the alpha channel for the image
    img.putalpha(ImageChops.multiply(alpha, img_alpha))
    return img

def corner_pin_effect(path):
    # First determine if the image is real
    img = Image.open(path).convert("RGBA")

    # Get left and right transform
    img_left = perform_perspective_transform(img, True)
    img_right = perform_perspective_transform(img, False)

    # Get the alphagradients
    img_left = multiply_alpha_gradient(img_left, True)
    img_right = multiply_alpha_gradient(img_right, False)

    # Prepare file path
    left_path = path[0:path.find(".")] + "_left" + path[path.find("."):]
    right_path = path[0:path.find(".")] + "_right" + path[path.find("."):]

    # Save the files
    img_left.save(left_path)
    img_right.save(right_path)

# if __name__ == "__main__":
#     basedir = "D:\\Dev\\Python\\cdp_db_site\\media\\images"
#     for image in os.listdir("D:\\Dev\\Python\\cdp_db_site\\media\\images"):
#         corner_pin_effect(basedir + "\\" + image)