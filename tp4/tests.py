import unittest
from tp4 import edit_distance

class TestEditDistance(unittest.TestCase):
    def test_general(self):
        self.assertEqual(
            edit_distance("aloroswmenet", "calorosamente",
                         ins_cost=2, del_cost=2, sub_cost=4, swap_cost=3), 9
        )

        self.assertEqual(
            edit_distance("anticonstitucional", "maticonsujkannal",
                         ins_cost=2, del_cost=2, sub_cost=4, swap_cost=3), 24
        )

        self.assertEqual(
            edit_distance("calor", "caolr",
                         ins_cost=2, del_cost=2, sub_cost=4, swap_cost=3), 3
        )





unittest.main()

