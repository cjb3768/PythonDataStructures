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
        #recolor and rotate tree as necessary to rebalance
        self.insertion_rebalance(node)


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


    def find_minima(self, node):
        #find the minimum value of a tree starting at a given node
        if node.left_child is not None:
            return self.find_minima(node.left_child)
        else:
            return node


    def find_maxima(self, node):
        #find the maximum value of a tree starting at a given node
        if node.right_child is not None:
            return self.find_maxima(node.right_child)
        else:
            return node


    def find_predecessor(self, node):
        #if a node has a left child, it's predecessor is the maximum value of its left subtree
        if node.left_child is not None:
            return self.find_maxima(node.left_child)
        #otherwise, if a predecessor exists, it is the lowest node in the tree y such that it is an ancestor of our node whose right child is also an ancestor of our node
        else:
            x = node
            y = node.parent
            while y is not None and y.left_child == x:
                x = y
                y = y.parent
            return y


    def find_successor(self, node):
        #if a node has a right child, it's successor is the minimum value of its right subtree
        if node.right_child is not None:
            return self.find_minima(node.right_child)
        #otherwise, if a successor exists, it is the lowest node in the tree y such that it is an ancestor of our node whose left child is also an ancestor of our node
        else:
            x = node
            y = node.parent
            while y is not None and y.right_child == x:
                x = y
                y = y.parent
            return y #returns none if there is no successor, or y if there is one


    def transplant(self, node, child):
        #reseat child in place of node in a tree structure
        if node.parent is None:
            #node was the root; make child the root
            self.root = child
        else:
            #determine which child of node.parent node was and reassign that pointer to child
            if node.parent.left_child == node:
                node.parent.left_child = child
            else:
                node.parent.right_child = child
        if child is not None:
            #if child exists, connect it to node.parent
            child.parent = node.parent


    def delete(self, value, root=None):
        if root is None:
            root = self.root

        #find node from value
        node = self.search(value, root)
        #return if no such node
        if node is None:
            logger.debug("No node with value {} found. Deletion failed".format(value))
            return

        #back up node; we will need it for position information and rebalancing
        working_node = node
        working_node_original_color = node.color

        #determine course of action based on what children node has
        #node has no left child
        if node.left_child is None:
            child = node.right_child
            self.transplant(node, node.right_child)
        #node has no right child, but has a left child
        elif node.right_child is None:
            child = node.left_child
            self.transplant(node, node.left_child)
        #node has two children
        else:
            #get successor to node
            working_node = self.find_minima(node.right_child)
            working_node_original_color = working_node.color
            child = working_node.right_child

            if working_node.parent == node:
                if child is not None:
                    child.parent = working_node
            else:
                self.transplant(working_node, working_node.right_child)
                working_node.right_child = node.right_child
                working_node.right_child.parent = working_node
            self.transplant(node, working_node)
            working_node.left_child = node.left_child
            working_node.left_child.parent = working_node
            working_node.color = node.color
        if working_node_original_color == node_color.BLACK:
            #call recoloring function
            logger.debug("We deleted or moved a black node; we need to do stuff here")
            self.deletion_rebalance(child)
        #
        # #determine course of action based on whether node is a leaf, has one child, or has two children
        # if node.left_child is None and node.right_child is None:
        #     #node is a leaf
        #     #unlink node from its parent if it has one
        #     if node.parent is not None:
        #         if node.parent.left_child == node:
        #             node.parent.left_child = None
        #         else:
        #             node.parent.right_child = None
        #     else:
        #         #if node has no parent, it is a root; set self.root to None
        #         self.root = None
        #
        #
        # elif (node.left_child is not None and node.right_child is None) or (node.left_child is None and node.right_child is not None):
        #     #node has one child; swap child into node's position and delete node
        #     if node.left_child is not None:
        #         child = node.left_child
        #     else:
        #         child = node.right_child
        #
        #     #link child to node's parent if it has one
        #     if node.parent is not None:
        #         if node.parent.left_child == node:
        #             node.parent.left_child = child
        #         else:
        #             node.parent.right_child = child
        #     else:
        #         #if node has no parent, it is a root; set self.root to the child
        #         self.root = child
        #
        #     child.parent = node.parent
        # else:
        #     #node has two children; need to replace the value at the root with an inorder successor
        #     #find minima of node's right child (recurse through left children until you hit a leaf); this is node's inorder successor
        #     inorder_successor = self.find_successor(node.right_child)
        #     #set successor's parent's left child to None, delinking it from successor
        #     inorder_successor.parent.left_child = None
        #     #set sucessor's left and right children to node's left and right children
        #     inorder_successor.left_child = node.left_child
        #     node.left_child.parent = inorder_successor
        #     inorder_successor.right_child = node.right_child
        #     node.right_child.parent = inorder_successor
        #     #if node has a parent, link m to it's parent; otherwise make it the root.
        #     if node.parent is not None:
        #         if node.parent.left_child == node:
        #             node.parent.left_child = inorder_successor
        #         else:
        #             node.parent.right_child = inorder_successor
        #     else:
        #         #if node has no parent, it is a root; set self.root to successor
        #         self.root = inorder_successor
        # #handle recoloring


    def insertion_rebalance(self, node):
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
                    #call insertion_rebalance on grandparent
                    logger.debug("Calling rebalance again: node is {}, parent is {}, grandparent is {}, uncle is {}".format(node, parent, grandparent, uncle))
                    #self.print_inorder()
                    self.insertion_rebalance(grandparent)
                #if new node's uncle is black or doesn't exist (if it doesn't exist, we need to rotate)
                else:
                    #rotate appropriately (see left-left, left-right, right-left, and right-right cases)
                    logger.debug("Calling rotation: node is {}, parent is {}, grandparent is {}, uncle is {}".format(node, parent, grandparent, uncle))
                    #self.print_inorder()
                    self.insertion_rotation(node)


    def deletion_rebalance(self, node):
        pass


    def left_rotate(self, node):
        #rotate node up and to the left
        #creating helper for legibility
        parent = node.parent

        #link node's left child as parent's right child
        parent.right_child = node.left_child
        if node.left_child is not None:
            node.left_child.parent = parent

        #link parent's parent to node
        self.transplant(parent, node)

        #link parent as node's left child
        node.left_child = parent
        parent.parent = node


    def right_rotate(self, node):
        #rotate node up and to the right
        #creating helper for legibility
        parent = node.parent

        #link node's right child as parent's left child
        parent.left_child = node.right_child
        if node.right_child is not None:
            node.right_child.parent = parent

        #link parent's parent to node
        self.transplant(parent, node)

        #link parent as node's right child
        node.right_child = parent
        parent.parent = node


    def insertion_rotation(self, node):
        #create some helper variables to clear up code
        parent = node.parent
        grandparent = parent.parent
        logger.debug("Attempting rotation: node is {}, parent is {}, grandparent is {}".format(node, parent, grandparent))

        #check to see which case we are in
        if parent == grandparent.left_child:
            #we are in one of the left cases
            if node == parent.left_child:
                #left-left
                logger.debug("Left-Left case, need a right rotation and recoloring")
                #call appropriate rotation
                self.right_rotate(parent)

                #flip colors of parent and grandparent
                parent.flip_color()
                grandparent.flip_color()
            else:
                #left-right
                logger.debug("Left-Right case, need a left rotation then call a left-left case")
                #call appropriate rotation
                self.left_rotate(node)

                #call again on parent to run left-left
                logger.debug("Calling insertion_rotation again on parent: node is {}, parent is {}, grandparent is {}".format(node, parent, grandparent))
                self.insertion_rotation(parent)
        else:
            #we are in one of the right cases
            if node == parent.left_child:
                #right-left
                logger.debug("Right-Left case, need a right rotation then call a right-right case")
                #call appropriate rotation
                self.right_rotate(node)

                #call again on parent to run right-right
                logger.debug("Calling insertion_rotation again on parent: node is {}, parent is {}, grandparent is {}".format(node, parent, grandparent))
                self.insertion_rotation(parent)
            else:
                #right-right
                logger.debug("Right-Right case, need a left rotation and recoloring")
                #call appropriate rotation
                self.left_rotate(parent)

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
