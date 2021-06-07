import unittest
import os
from college_region import *

class TestRegionData(unittest.TestCase):

    # confirm length of final dictionary
    def test_region_data(self):
        ref = RegionData()
        ref._load_data()
        self.assertEqual(len(ref.x1), 5)

    # checks for region plot output
    def test_region_plot(self):
        if not os.path.exists('salary_by_region.jpg'):
            RegionData().region_plot()
            path='salary_by_region.jpg'
            self.assertTrue(os.path.exists(path))

class TestMapData(unittest.TestCase):

    # checks the size of the map dataframe
    def test_map_data(self):
        ref = MapData()
        ref._load_data()
        self.assertEqual(len(ref.all_data.index), 249)

if __name__ == '__main__':
    unittest.main()
