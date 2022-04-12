# box-diff
Utilities for comparing bounding boxes

Author: Kevin Barnard, [kbarnard@mbari.org](mailto:kbarnard@mbari.org)

[![tests](https://github.com/kevinsbarnard/box-diff/workflows/tests/badge.svg)](https://github.com/kevinsbarnard/box-diff/actions/workflows/tests.yml)


## Installation

box-diff is available on PyPI as [boxdiff](https://pypi.org/project/boxdiff/):

```bash
pip install boxdiff
```

## Usage

All of box-diff is housed within the `boxdiff` package.

```python
import boxdiff
```

The core data models are defined in the `boxdiff.models` module. These are split into three groups:
- `BoundingBox`: ID + labeled 2D bounding box
- `Image`: ID + collection of bounding boxes
- `ImageSet`: ID + collection of images

*Note: IDs may be integers, UUIDs, or strings.*

Each group has a data model (defined in `boxdiff.models.core`), a delta (`boxdiff.models.deltas`), and a difference flag (`boxdiff.models.flags`).
The data model represents the object and its attributes, whereas a delta represents the difference in attribute values between two objects.
Difference flags represent the presence of attribute differences between two objects as derived from a delta object.

All of the data models are serializable to JSON. For example,
```python
json_str = bounding_box.to_json(indent=2)

print(json_str)
```
might give
```json
{
  "id": 0,
  "label": "label",
  "x": 0.0,
  "y": 0.0,
  "width": 1.0,
  "height": 1.0
}
```

Similarly, data model objects may be parsed from JSON. For example,
```python
bounding_box = BoundingBox.from_json(json_str)

print(bounding_box)
# BoundingBox(id=0, label='label', x=0.0, y=0.0, width=1.0, height=1.0)
```

### Bounding Boxes

A `BoundingBox` is defined by an ID, a label, and a 2D box (x, y, width, height).

```python
from boxdiff import BoundingBox

car_box = BoundingBox(
    id=0,
    label='car',
    x=100, y=200,
    width=300, height=80
)
```

Equality can be checked using the `==` operator:

```python
same_car_box = BoundingBox(
    id=0,
    label='car',
    x=100, y=200,
    width=300, height=80
)

print(car_box == same_car_box)
# True

corrected_car_box = BoundingBox(
    id=0,
    label='car',
    x=90, y=210,
    width=320, height=85
)

print(car_box == corrected_car_box)
# False
```

A `BoundingBoxDelta` between two boxes can be computed with the `-` operator:

```python
box_delta = corrected_car_box - car_box

print(box_delta)
# BoundingBoxDelta(id=1, label_old='car', label_new='car', x_delta=-10.0, y_delta=10.0, width_delta=20.0, height_delta=5.0)
```

`BoundingBoxDifference` flags may then be computed from the delta:

```python
print(box_delta.flags)
# BoundingBoxDifference.RESIZED|MOVED
```

Deltas may be applied to a bounding box using the `+` operator:

```python
new_car_box = car_box + box_delta

print(new_car_box)
# BoundingBox(id=1, label='car', x=90.0, y=210.0, width=320.0, height=85.0)

print(new_car_box == corrected_car_box)
# True
```

Area may be computed from a bounding box:

```python
print(car_box.area)
# 24000.0
```

Intersection over union between bounding boxes can be computed using the `iou` method:

```python
car_iou = car_box.iou(corrected_car_box)

print(car_iou)
# 0.695364238410596
```

### Images

An `Image` is defined by an ID and a collection of bounding boxes.

```python
from boxdiff import Image
from uuid import UUID

image = Image(
    id=UUID('78d76772-4664-467c-ae88-a25496234966'),
    bounding_boxes=[car_box]
)
```

Likewise, equality can be checked using the `==` operator and deltas computed using the `-` operator:

```python
corrected_image = Image(
    id=UUID('78d76772-4664-467c-ae88-a25496234966'),
    bounding_boxes=[corrected_car_box]
)

image_delta = corrected_image - image

print(image_delta)
# ImageDelta(
#   id=0, 
#   boxes_added=[], 
#   boxes_removed=[], 
#   box_deltas=[
#     BoundingBoxDelta(
#       id=0, 
#       label_old='car', 
#       label_new='car', 
#       x_delta=-10.0, 
#       y_delta=10.0, 
#       width_delta=20.0, 
#       height_delta=5.0
#     )
#   ]
# )
```

Similarly, flags may be computed from the delta:

```python
print(image_delta.flags)
# ImageDifference.BOXES_MODIFIED
```

### Image Sets

An `ImageSet` is defined by an ID and a collection of images.

```python
from boxdiff import ImageSet

image_set = ImageSet(
    id='my_image_set',
    images=[image, ...]
)
```

Its syntax and structure is analogous to that of an `Image`.
