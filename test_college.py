"""Unit tests for the college_type program."""
import unittest

from college_type import *

class TestCollege(unittest.TestCase):

    def test_median_data_start(self):
        # make sure the median_data method properly parses input list into correct startAvg defaultdict 
        A1= SalaryData()
        f = [['rock', 'solid', '$30,000', '$40,000'], ['cheese', 'solid', '$20,000', '$30,000']]
        A1.median_data(f)
        self.assertEqual(A1.d['solid'], 25000)

    def test_median_data_mid(self):
        # make sure the median_data method properly parses input list into correct midAvg defaultdict 
        A1= SalaryData()
        f = [['rock', 'solid', '$30,000', '$40,000'], ['cheese', 'solid', '$20,000', '$30,000']]
        A1.median_data(f)
        self.assertEqual(A1.e['solid'], 35000)

    def test_spread_data_tenth(self):
        # make sure the spread_data method properly parses input list into correct tenthAvg defaultdict 
        A1= SalaryData()
        f = [['rock', 'solid', '$30,000', '$40,000', '$30,000', '$20,000', '$30,000', '$40,000'], ['cheese', 'solid', '$20,000', '$30,000', '$40,000', '$20,000', '$30,000', '$30,000']]
        A1.spread_data(f)
        self.assertEqual(A1.g['solid'], 35000)

    def test_spread_data_twentyfifth(self):
        # make sure the spread_data method properly parses input list into correct twentyfifthAvg defaultdict 
        A1= SalaryData()
        f = [['rock', 'solid', '$30,000', '$40,000', '$30,000', '$20,000', '$30,000', '$40,000'], ['cheese', 'solid', '$20,000', '$30,000', '$40,000', '$20,000', '$30,000', '$30,000']]
        A1.spread_data(f)
        self.assertEqual(A1.h['solid'], 20000)

    def test_spread_data_seventyfifth(self):
        # make sure the spread_data method properly parses input list into correct seventyfifthAvg defaultdict 
        A1= SalaryData()
        f = [['rock', 'solid', '$30,000', '$40,000', '$30,000', '$20,000', '$30,000', '$40,000'], ['cheese', 'solid', '$20,000', '$30,000', '$40,000', '$20,000', '$30,000', '$30,000']]
        A1.spread_data(f)
        self.assertEqual(A1.i['solid'], 30000)

    def test_spread_data_ninetieth(self):
        # make sure the spread_data method properly parses input list into correct ninetiethAvg defaultdict 
        A1= SalaryData()
        f = [['rock', 'solid', '$30,000', '$40,000', '$30,000', '$20,000', '$30,000', '$40,000'], ['cheese', 'solid', '$20,000', '$30,000', '$40,000', '$20,000', '$30,000', '$30,000']]
        A1.spread_data(f)
        self.assertEqual(A1.j['solid'], 35000)


if __name__ == '__main__':
    unittest.main()

