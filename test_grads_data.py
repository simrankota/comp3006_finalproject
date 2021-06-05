import unittest
from grads_data import GradData

class test_grads_data(unittest.TestCase):
    d = GradData()

    # tests sort functionality by ensuring the max/min values are in the appropriate spot based on
    # sort logic
    def test_sort(self):
        # attempt to sort on column that does not exist. Should throw IndexError
        with self.assertRaises(IndexError):
            ret = self.d.sort_data('hello')
        # attempt to sort by descending values of Median column. Max column value should be the
        # first value
        self.d.sort_data('Median')
        self.assertEqual(self.d.data['Median'].max(), list(self.d.data['Median'])[0])
        # attempt to sort by ascending values of Median column. Max column value should be the
        # last value
        self.d.sort_data('Median', True)
        self.assertEqual(self.d.data['Median'].max(), list(self.d.data['Median'])[len(self.d.data["Median"]) - 1])

    # tests get_stats function. Ensures all computed statistics return their expected values
    def test_get_stats(self):
        self.d.get_stats()
        self.assertEqual(self.d.dims, (173, 21))
        self.assertEqual(self.d.num_cats, 16)
        self.assertEqual(self.d.median_sal_range, (22000, 110000))

    # normal load data funtionality is tested with initialization of GradData object. Check what
    # happens if load_data method is called with nonexistent file being passed in. Expected to throw
    # a FileNotFoundError
    def test_load_data(self):
        self.d.FILE_PATH = './test-false.csv'
        with self.assertRaises(FileNotFoundError):
            ret = self.d.load_data()

    # test get data functionality. Shape of returned dataframe should be 173 x 21
    def test_get_data(self):
        self.assertEqual(self.d.get_data().shape, (173, 21))

if __name__ == '__main__':
    unittest.main()
