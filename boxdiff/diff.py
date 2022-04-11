from boxdiff.models.core import BoundingBox, Image, ImageSet
from boxdiff.models.flags import (
    BoundingBoxDifference,
    ImageDifference,
    ImageSetDifference,
)


def bounding_box_diff(box1: BoundingBox, box2: BoundingBox) -> BoundingBoxDifference:
    """
    Compute the difference between two bounding boxes.
    """
    flags = 0

    if box2.x != box1.x or box2.y != box1.y:
        flags |= BoundingBoxDifference.MOVED

    if box2.width != box1.width or box2.height != box1.height:
        flags |= BoundingBoxDifference.RESIZED

    if box2.label != box1.label:
        flags |= BoundingBoxDifference.RELABELED

    return flags


def image_diff(image1: Image, image2: Image) -> ImageDifference:
    """
    Compute the difference between two images.
    """
    flags = 0

    image1_ids = set(box.id for box in image1.bounding_boxes)
    image2_ids = set(box.id for box in image2.bounding_boxes)

    if image2_ids - image1_ids:
        flags |= ImageDifference.BOXES_ADDED

    if image1_ids - image2_ids:
        flags |= ImageDifference.BOXES_REMOVED

    return flags


def image_set_diff(set1: ImageSet, set2: ImageSet) -> ImageSetDifference:
    """
    Compute the difference between two image sets.
    """
    flags = 0

    set1_ids = set(image.id for image in set1.images)
    set2_ids = set(image.id for image in set2.images)

    if set2_ids - set1_ids:
        flags |= ImageSetDifference.IMAGES_ADDED

    if set1_ids - set2_ids:
        flags |= ImageSetDifference.IMAGES_REMOVED

    return flags
