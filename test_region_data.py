import unittest
import os
from college_region import *

class TestRegionData(unittest.TestCase):

    def test_region_data(self):
        ref = RegionData()
        ref._load_data()
        self.assertEqual(len(ref.x1), 5)

    def test_region_plot(self):
        if not os.path.exists('salary_by_region.jpg'):
            RegionData().region_plot()
            path='salary_by_region.jpg'
            self.assertTrue(os.path.exists(path))

class TestMapData(unittest.TestCase):

    def test_map_data(self):
        ref = MapData()
        ref._load_data()
        self.assertEqual(len(ref.all_data.index), 249)

    def test_map_plot(self):
        if not os.path.exists('final_map.jpg'):
            MapData().plot_map()
            path='final_map.jpg'
            self.assertTrue(os.path.exists(path))

if __name__ == '__main__':
    unittest.main()
