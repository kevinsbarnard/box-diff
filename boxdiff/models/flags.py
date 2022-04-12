from enum import Flag, auto


class BoundingBoxDifference(Flag):
    """
    Flag enum for the different types of box-level differences.
    """

    MOVED = auto()
    RESIZED = auto()
    RELABELED = auto()


class ImageDifference(Flag):
    """
    Flag enum for the different types of image-level differences.
    """

    BOXES_ADDED = auto()
    BOXES_REMOVED = auto()
    BOXES_MODIFIED = auto()


class ImageSetDifference(Flag):
    """
    Flag enum for the different types of image-set-level differences.
    """

    IMAGES_ADDED = auto()
    IMAGES_REMOVED = auto()
    IMAGES_MODIFIED = auto()
