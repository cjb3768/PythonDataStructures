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

    
