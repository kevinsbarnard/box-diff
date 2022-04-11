import json
from unittest import TestCase
from uuid import UUID, uuid4

from random import randint

from boxdiff.models.core import BoundingBox


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
