from .node import Node
from copy import deepcopy
from .tree_exceptions import *


class Binary_Search_Tree(object):
    """Documentation for Binary_Search_Tree

    """
    def __init__(self, tree=None, deep=None):
        super(Binary_Search_Tree, self).__init__()
    
        self._nodes = {}
        self._root = None

        if tree:
            if deep:
                self.root = deepcopy(tree.root)
                self.nodes = deepcopy(tree.nodes)
            else:
                self.root = tree.root
                self.nodes = tree.nodes

    def __len__(self):
        return len(self.nodes)

    def __getitem__(self, node_id):
        try:
            return self.nodes[node_id]
        except KeyError:
            raise TreeNodeNonExistError("Node '%s' is not in the tree" % key)

    def __setitem__(self, key, item):
        self.nodes.update({key: item})

    def __str__(self):
        raise Exception('Not Implemented Function')
    
    @property
    def root(self):
        return self._root

    @root.setter
    def root(self, val):
        self._root = val if val else None

    @property
    def nodes(self):
        return self._nodes

    @nodes.setter
    def nodes(self, val):
        self._nodes = val

    def create_empty_node(self):
        node_empty = Node()
        self.nodes.update({node_empty.identifier, node_empty})
        return node_empty

    async def inorder_tree_walk(self, node):
        if node != None:
            await inorder_tree_walk(node.left_node)
            yield node
            await inorder_tree_walk(node.right_node)
        
    
    def tree_search(self, node=self.root, val):
        if node == None or node.compare_value == val:
            return node
        elif val < node.compare_value:
            tree_search(node.left_node, val)
        else:
            tree_search(node.right_node, val)

    def iterative_tree_search(self, node=self.root, val):
        while node != None and node.compare_value!=val:
            if val < node.compare_value:
                node = node.left_node
            else:
                node = node.right_node
        return node

    def min_tree(self,node=self.root):
        while node.left_node!=None:
            node = node.left_node
        return node.compare_value

    def max_tree(self, node=self.root):
        while node.right_node != None:
            node = node.right_node
        return node.compare_value

    def tree_successor(self, node):
        if node.right_node != None:
            return min_tree(node.right_node)
        y = node.parent_node
        while y != None and node == y.right_node:
            
    def tree_insert(self, val):
        new_node = self.create_empty_node()
        new_node.compare_value = val
        current_root = self.root
        cursor = None
        while current_root != None:
            cursor = current_root
            if new_node < current_root:
                current_root = current_root.left_node
            else:
                current_root = current_root.right_node
        new_node.parent_node = cursor

        # In the case that the Tree is Empty
        if cursor == None:
            self.root = new_node
        elif new_node < cursor:
            cursor.left_node = new_node
        else:
            cursor.right_node = new_node

    def deletion(self, )
