from typing import List, TypeVar
from uuid import UUID

from pydantic.dataclasses import dataclass
from dataclasses_json import dataclass_json

from boxdiff.models.deltas import BoundingBoxDelta, ImageDelta, ImageSetDelta


ID = TypeVar('ID', int, UUID, str)  # Parses in order: int, UUID, then str


@dataclass_json
@dataclass
class BoundingBox:
    """
    Identified 2D bounding box: label + position, width, and height.
    """

    id: ID
    label: str
    x: float
    y: float
    width: float
    height: float

    def __sub__(self, other: 'BoundingBox') -> BoundingBoxDelta:
        """
        Compute the delta between two bounding boxes.
        """
        return BoundingBoxDelta(
            self.id,
            other.label,
            self.label,
            self.x - other.x,
            self.y - other.y,
            self.width - other.width,
            self.height - other.height,
        )

    def __add__(self, delta: BoundingBoxDelta) -> 'BoundingBox':
        return BoundingBox(
            delta.id,
            delta.new_label,
            self.x + delta.delta_x,
            self.y + delta.delta_y,
            self.width + delta.delta_width,
            self.height + delta.delta_height,
        )

    def __iadd__(self, delta: BoundingBoxDelta) -> 'BoundingBox':
        self.label = delta.new_label
        self.x += delta.delta_x
        self.y += delta.delta_y
        self.width += delta.delta_width
        self.height += delta.delta_height
        return self


@dataclass_json
@dataclass
class Image:
    """
    Identified list of bounding boxes.
    """

    id: ID
    bounding_boxes: List[BoundingBox]

    def __sub__(self, other: 'Image') -> 'ImageDelta':
        """
        Compute the delta between two images.
        """
        # Get the unique set of IDs for the boxes in each image
        box_ids_self = {box.id for box in self.bounding_boxes}
        box_ids_other = {box.id for box in other.bounding_boxes}

        # Find the boxes that are in one image but not the other
        boxes_added = [
            box for box in other.bounding_boxes if box.id not in box_ids_self
        ]
        boxes_removed = [
            box for box in self.bounding_boxes if box.id not in box_ids_other
        ]

        # Find the boxes that are in both images
        box_ids_common = box_ids_self & box_ids_other
        boxes_common_self = sorted(
            [box for box in self.bounding_boxes if box.id in box_ids_common],
            key=lambda box: box.id,
        )
        boxes_common_other = sorted(
            [box for box in other.bounding_boxes if box.id in box_ids_common],
            key=lambda box: box.id,
        )

        assert len(boxes_common_self) == len(
            boxes_common_other
        ), 'Common box count mismatch'

        # Compute the deltas between the common boxes
        box_deltas = []
        for box_self, box_other in zip(boxes_common_self, boxes_common_other):
            box_deltas.append(box_self - box_other)

        return ImageDelta(self.id, boxes_added, boxes_removed, box_deltas)


@dataclass_json
@dataclass
class ImageSet:
    """
    Identified list of images.
    """

    id: ID
    images: List[Image]

    def __sub__(self, other: 'ImageSet') -> ImageSetDelta:
        """
        Compute the delta between two image sets.
        """
        # Get the unique set of IDs for the images in each set
        image_ids_self = {image.id for image in self.images}
        image_ids_other = {image.id for image in other.images}

        # Find the images that are in one set but not the other
        images_added = [
            image for image in other.images if image.id not in image_ids_self
        ]
        images_removed = [
            image for image in self.images if image.id not in image_ids_other
        ]

        # Find the images that are in both sets
        image_ids_common = image_ids_self & image_ids_other
        images_common_self = sorted(
            [image for image in self.images if image.id in image_ids_common],
            key=lambda im: im.id,
        )
        images_common_other = sorted(
            [image for image in other.images if image.id in image_ids_common],
            key=lambda im: im.id,
        )

        assert len(images_common_self) == len(
            images_common_other
        ), 'Common image count mismatch'

        # Compute the deltas between the common images
        image_deltas = []
        for image_self, image_other in zip(images_common_self, images_common_other):
            image_deltas.append(image_self - image_other)

        return ImageSetDelta(self.id, images_added, images_removed, image_deltas)
