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

    def __str__(self):
        return "({},{})".format(self.value, self.color.name)


class rbtree:
    def __init__(self):
        #self.root = rbtree_node(value, node_color.BLACK, None)
        self.root = None
        self.max = None
        self.min = None
        self.black_height = None


    def insert(self, value, root=None):
        if root is None:
            root = self.root
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

                logger.debug("Attempting rebalance: node is {}, parent is {}, grandparent is {}, uncle is {}".format(node, parent, grandparent, uncle))

                #if node's uncle exists and is red
                if uncle is not None and parent.color == uncle.color:
                    #make parent and uncle black
                    uncle.flip_color()
                    parent.flip_color()
                    #make grandparent red
                    grandparent.flip_color()
                    #call balance_tree on grandparent
                    logger.debug("Calling rebalance again: node is {}, parent is {}, grandparent is {}, uncle is {}".format(node, parent, grandparent, uncle))
                    #self.print_inorder()
                    self.balance_tree(grandparent)
                #if new node's uncle is black or doesn't exist (if it doesn't exist, we need to rotate)
                else:
                    #rotate appropriately (see left-left, left-right, right-left, and right-right cases)
                    logger.debug("Calling rotation: node is {}, parent is {}, grandparent is {}, uncle is {}".format(node, parent, grandparent, uncle))
                    #self.print_inorder()
                    self.rotate(node)


    def rotate(self, node):
        #create some helper variables to clear up code
        parent = node.parent
        grandparent = parent.parent
        temp_node = None
        logger.debug("Attempting rotation: node is {}, parent is {}, grandparent is {}, temp_node is {}".format(node, parent, grandparent, temp_node))

        #check to see which case we are in
        if parent == grandparent.left_child:
            #we are in one of the left cases
            if node == parent.left_child:
                #left-left
                logger.debug("Left-Left rotation")
                #temporarily store right child of parent
                logger.debug("STEP 1 - Temporarily store parent's right child")
                temp_node = parent.right_child
                logger.debug("temp_node is {}, parent's right child is {}".format(temp_node, parent.right_child))
                #rotate parent up
                #set parent's right child to grandparent
                logger.debug("STEP 2 - Set parent's right child to grandparent")
                parent.right_child = grandparent
                #set parent's parent to grandparent's parent
                parent.parent = grandparent.parent
                #link parent to its new parent
                if parent.parent is not None:
                    if parent.parent.left_child is not None and grandparent == parent.parent.left_child:
                        parent.parent.left_child = parent
                    elif parent.parent.right_child is not None and grandparent == parent.parent.right_child:
                        parent.parent.right_child = parent
                else:
                    #if the parent has no parent now, it is the root
                    self.root = parent

                #set grandparent's parent to parent
                grandparent.parent = parent

                #set grandparent's left child to temporary node
                grandparent.left_child = temp_node
                #set temp_node's parent to grandparent if temp_node is not None
                if temp_node is not None:
                    temp_node.parent = grandparent

                #flip colors of parent and grandparent
                parent.flip_color()
                grandparent.flip_color()
                #self.print_inorder()
                #print("____")
            else:
                #left-right
                logger.debug("Left-Right rotation")
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
                #set temp_node's parent to parent if temp_node is not None
                if temp_node is not None:
                    temp_node.parent = parent

                #call again on parent to run left-left
                logger.debug("Calling rotation again on parent: node is {}, parent is {}, grandparent is {}, temp_node is {}".format(node, parent, grandparent, temp_node))
                #self.print_inorder()
                self.rotate(parent)
        else:
            #we are in one of the right cases
            if node == parent.left_child:
                #right-left
                logger.debug("Right-Left rotation")
                #temporarily store node's right child
                #logger.debug("STEP 1 - store node's right child in temp")
                temp_node = node.right_child
                #logger.debug("node is {}, node's parent is {}, node's right child is {}, parent is {}, parent's left_child is {}, parent's parent is {}, grandparent is {}, grandparent's right child is {}, temp_node is {}".format(node, node.parent, node.right_child, parent, parent.left_child, parent.parent, grandparent, grandparent.right_child, temp_node))
                #set node's right child to parent
                #logger.debug("STEP 2 - set parent as node's right child")
                node.right_child = parent
                #logger.debug("node is {}, node's parent is {}, node's right child is {}, parent is {}, parent's left_child is {}, parent's parent is {}, grandparent is {}, grandparent's right child is {}, temp_node is {}".format(node, node.parent, node.right_child, parent, parent.left_child, parent.parent, grandparent, grandparent.right_child, temp_node))
                #set parent's parent to node
                #logger.debug("STEP 3 - set parent's parent to node")
                parent.parent = node
                #logger.debug("node is {}, node's parent is {}, node's right child is {}, parent is {}, parent's left_child is {}, parent's parent is {}, grandparent is {}, grandparent's right child is {}, temp_node is {}".format(node, node.parent, node.right_child, parent, parent.left_child, parent.parent, grandparent, grandparent.right_child, temp_node))
                #set node's parent to grandparent
                #logger.debug("STEP 4 - set node's parent to grandparent")
                node.parent = grandparent
                #logger.debug("node is {}, node's parent is {}, node's right child is {}, parent is {}, parent's left_child is {}, parent's parent is {}, grandparent is {}, grandparent's right child is {}, temp_node is {}".format(node, node.parent, node.right_child, parent, parent.left_child, parent.parent, grandparent, grandparent.right_child, temp_node))
                #set grandparent's right child to node
                #logger.debug("STEP 5 - set grandparent's right child to node")
                grandparent.right_child = node
                #logger.debug("node is {}, node's parent is {}, node's right child is {}, parent is {}, parent's left_child is {}, parent's parent is {}, grandparent is {}, grandparent's right child is {}, temp_node is {}".format(node, node.parent, node.right_child, parent, parent.left_child, parent.parent, grandparent, grandparent.right_child, temp_node))
                #set parent's left child to temp_node
                #logger.debug("STEP 6 - set parent's left child to temp")
                parent.left_child = temp_node
                #logger.debug("node is {}, node's parent is {}, node's right child is {}, parent is {}, parent's left_child is {}, parent's parent is {}, grandparent is {}, grandparent's right child is {}, temp_node is {}".format(node, node.parent, node.right_child, parent, parent.left_child, parent.parent, grandparent, grandparent.right_child, temp_node))
                #set temp_node's parent to parent if temp_node is not None
                if temp_node is not None:
                    #logger.debug("STEP 7 (optional) - set temp's parent to parent")
                    temp_node.parent = parent
                    #logger.debug("node is {}, node's parent is {}, node's right child is {}, parent is {}, parent's left_child is {}, parent's parent is {}, grandparent is {}, grandparent's right child is {}, temp_node is {}, temp_node's parent is {}".format(node, node.parent, node.right_child, parent, parent.left_child, parent.parent, grandparent, grandparent.right_child, temp_node, temp_node.parent))

                #call again on parent to run right-right
                logger.debug("Calling rotation again on parent: node is {}, parent is {}, grandparent is {}, temp_node is {}".format(node, parent, grandparent, temp_node))
                #self.print_inorder()
                self.rotate(parent)
            else:
                #right-right
                logger.debug("Right-Right rotation")
                #temporarily store left child of parent
                temp_node = parent.left_child

                #rotate parent up
                #set parent's left child to grandparent
                parent.left_child = grandparent
                #set parent's parent to grandparent's parent
                parent.parent = grandparent.parent
                #link parent to its new parent
                if parent.parent is not None:
                    if parent.parent.left_child is not None and grandparent == parent.parent.left_child:
                        parent.parent.left_child = parent
                    elif parent.parent.right_child is not None and grandparent == parent.parent.right_child:
                        parent.parent.right_child = parent
                else:
                    #if parent has no parent, it is now the root
                    self.root = parent

                #set grandparent's parent to parent
                grandparent.parent = parent

                #set grandparent's right child to temporary node
                grandparent.right_child = temp_node
                #set temp_node's parent to grandparent if temp_node is not None
                if temp_node is not None:
                    temp_node.parent = grandparent

                #flip colors of parent and grandparent
                parent.flip_color()
                grandparent.flip_color()


    def search(self, value, root):

        #if there is no root, or the root has the value, return root
        if root is None or root.value == value:
            logger.debug("Either root value equals value, or there is no root; returning root (or lack thereof).")
            return root
        #recurse through left tree if value less than root.value
        elif value < root.value:
            logger.debug("Value {} less than root value {}; recursing through left subtree".format(value, root.value))
            return self.search(value, root.left_child)
        #otherwise, recurse through right tree (value greater than root.value)
        else:
            logger.debug("Value {} greater than root value {}; recursing through right subtree".format(value, root.value))
            return self.search(value, root.right_child)


    def print_inorder(self, root=None, offset=""):
        #traverse and print the tree via an inorder traversal
        if root is None:
            root = self.root

        if root.left_child is not None:
            self.print_inorder(root.left_child, offset+"- ")

        print("{}({},{})".format(offset,root.value, root.color.name))

        if root.right_child is not None:
            self.print_inorder(root.right_child, offset+"- ")
