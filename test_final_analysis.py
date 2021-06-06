from final_analysis import *
import unittest
import os

class test_final_analysis(unittest.TestCase):

    # MapPlot tests
    m = MapPlot()

    # test that MapPlot object is initialized with the correct data
    def test_create_mp(self):
        self.assertEqual(self.m.merged.shape, (249, 31))

    # test that MapPlot object writes to csv output as expected
    def test_get_csv(self):
        self.m.get_csv('test_mp_out.csv')
        self.assertEqual(os.path.exists('test_mp_out.csv'), True)

    # MajCat tests

    # test that MajCat objects for every available major category are created with the correct
    # data, and have the correct output size after processing the data for the charts
    def test_create_mc(self):
        for i in ['Education', 'Psychology & Social Work',
        'Biology & Life Science', 'Arts', 'Humanities & Liberal Arts', 'Health', 'Industrial Arts & Consumer Services',
        'Agriculture & Natural Resources', 'Social Science', 'Communications & Journalism', 'Business', 'Law & Public Policy',
        'Physical Sciences', 'Computers & Mathematics', 'Interdisciplinary', 'Engineering']:
            mc = MajCat(i)
            self.assertEqual(mc.cat, i)
            self.assertEqual(mc.salary_data.shape, (173, 21))
            self.assertEqual(mc.type_data.shape, (269, 8))
            self.assertLessEqual(mc.top_5m.shape, (5, 21))
            self.assertLessEqual(mc.top_5s.shape, (5, 8))

    # test that MajCat objects write to csv output as expected for top 5 majors
    def test_get_csv_top5m(self):
        for i in ['Education', 'Psychology & Social Work',
        'Biology & Life Science', 'Arts', 'Humanities & Liberal Arts', 'Health', 'Industrial Arts & Consumer Services',
        'Agriculture & Natural Resources', 'Social Science', 'Communications & Journalism', 'Business', 'Law & Public Policy',
        'Physical Sciences', 'Computers & Mathematics', 'Interdisciplinary', 'Engineering']:
            mc = MajCat(i)
            mc.get_csv_top5m('test_5m_mc_' + i + "out.csv")
            self.assertEqual(os.path.exists('test_5m_mc_' + i + "out.csv"), True)

    # test that MajCat objects write to csv output as expected for top 5 schools
    def test_get_csv_top5s(self):
        for i in ['Education', 'Psychology & Social Work',
        'Biology & Life Science', 'Arts', 'Humanities & Liberal Arts', 'Health', 'Industrial Arts & Consumer Services',
        'Agriculture & Natural Resources', 'Social Science', 'Communications & Journalism', 'Business', 'Law & Public Policy',
        'Physical Sciences', 'Computers & Mathematics', 'Interdisciplinary', 'Engineering']:
            mc = MajCat(i)
            mc.get_csv_top5s('test_5s_mc_' + i + "out.csv")
            self.assertEqual(os.path.exists('test_5s_mc_' + i + "out.csv"), True)

if __name__ == '__main__':
    unittest.main()