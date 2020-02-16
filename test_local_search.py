import unittest
import backtrack_assign1 as Backtrack

class TestLocalSearch(unittest.TestCase):
    def setUp(self):
        """Incomplete unit test for Local Search"""
        g = Backtrack.Graph("usdata.txt")
        _local_search = Backtrack.LocalSearch(g)
    