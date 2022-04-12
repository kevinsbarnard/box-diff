from typing import List, TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from boxdiff.models.core import ID, BoundingBox
from boxdiff.models.flags import (
    BoundingBoxDifference,
    ImageDifference,
    ImageSetDifference,
)


@dataclass
class BoundingBoxDelta:
    id: 'ID'
    label_old: str
    label_new: str
    x_delta: float
    y_delta: float
    width_delta: float
    height_delta: float

    @property
    def flags(self) -> BoundingBoxDifference:
        f = BoundingBoxDifference(0)

        if self.label_old != self.label_new:
            f |= BoundingBoxDifference.RELABELED

        if self.x_delta != 0 or self.y_delta != 0:
            f |= BoundingBoxDifference.MOVED

        if self.width_delta != 0 or self.height_delta != 0:
            f |= BoundingBoxDifference.RESIZED

        return f


@dataclass
class ImageDelta:
    id: 'ID'
    boxes_added: List['BoundingBox']
    boxes_removed: List['BoundingBox']
    box_deltas: List[BoundingBoxDelta]

    @property
    def flags(self) -> ImageDifference:
        f = ImageDifference(0)

        if self.boxes_added:
            f |= ImageDifference.BOXES_ADDED

        if self.boxes_removed:
            f |= ImageDifference.BOXES_REMOVED

        if any(delta.flags for delta in self.box_deltas):
            f |= ImageDifference.BOXES_MODIFIED

        return f


@dataclass
class ImageSetDelta:
    id: 'ID'
    images_added: List[ImageDelta]
    images_removed: List[ImageDelta]
    image_deltas: List[ImageDelta]

    @property
    def flags(self) -> ImageSetDifference:
        f = ImageSetDifference(0)

        if self.images_added:
            f |= ImageSetDifference.IMAGES_ADDED

        if self.images_removed:
            f |= ImageSetDifference.IMAGES_REMOVED

        if any(delta.flags for delta in self.image_deltas):
            f |= ImageSetDifference.IMAGES_MODIFIED

        return f
