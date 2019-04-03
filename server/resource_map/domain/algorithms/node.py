
import uuid
import copy

class Node(object):
    """
    Node Class: Base Node for binary search tree
    """
    def __init__(self, compare_value=None, identifier=None, additional_info=None, data=None ):
        self._identifier = None
        self._set_identifier(identifier)

        if compare_value is None:
            self._compare_value = self._identifier
        else:
            self._compare_value = compare_value

        
        self._additional_info = additional_info if additional_info else None
            
        self._parent_node = None
        self._left_node = None
        self._right_node = None
        self._parent_node_id = None
        self._left_node_id = None
        self._right_node_id = None
        
        self._data = copy.deepcopy(data) if (data != None) else data

    def __lt__(self, other):
        return self.compare_value < other.compare_value

    def __eq__(self, other):
        attr = ["compare_value",
                "additional_info",
                "parent_node",
                "left_node",
                "right_node",
                "data"]
        for i in attr:
            if getattr(self,i,None) != getattr(other,i,None):
                return False
        return True

    def _set_identifier(self, _id):
        if _id:
            self._identifier = _id
        else:
            self._identifier = str(uuid.uuid1())


    @property
    def parent_node_id(self):
        return self._parent_node_id

    @parent_node_id.setter
    def parent_node_id(self, _id):
        if _id:
            self._parent_node_id = _id
            
    @property
    def parent_node(self):
        return self._parent_node

    @parent_node.setter
    def parent_node(self, _node):
        if _node:
            self._parent_node = _node
            self._parent_node_id = _node._identifier

    @property
    def right_node_id(self):
        return self._right_node_id

    @right_node_id.setter
    def right_node_id(self, _id):
        if _id:
            self._right_node_id = _id
            
    @property
    def right_node(self):
        return self._right_node

    @right_node.setter
    def right_node(self, _node):
        if _node:
            self._right_node = _node
            self._right_node_id = _node._identifier


    @property
    def left_node_id(self):
        return self._left_node_id

    @left_node_id.setter
    def left_node_id(self, _id):
        if _id:
            self._left_node_id = _id
            
    @property
    def left_node(self):
        return self._left_node

    @left_node.setter
    def left_node(self, _node):
        if _node:
            self._left_node = _node
            self._left_node_id = _node._identifier
            
    @property
    def identifier(self):
        return self._identifier

    @identifier.setter
    def identifier(self, val):
        if val:
            self._set_identifier = val
        else:
            raise Warning('node ID should be some value')

    @property
    def compare_value(self):
        return self._compare_value
    
    @compare_value.setter
    def compare_value(self, val):
        if val is not None:
            self._compare_value = val

    @property
    def additional_info(self):
        return self._additional_info

    @additional_info.setter
    def additional_info(self, adinfo):
        if adinfo:
            self._additional_info = adinfo.deepcopy()

    @property
    def data(self):
        return self._data
    
    @data.setter
    def data(self, val):
        self._data = val if (val != None) else None    

    @property
    def json_dict(self):
        attr = ["identifier",
                "compare_value",
                "additional_info",
                "parent_node",
                "left_node",
                "right_node",
                "data"]
        return {k:getattr(self,k) for k in attr }
    
    @json_dict.setter
    def json_dict(self, js):
        for k, v in js.items():
            setattr(self, k, copy.deepcopy(v))
    
    def is_leaf(self):
        return (self._left_node == None) and (self._right_node == None)

    def is_root(self):
        return self._parent_node == None

    def update_parent_node(self, node):
        if node:
            self.parent_node = node

    def update_left_node(self, node):
        if node:
            self.left_node = node

    def update_right_node(self, node):
        if node:
            self.right_node = node

    def __repr__(self):
        name = self.__class__.__name__
        kwargs = [
            "compare_value={0}".format(self.compare_value),
            "identifier={0}".format(self.identifier),
            "additional_info={0}".format(getattr(self, '_additional_info', None)),
            "data={0}".format(self.data),
        ]
        return "%s(%s)" % (name, ", ".join(kwargs))
        
