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
    def __init__(self, value, color = node_color.RED, parent = None):
        self.value = value
        self.color = color
        self.parent = parent
        self.left_child = None
        self.right_child = None

    def flip_color(self):
        if self.color == node_color.BLACK:
            self.color = node_color.RED
        else:
            self.color = node_color.BLACK


class rbtree:
    def __init__(self):
        #self.root = rbtree_node(value, node_color.BLACK, None)
        self.root = None
        self.max = None
        self.min = None
        self.black_height = None


    def insertion(self, root=self.root, value):
        #create node
        node = rbtree_node(value)
        #traverse through the tree and insert new node as a leaf
        self.bst_insertion(root, node)
        #recolor and rotate tree as necessary to balance
        self.balance_tree(node)


    def bst_insertion(self, root, node):
        #insert at root if there is none
        if root is None:
            root = node
            self.root = node
        else:
            if node.value < root.value:
                #working on left half of tree
                if root.left_child is None:
                    root.left_child = node
                    node.parent = root
                else:
                    self.bst_insertion(root.left_child, node)
            else:
                #working on right half of tree
                if root.right_child is None:
                    root.right_child = node
                    node.parent = root
                else:
                    self.bst_insertion(root.right_child, node)


    def balance_tree(self, node):
        #Attempt to balance tree by recoloring first, then rotating if needed
        #if node is root, make it black
        if node is self.root:
            node.color = node_color.BLACK
        #node is not root
        else:
            #if node's parent is red
            if node.parent.color == node_color.RED:
                #create some helper variables to help with recoloring
                parent = node.parent
                grandparent = node.parent.parent
                if parent == grandparent.left_child:
                    uncle = grandparent.right_child
                else:
                    uncle = grandparent.left_child

                #if node's uncle is red
                if parent.color == uncle.color:
                    #make parent and uncle black
                    uncle.flip_color()
                    parent.flip_color()
                    #make grandparent red
                    grandparent.flip_color()
                    #call balance_tree on grandparent
                    balance_tree(grandparent)
                #if new node's uncle is black
                else:
                    #rotate appropriately (see left-left, left-right, right-left, and right-right cases)
                    self.rotate(node)


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
            logger.debug("Either root value equals value, or there is no root; returning root (or lack thereof).")
            return root
        #recurse through left tree if value less than root.value
        elif value < root.value:
            logger.debug("Value {} less than root value {}; recursing through left subtree".format(value, root.value))
            return search(root.left_child, value)
        #otherwise, recurse through right tree (value greater than root.value)
        else:
            logger.debug("Value {} greater than root value {}; recursing through right subtree".format(value, root.value))
            return search(root.right_child, value)
