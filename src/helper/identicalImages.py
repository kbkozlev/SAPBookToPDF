from PIL import Image


def are_images_identical(image1: str, image2: str) -> bool:
    """
    Takes in the last two images in the list and compares the pixels.
    If they are the same returns True
    :param image1:
    :param image2:
    :return:
    """

    if Image.open(image1) == Image.open(image2):
        return True

    else:
        return False
