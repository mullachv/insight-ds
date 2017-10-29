# Author: V. Mullachery
# Copyright, All rights reserved
#
# Augmented Tree Node inspired from BST to store and retrieve nodes in
# O(log(n)) time. The main purpose is these can fetch median values in O(log(n)) time
# because they contain left and right child node counts, and also a repetitions count for
# duplicate values for each node
#
class AugTreeNode(object):
    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data
        self.nleft_children = 0
        self.nright_children = 0
        self.parent = None
        self.reps = 1

    def _is_root(self):
        return self.parent == None

    def _is_a_left_child(self):
        if self._is_root():
            return False
        return self == self.parent.left

    # Given parent node's sorted ordinal position, compute the current nodes ordinal
    def _get_ord_position(self, ppos):
        if (self._is_a_left_child()):
            return ppos[0] - self.nright_children - self.reps, \
                   ppos[0] - self.nright_children - 1

        return ppos[1] + self.nleft_children + 1, \
               ppos[1] + self.nleft_children + self.reps

    #t is the desired position, p is the position of the parent of this node
    def _find_at_posn(self, t):
        if not self._is_root():
            raise ValueError('__find_at_posn method called on non-root node')

        root_pos = self.nleft_children + 1, self.nleft_children + self.reps
        total = (self.nleft_children + self.nright_children + self.reps)
        if t > total:
            raise IndexError('Augmented Tree: search index exceeds range')
        if t < 1:
            raise IndexError('Augmented Tree: search index exceeds range')
        if  root_pos[0] <= t <= root_pos[1]:
            return self
        if t < root_pos[0]:
            return self.left._get_node_at_position(t, root_pos)

        if self.right:
            return self.right._get_node_at_position(t, root_pos)


    def _get_node_at_position(self, t, p):
        m_pos = self._get_ord_position(p)
        if m_pos[0] <= t <= m_pos[1]:
            return self
        if m_pos[1] < t:
            return self.right._get_node_at_position(t, m_pos)
        return self.left._get_node_at_position(t, m_pos)

    def insert(self, value):
        if value == self.data:
            self.reps += 1
        elif value < self.data:
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
        total = (self.nleft_children + self.nright_children + self.reps)
        med_pos = total >> 1
        if total % 2 == 0:
            m1 = self._find_at_posn(med_pos).data
            m2 = self._find_at_posn(med_pos + 1).data
            return round( (m1 + m2)/ 2)

        return self._find_at_posn(med_pos + 1).data

#Unittests
import unittest
class TestTree(unittest.TestCase):
    def test8(self):
        sol = AugTreeNode(20)
        for _ in range(900):    sol.insert(19)
        sol.insert(20)
        self.assertEqual(19, sol.median())
    def test7(self):
        sol = AugTreeNode(20)
        for _ in range(900):    sol.insert(500)
        sol.insert(499)
        self.assertEqual(500, sol.median())
    def test6(self):
        sol = AugTreeNode(20)
        for _ in range(900):    sol.insert(500)
        sol.insert(501)
        self.assertEqual(500, sol.median())
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
