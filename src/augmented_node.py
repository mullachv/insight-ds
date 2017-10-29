# Author: V. Mullachery
# Copyright, All rights reserved
#
# Augmented Tree Node inspired from BST to store and retrieve nodes in
# O(log(n)) time. The main purpose is these can fetch median values in O(log(n)) time
# because they contain left and right child node count, for each node
#
class AugTreeNode(object):
    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data
        self.nleft_children = 0
        self.nright_children = 0
        self.parent = None

    def _is_root(self):
        return self.parent == None

    def _is_a_left_child(self):
        return self.data <= self.parent.data

    # Given parent node's sorted ordinal position, compute the current nodes ordinal
    def _get_ord_position(self, ppos):
        if (self._is_a_left_child()):
            return ppos - self.nright_children - 1

        return ppos + self.nleft_children + 1

    #t is the desired position, p is the position of the parent of this node
    def _find_at_posn(self, t):
        if not self._is_root():
            raise ValueError('__find_at_posn method called on non-root node')

        root_pos = self.nleft_children + 1
        total = (self.nleft_children + self.nright_children + 1)
        if t > total:
            raise IndexError('Augmented Tree: search index exceeds range')
        if t < 1:
            raise IndexError('Augmented Tree: search index exceeds range')
        if t == root_pos:
            return self
        if t < root_pos:
            return self.left._get_node_at_position(t, root_pos)

        if self.right:
            return self.right._get_node_at_position(t, root_pos)


    def _get_node_at_position(self, t, p):
        if t == p:
            return self.parent
        m_pos = self._get_ord_position(p)
        if m_pos == t:
            return self
        if m_pos < t:
            return self.right._get_node_at_position(t, m_pos)
        return self.left._get_node_at_position(t, m_pos)

    def insert(self, value):
        if value <= self.data:
            self.nleft_children += 1
            if self.left:
                self.left.insert(value)
            else:
                self.left = AugTreeNode(value)
                self.left.parent = self
        else:
            self.nright_children += 1
            if self.right:
                self.right.insert(value)
            else:
                self.right = AugTreeNode(value)
                self.right.parent = self

    def median(self):
        total = (self.nleft_children + self.nright_children + 1)
        med_pos = total >> 1
        if total % 2 == 0:
            m1 = self._find_at_posn(med_pos).data
            m2 = self._find_at_posn(med_pos + 1).data
            return round( (m1 + m2)/ 2)

        return self._find_at_posn(med_pos + 1).data

#Unittests
import unittest
class TestTree(unittest.TestCase):
    def test5(self):
        sol = AugTreeNode(100087)
        self.assertEqual(100087, sol.median())
    def test_4(self):
        sol = AugTreeNode(10); sol.insert(20)
        self.assertEqual(15, sol.median())
    def test_3(self):
        sol = AugTreeNode(-1)
        self.assertEqual(-1, sol.median())
    def test_2(self):
        sol = AugTreeNode(22)
        sol.insert(-32);sol.insert(42);sol.insert(908); sol.insert(37)
        self.assertEqual(37, sol.median())
    def test_1(self):
        sol = AugTreeNode(22)
        sol.insert(-32); sol.insert(42); sol.insert(908)
        self.assertEqual(32, sol.median())

if __name__ == '__main__':
    unittest.main()
