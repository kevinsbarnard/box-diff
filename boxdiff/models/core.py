from typing import List, TypeVar
from uuid import UUID

from pydantic.dataclasses import dataclass
from dataclasses_json import dataclass_json


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


@dataclass_json
@dataclass
class Image:
    """
    Identified list of bounding boxes.
    """

    id: ID
    bounding_boxes: List[BoundingBox]


@dataclass_json
@dataclass
class ImageSet:
    """
    Identified list of images.
    """

    id: ID
    images: List[Image]
