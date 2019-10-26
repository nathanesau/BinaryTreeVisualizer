import unittest
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Node:
    def __init__(self):
        self.p = None
        self.key = 0
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self._root = None

    def insert(self, a):
        tmp = Node()
        tmp.key = a
        tmp.left = None
        tmp.right = None

        if not self._root:
            tmp.p = None
            self._root = tmp
        else:
            cElem = self._root
            parent = None
            while cElem:
                parent = cElem
                cElem = cElem.left if a < cElem.key else cElem.right
            tmp.p = parent
            if a < parent.key:
                parent.left = tmp
            else:
                parent.right = tmp
    
    def _preorderWalk(self, p):
        if p:
            print(str(p.key) + " ", end="")
            self._preorderWalk(p.left)
            self._preorderWalk(p.right)
        
    def preorderWalk(self):
        print("Preorder walk: ")
        self._preorderWalk(self._root)
        print("\n", end="")
    
    def _postorderWalk(self, p):
        if p:
            self._postorderWalk(p.left)
            self._postorderWalk(p.right)
            print(str(p.key) + " ", end="")

    def postorderWalk(self):
        print("Postorder walk: ", end="")
        self._postorderWalk(self._root)
        print("\n", end="")

    def _inorderWalk(self, p):
        if p:
            self._inorderWalk(p.left)
            print(str(p.key) + " ", end="")
            self._inorderWalk(p.right)
    
    def inorderWalk(self):
        print("Inorder walk: ", end="")
        self._inorderWalk(self._root)
        print("\n", end="")
    
    def _findElem(self, val, p):
        if p:
            if val is p.key:
                return p
            if val < p.key:
                return self._findElem(val, p.left)
            else:
                return self._findElem(val, p.right)
        else:
            return None

    def findElem(self, val):
        return self._findElem(val, self._root)

    def _findSuccessor(self, val):
        startNode = self.findElem(val)
        parent = startNode
        startNode = startNode.right
        while startNode and startNode.left:
            parent = startNode
            startNode = startNode.left
        return startNode
    
    def _deleteNode(self, p):
        q = None
        r = None
        if not p.left or not p.right:
            q = p
        else:
            q = self._findSuccessor(p.key)

        if q.left:
            r = q.left
        else:
            r = q.right

        if r:
            r.p = q.p

        if not q.p:
            self._root = r
        elif q is q.p.left:
            q.p.left = r
        else:
            q.p.right = r

        if q != p:
            p.key = q.key


    def deleteNode(self, val):
        self._deleteNode(self.findElem(val))

    def _countLevels(self, p):
        if not p:
            return 0
        h1 = 0 if not p.left else self._countLevels(p.left)
        h2 = 0 if not p.right else self._countLevels(p.right)
        return max(h1, h2) + 1
        
    def countLevels(self):
        return self._countLevels(self._root)
    
    def _countNodes(self, p):
        if not p:
            return 0
        else:
            return self._countNodes(p.left) + self._countNodes(p.right) + 1

    def countNodes(self):
        return self._countNodes(self._root)
    
    def _countLeftNodes(self, p):
        if not p:
            return 0
        else:
            return self._countNodes(p.left) + self._countNodes(p.right) + (1 if p.left and not p.right else 0)

    def countLeftNodes(self):
        return self._countLeftNodes(self._root)
    
    def _graphWalk(self, p, stream):
        if p:
            stream << "\t\t" << "n" << p.key << "[label=\"" << p.key << "\"];\n"
            if p.left:
                stream << "\t\tn" << p.key << "--" << "n" << p.left.key << ";\n"
                self._graphWalk(p.left, stream)
            else:
                stream << "\t\t" << "n" << p.key << "leftNull" << "[style=\"filled\",label=\"NULL\"];\n"
                stream << "\t\tn" << p.key << "--" << "n" << p.key << "leftNull\n"
            if p.right:
                stream << "\t\tn" << p.key << "--" << "n" << p.right.key << ";\n"
                self._graphWalk(p.right, stream)
            else:
                stream << "\t\t" << "n" << p.key << "rightNull" << "[style=\"filled\", label=\"NULL\"];\n"
                stream << "\t\tn" << p.key << "--" << "n" << p.key << "rightNull\n"

    def _prepareGraph(self):
        a = QByteArray()
        stream = QTextStream(a, QIODevice.ReadWrite)
        stream << "graph{\n"
        stream << "\tnode[fontsize=10,margin=0,width=\".4\", height=\".3\"];\n"
        stream << "\tsubgraph cluster17{\n"
        self._graphWalk(self._root, stream)
        stream << "\t}\n" << "}\n"
        stream.flush()
        return a

    def getPixmap(self):
        p = QProcess()
        
        a = self._prepareGraph()
        #a_str = QTextCodec.codecForMib(106).toUnicode(a)

        p.setProcessChannelMode(QProcess.MergedChannels)
        p.start("dot", ["-Tpng"]) # Graphviz must be installed and added to PATH
        p.write(a)

        data = QByteArray()
        pixmap = QPixmap()
        while p.waitForReadyRead(100):
            data.append(p.readAll())
        pixmap.loadFromData(data)

        return pixmap


class TestBST(unittest.TestCase):
    def _setup(self):
        self.a = BST()
        self.a.insert(7)
        self.a.insert(6)
        self.a.insert(10)
        self.a.insert(3)
        self.a.insert(4)
        self.a.insert(5)
        self.a.insert(8)
        self.a.insert(12)
        self.a.insert(9)
        self.a.deleteNode(7)
    
    def test_countLeftNodes(self): # number of nodes with only left child
        self._setup()
        self.assertEqual(self.a.countLeftNodes(), 7)
    
    def test_countLevels(self): # tree neight
        self._setup()
        self.assertEqual(self.a.countLevels(), 5)
    
    def test_countNodes(self): # number of nodes
        self._setup()
        self.assertEqual(self.a.countNodes(), 8)
    
    def test_findElem(self): # find element
        self._setup()
        self.assertTrue(self.a.findElem(12) is not None)

    def test_preorderWalk(self): # run the method
        self._setup()
        self.a.preorderWalk()
    
    def test_inorderWalk(self): # run the method
        self._setup()
        self.a.inorderWalk()

    def test_postorderWalk(self): # run the method
        self._setup()
        self.a.postorderWalk()
