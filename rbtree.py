import logging
from enum import Enum, unique
import sys

####################
# Global variables #
####################
logger = logging.getLogger("datastructures.rbtree")

#Create base color Enum (note: this could be handled with a boolean value; I want an explicit readable red/black type)
@unique
class node_color(Enum):
    BLACK = 0
    RED = 1


class rbtree_node:
    def __init__(self, value, color = node_color.BLACK, parent = None):
        self.value = value
        self.color = color
        self.parent = parent
        self.left_child = None
        self.right_child = None

    
    def search(self, root, value):

        #if there is no root, or the root has the value, return root
        if root == None or root.value == value:
            logger.debug("Either root value equals value, or there is no root; returning root.")
            return root
        #recurse through left tree if value less than root.value
        elif value < root.value:
            logger.debug("Value {} less than root value {}; recursing through left subtree".format(value, root.value))
            return search(root.left_child, value)
        #otherwise, recurse through right tree (value greater than root.value)
        else:
            logger.debug("Value {} greater than root value {}; recursing through right subtree".format(value, root.value))
            return search(root.right_child, value)
