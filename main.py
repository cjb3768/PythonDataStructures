import logging
import sys
from rbtree import *

####################
# Global variables #
####################
logger = logging.getLogger("datastructures.main")

def main():
    #set logging level to output all messages of DEBUG level or higher
    logging.basicConfig(level=logging.DEBUG)

    tree = rbtree()
    logger.debug("Inserting node with value 10.")
    tree.insert(15)
    tree.print_inorder()
    logger.debug("Inserting node with value 2.")
    tree.insert(2)
    logger.debug("Inserting node with value 19.")
    tree.insert(19)
    tree.print_inorder()
    #test recolor with red uncle
    logger.debug("Inserting node with value 1")
    tree.insert(1)
    tree.print_inorder()
    logger.debug("Inserting nodes with values 3 and 4.")
    tree.insert(3)
    tree.insert(4)
    tree.print_inorder()
    logger.debug("Inserting node with value 5.")
    tree.insert(5)
    tree.print_inorder()
    #test left-right and left-left rotation
    logger.debug("Inserting node with value 6.")
    tree.insert(6)
    tree.print_inorder()
    #test right-right rotation
    logger.debug("Inserting node with value 9")
    tree.insert(9)
    tree.print_inorder()
    #test right-left rotation
    logger.debug("Inserting nodes with values 13 and 10")
    tree.insert(13)
    tree.print_inorder()
    tree.insert(10)
    tree.print_inorder()

    #test search
    #searching for an invalid entry should print out "None"
    print(tree.search(27, tree.root))
    #searching for a valid entry should print out it's value and color
    print(tree.search(13, tree.root))

if __name__ == "__main__":
    main()
