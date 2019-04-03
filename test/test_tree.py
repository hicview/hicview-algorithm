import unittest
import sys
sys.path.append('..')
from server.resource_map.domain.algorithms import Node
from copy import deepcopy

class TestNode(unittest.TestCase):
    def test_node_construct(self):
        a = Node(compare_value=1)
        print(a)
        self.assertEqual(a.compare_value, 1)
        b = Node()
        self.assertEqual(b.compare_value, b.identifier)

    def test_node_parent(self):
        a = Node()
        b = Node()
        a.update_parent_node(b)
        self.assertEqual(a.parent_node_id, b.identifier)
        self.assertEqual(a.parent_node, b)
        
    def test_node_left(self):
        a = Node()
        b = Node()
        a.update_left_node(b)
        self.assertEqual(a.left_node_id, b.identifier)

    def test_node_right(self):
        a = Node()
        b = Node()
        a.update_right_node(b)
        self.assertEqual(a.right_node_id, b.identifier)

    def test_node_additional_info(self):
        a = Node(compare_value=1, additional_info=2)
        print(a)
        self.assertEqual(a.additional_info, 2)

    def test_node_data(self):
        a = Node(data={'1': 2, '2': 3})
        self.assertEqual(a.data, {'1': 2, '2': 3})

    def test_node_json(self):
        a = Node(data={'1': 2, '2': 3})
        b = {
            'identifier': str(a.identifier),
            'compare_value': str(a.identifier),
            'additional_info': None,
            'parent_node': None,
            'left_node': None,
            'right_node': None,
            'data': a.data
        }
        self.assertEqual(a.json_dict, b)

    def test_node_equal(self):
        a = Node(data={'1': 2, '2': 3})
        b = Node()
        b.json_dict = a.json_dict
        self.assertEqual(a == b, True)


    def test_node_deepcopy(self):
        a = Node(data={'1': 2, '2': 3})
        b = deepcopy(a)
        self.assertEqual(a, b)
