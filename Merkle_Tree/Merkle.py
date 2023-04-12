from typing import List
import typing 
import hashlib #to be used to perform the hashing function

class Node:
    def __init__(self,left,right,value:str) -> None:
        self.left: Node = left #here left of the node is also of type Node
        self.right: Node = right #here right of the node is also of type Node
        self.value=value #assigning the value of the node

    @staticmethod #so that it can be called without making an object
    def hash(value:str)->str:
        return hashlib.sha256(value.encode('utf-8')).hexdigest()
    
    @staticmethod #so that it can be called without making an object
    def double_hash(value:str)->str:
        return Node.hash(Node.hash(value))
    #we perform double hashing for extra security, and on every node as we want to make even number of nodes due to it being a binary tree    
class merkle:
    def __init__(self,values:List[str])->None:
        self.buildTree(values) #we call the buildTree function to make a merkle tree 

    def buildTree(self, values: List[str])-> None: #it takes the string values in a list 

        Leaves: List[Node] = [Node(None, None, Node.doubleHash(e)) for e in values]
        #here we perform double hashing on each value in the list of nodes
        if len(Leaves) % 2 == 1: #we checl if there are odd or even number of leaves
            Leaves.append(Leaves[-1:][0]) #if there are odd numbers, we will make it even by duplicating the last element
        self.root: Node = self.buildTreeRec(Leaves) #here we call the buildTree rec function

    def buildTreeRec(self, nodes: List[Node])-> Node:
        #this will take in the merkle tree and then build the left and right halves of it
        #it will then return the tree

        half: int = len(nodes) // 2 #we first divide the tree into 2 halves

        if len(nodes) == 2: #if there are just 2 nodes, then we just perform hashing on both nodes
            return Node(nodes[0], nodes[1], Node.doubleHash(nodes[0].value + nodes[1].value))
        #incase there are nodes > 2, we then slice the list into two parts
        left: Node = self.__buildTreeRec(nodes[:half]) # 0th index to half
        right: Node = self.__buildTreeRec(nodes[half:]) # half to last index
        value: str = Node.doubleHash(left.value + right.value) # we then perform the hashing on both halves' values
        return Node(left, right, value) #we then return these hashed halaves of the tree

    def printTree(self)-> None: #this prints the tree's root and halves
        self.printTreeRec(self.root)
    
    def printTreeRec(self, node)-> None: #this prints the tree and its halves (left and right)
        if node != None:
            print(node.value)
            self.printTreeRec(node.left)
            self.printTreeRec(node.right)

    def getRootHash(self)-> str: #here we are receiving the hash of the root of the tree
        return self.root.value


    def test()-> None:
        elems = ["Hello", "mister", "Merkle"]
        mtree = merkle(elems)
        print(mtree.getRootHash())