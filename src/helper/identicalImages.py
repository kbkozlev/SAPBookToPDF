from PIL import Image


def are_images_identical(image1: str, image2: str) -> bool:
    """
    Takes in the last two images in the list and compares the hashes.
    If they are the same returns true
    :param image1:
    :param image2:
    :return:
    """

    img1 = Image.open(image1)
    img2 = Image.open(image2)

    if img1 == img2:
        return True

    else:
        return False
