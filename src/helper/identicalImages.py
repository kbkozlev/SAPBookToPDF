from PIL import Image


def are_images_identical(image_path1: str, image_path2: str, threshold: int = 1) -> bool:
    """
    Takes in the last two images in the list and compares the hashes.
    If they are the same returns true
    :param image_path1:
    :param image_path2:
    :param threshold:
    :return:
    """

    img1 = Image.open(image_path1)
    img2 = Image.open(image_path2)

    if img1 == img2:
        return True

    else:
        return False
