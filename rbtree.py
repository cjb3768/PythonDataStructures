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

    
    def rotate(self, node):
        #create some helper variables to clear up code
        parent = node.parent
        grandparent = parent.parent
        temp_node = None
        
        #check to see which case we are in
        if node == parent.left_child:
            #we are in one of the left cases
            if parent = grandparent.left_child:
                #left-left
                #temporarily store right child of parent
                temp_node = parent.right_child

                #rotate parent up
                #set parent's right child to grandparent
                parent.right_child = grandparent
                #set parent's parent to grandparent's parent
                parent.parent = grandparent.parent
                #set grandparent's parent to parent
                grandparent.parent = parent
                #link parent to it's new parent (add None check, in case of root?)
                if grandparent == parent.parent.left_child:
                    parent.parent.left_child = parent
                else:
                    parent.parent.right_child = parent

                #reattach temp_node
                #set grandparent's left child to temporary node
                grandparent.left_child = temp_node
                #set temp_node's parent to grandparent
                temp_node.parent = grandparent

                #flip colors of parent and grandparent
                parent.flip_color()
                grandparent.flip_color()
            else:
                #left-right
                #temporarily store node's left child
                temp_node = node.left_child
                #set node's left child to parent
                node.left_child = parent
                #set parent's parent to node
                parent.parent = node
                #set node's parent to grandparent
                node.parent = grandparent
                #set grandparent's left child to node
                grandparent.left_child = node
                #set parent's right child to temp_node
                parent.right_child = temp_node
                #set temp_node's parent to parent
                temp_node.parent = parent
                #call again on parent to run left-left
                self.rotate(parent)
        else:
            #we are in one of the right cases
            if parent = grandparent.left_child:
                #right-left
                #temporarily store node's right child
                temp_node = node.right_child
                #set node's right child to parent
                node.right_child = parent
                #set parent's parent to node
                parent.parent = node
                #set node's parent to grandparent
                node.parent = grandparent
                #set grandparent's right child to node
                grandparent.right_child = node
                #set parent's left child to temp_node
                parent.left_child = temp_node
                #set temp_node's parent to parent
                temp_node.parent = parent
                #call again on parent to run right-right
                self.rotate(parent)
            else:
                #right-right
                #temporarily store left child of parent
                temp_node = parent.left_child

                #rotate parent up
                #set parent's left child to grandparent
                parent.left_child = grandparent
                #set parent's parent to grandparent's parent
                parent.parent = grandparent.parent
                #set grandparent's parent to parent
                grandparent.parent = parent
                #link parent to it's new parent
                if grandparent == parent.parent.left_child:
                    parent.parent.left_child = parent
                else:
                    parent.parent.right_child = parent

                #reattach temp_node
                #set grandparent's right child to temporary node
                grandparent.right_child = temp_node
                #set temp_node's parent to grandparent
                temp_node.parent = grandparent


                #flip colors of parent and grandparent
                parent.flip_color()
                grandparent.flip_color()


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
