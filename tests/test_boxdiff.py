import json
from unittest import TestCase
from uuid import UUID, uuid4

from random import randint

from boxdiff.models.core import BoundingBox
from boxdiff.models.deltas import BoundingBoxDelta
from boxdiff.models.flags import BoundingBoxDifference


class TestSerialization(TestCase):
    def setUp(self) -> None:
        # Common test box label
        self.box_label = 'test'

        # Create a bounding box template JSON string with the common test label
        self.box_json_str_template = '''
        {{{{
            "id": {{id}},
            "label": "{label}",
            "x": 0.0,
            "y": 0.0,
            "width": 1.0,
            "height": 1.0
        }}}}
        '''.format(
            label=self.box_label
        )

    def test_serialization_with_int_id(self):
        # Create a bounding box JSON string with a random integer ID
        box_with_int_id_id = randint(1, 100)
        box_with_int_id_json_str = self.box_json_str_template.format(
            id=box_with_int_id_id
        )

        # Deserialize the bounding box JSON string
        box_with_int_id = BoundingBox.from_json(box_with_int_id_json_str)

        # Check that the bounding box has a matching integer ID
        self.assertIsInstance(box_with_int_id.id, int)
        self.assertEqual(box_with_int_id_id, box_with_int_id.id)

        # Serialize the bounding box
        serialized_box_with_int_id_json_str = box_with_int_id.to_json()

        # Check that the bounding box JSON string is valid
        true_json_str = json.dumps(json.loads(box_with_int_id_json_str))
        self.assertEqual(true_json_str, serialized_box_with_int_id_json_str)

    def test_serialization_with_uuid_id(self):
        # Create a bounding box JSON string with a random UUID ID
        box_with_uuid_id_id = uuid4()
        box_with_uuid_id_json_str = self.box_json_str_template.format(
            id=f'"{box_with_uuid_id_id}"'
        )

        # Deserialize the bounding box JSON string
        box_with_uuid_id = BoundingBox.from_json(box_with_uuid_id_json_str)

        # Check that the bounding box has a matching UUID ID
        self.assertIsInstance(box_with_uuid_id.id, UUID)
        self.assertEqual(box_with_uuid_id_id, box_with_uuid_id.id)

        # Serialize the bounding box
        serialized_box_with_int_id_json_str = box_with_uuid_id.to_json()

        # Check that the bounding box JSON string is valid
        true_json_str = json.dumps(json.loads(box_with_uuid_id_json_str))
        self.assertEqual(true_json_str, serialized_box_with_int_id_json_str)

    def test_serialization_with_str_id(self):
        # Create a bounding box JSON string with a given string ID
        box_with_str_id_id = 'test_id'
        box_with_str_id_json_str = self.box_json_str_template.format(
            id=f'"{box_with_str_id_id}"'
        )

        # Deserialize the bounding box JSON string
        box_with_str_id = BoundingBox.from_json(box_with_str_id_json_str)

        # Check that the bounding box has a matching string ID
        self.assertIsInstance(box_with_str_id.id, str)
        self.assertEqual(box_with_str_id_id, box_with_str_id.id)

        # Serialize the bounding box
        serialized_box_with_int_id_json_str = box_with_str_id.to_json()

        # Check that the bounding box JSON string is valid
        true_json_str = json.dumps(json.loads(box_with_str_id_json_str))
        self.assertEqual(true_json_str, serialized_box_with_int_id_json_str)


class TestBoundingBoxDeltas(TestCase):
    def setUp(self) -> None:
        self.base_bounding_box = BoundingBox('test', 'test', 0.0, 0.0, 1.0, 1.0)

        self.move_delta = BoundingBoxDelta('test', 'test', 'test', 1.0, 1.0, 0.0, 0.0)
        self.moved_bounding_box = BoundingBox('test', 'test', 1.0, 1.0, 1.0, 1.0)

        self.resize_delta = BoundingBoxDelta('test', 'test', 'test', 0.0, 0.0, 1.0, 1.0)
        self.resized_bounding_box = BoundingBox('test', 'test', 0.0, 0.0, 2.0, 2.0)

        self.relabel_delta = BoundingBoxDelta(
            'test', 'test', 'test_relabeled', 0.0, 0.0, 0.0, 0.0
        )
        self.relabeled_bounding_box = BoundingBox(
            'test', 'test_relabeled', 0.0, 0.0, 1.0, 1.0
        )

    def test_compute_move_delta(self):
        computed_move_delta = self.moved_bounding_box - self.base_bounding_box
        self.assertEqual(self.move_delta, computed_move_delta)
        self.assertEqual(BoundingBoxDifference.MOVED, computed_move_delta.flags)

    def test_compute_resize_delta(self):
        computed_resize_delta = self.resized_bounding_box - self.base_bounding_box
        self.assertEqual(self.resize_delta, computed_resize_delta)
        self.assertEqual(BoundingBoxDifference.RESIZED, computed_resize_delta.flags)

    def test_compute_relabel_delta(self):
        computed_relabel_delta = self.relabeled_bounding_box - self.base_bounding_box
        self.assertEqual(self.relabel_delta, computed_relabel_delta)
        self.assertEqual(BoundingBoxDifference.RELABELED, computed_relabel_delta.flags)

    def test_apply_move_delta(self):
        computed_moved_bounding_box = self.base_bounding_box + self.move_delta
        self.assertEqual(self.moved_bounding_box, computed_moved_bounding_box)

    def test_apply_resize_delta(self):
        computed_resized_bounding_box = self.base_bounding_box + self.resize_delta
        self.assertEqual(self.resized_bounding_box, computed_resized_bounding_box)

    def test_apply_relabel_delta(self):
        computed_relabeled_bounding_box = self.base_bounding_box + self.relabel_delta
        self.assertEqual(self.relabeled_bounding_box, computed_relabeled_bounding_box)


class TestBoundingBoxIOU(TestCase):
    def setUp(self) -> None:
        self.box_a = BoundingBox('test', 'test', 0.0, 0.0, 1.0, 1.0)
        self.box_b = BoundingBox('test', 'test', 0.5, 0.5, 1.5, 1.5)

    def test_iou_with_same_boxes(self):
        self.assertEqual(1.0, self.box_a.iou(self.box_a))

    def test_iou_with_different_boxes(self):
        self.assertAlmostEqual(1 / 12, self.box_a.iou(self.box_b))
