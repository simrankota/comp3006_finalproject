from grads_data import GradData
import matplotlib.pyplot as plt
import argparse
import pandas as pd
import numpy as np
import descartes
import geopandas as gpd
from shapely.geometry import Point, Polygon
from re import sub
from decimal import Decimal
import math
import logging
import os
from college_type import SalaryData
import sys
from college_region import *

# MapPlot class to create a geoplot displaying the location, salary, and type of schools
class MapPlot():

    # constructor for MapPlot class. Reads in data from college_region module
    def __init__(self):
        logging.debug('retrieving map data from college_region module')
        m = MapData()
        self.merged = m.all_data

    # Map plotting logic. Creates a base map of the US, and then adds points for each school using
    # data from the joined data table and the geopandas module. Location of the point is based on
    # latitude and longitude of the school, size of the point is based on Starting Median salary
    # (scale created by dividing number by 250), and color is based on school type
    def create_map(self):
        all_data = self.merged
        logging.debug('retrieving base US geographic data from ./base_map/cb_2019_us_state_500k.shp')
        if not os.path.exists('./base_map/cb_2019_us_state_500k.shp'):
            raise FileNotFoundError()
        else:
            state_map = gpd.read_file('./base_map/cb_2019_us_state_500k.shp')
            logging.debug('data retrieved succesfully')
        geometry = [Point(xy) for xy in zip(all_data['LON'], all_data['LAT'])]
        geo_df = gpd.GeoDataFrame(all_data, geometry=geometry)
        fig, ax = plt.subplots(figsize=(8,4))
        fig.suptitle('Starting Median Salary based on Type of Schools in the US')
        state_map.plot(ax=ax, alpha=0.4, color='grey')
        geo_df.plot(column='School Type', cmap='jet', ax=ax, alpha=0.5, legend=True,
            markersize=[float(Decimal(sub(r'[^\d.]', '', i[1:]))) / 1000 for i in geo_df['Starting Median Salary']])
        # set latitiude and longitude boundaries for map display
        plt.xlim(-125,-65)
        plt.ylim(25,50)
        # show map
        logging.debug('creating geoplot')
        plt.show()

    # returns csv output of data used in plot. Prints to provided output file
    def get_csv(self, output):
        logging.debug(f'printing data to {output}')
        pd.DataFrame({"School Name": self.merged['School Name'], "School Type": self.merged['School Type'], "Latitude":
            self.merged['LAT'], "Longitude": self.merged['LON'], "Median Starting Salary":
            self.merged['Starting Median Salary']}).to_csv(output)

# MajCat class to create a bar chart of the top 5 schools/majors based on major category
class MajCat():

    # constructor for the MajCat class. Expects a string major_cat input based on which the top 5
    # schools and majors by median salary will be calculated. Retrieves necessary data files from
    # modules, as well as an additional csv which contains an abitrary mapping between major
    # categories and school type
    def __init__(self, major_cat):
        logging.debug('initializing MajCat object')
        self.cat = major_cat
        logging.debug('retrieving salary by major data from grads_data module')
        self.salary_data = GradData().get_data()
        logging.debug('retrieving major category to school type mapping file from ./College_Major-Type_Lookup.csv')
        if not os.path.exists('./College_Major-Type_Lookup.csv'):
            raise FileNotFoundError()
        else:
            self.mapping = pd.read_csv("./College_Major-Type_Lookup.csv")
        logging.debug('retrieving salaries by college type data from module')
        self.type_data = pd.DataFrame(SalaryData().get_data(), columns=['School Name',
            'School Type', 'Starting Median Salary', 'Mid-Career Median Salary',
            'Mid-Career 10th Percentile Salary', 'Mid-Career 25th Percentile Salary',
            'Mid-Career 75th Percentile Salary', 'Mid-Career 90th Percentile Salary'])
        self.top_5_schools()
        self.top_5_majors()


    # calculates the top 5 majors based on the provided major category. Filters salary data table
    # based on major category, sorts by median salary in descending order, and saves the top 5
    # rows to a class atrribute
    def top_5_majors(self):
        logging.debug(f'calculating top 5 majors by median salary for major category {self.cat}')
        majors = self.salary_data[self.salary_data['Major_category'] == self.cat]
        majors = majors.sort_values(by=['Median'], ascending=False)
        self.top_5m = majors.head(5)

    # calculates the top 5 schools based on the provided major category. Retrieves school types
    # from mapping table associated with the provided major category, finds all schools under that
    # school type from the salary by school type data table, sorts by starting median salary in
    # descending order, and saves the top 5 rows to a class attribute
    def top_5_schools(self):
        logging.debug(f'calculating top 5 schools by median salary for major category {self.cat}')
        types = self.mapping[self.mapping['Major_Category'] == self.cat]
        assert types.shape == (1, 2)
        types = [i.split(", ") for i in types['School_Type']]
        schools = self.type_data[self.type_data['School Type'].isin(types[0])]
        schools["Starting Median Salary"] = [float(Decimal(sub(r'[^\d.]', '', i[1:]))) for i in schools["Starting Median Salary"]]
        schools = schools.sort_values(by=['Starting Median Salary'], ascending=False)
        self.top_5s = schools.head(5)

    # logic to create the plot. Output will be a plot with two subplots, one showing the top 5
    # schools and the other showing the top 5 majors, both based on median salary
    def create_plot(self):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7, 8))
        fig.suptitle(f'Top 5 Schools and Majors for {self.cat}')
        ax1.bar(self.top_5m['Major'], self.top_5m['Median'], color='orange')
        ax1.set_title('Top 5 Majors')
        ax1.set_ylabel('Median Salary')
        ax2.bar(self.top_5s['School Name'], self.top_5s['Starting Median Salary'])
        ax2.set_title('Top 5 Schools')
        ax2.set_ylabel('Median Salary')
        for label in ax1.get_xticklabels() + ax2.get_xticklabels():
            label.set_rotation(90)
            label.set_ha('right')    
        plt.tight_layout()
        plt.subplots_adjust(top=0.9)
        logging.debug('creating major and school-type bar plots')
        plt.show()

    # returns csv output of data used in top 5 majors subplot. Prints to provided output file
    def get_csv_top5m(self, output):
        logging.debug(f'printing data to {output}')
        pd.DataFrame({"Major": self.top_5m["Major"], "Median Salary": self.top_5m['Median']}).to_csv(output)

    # returns csv output of data used in top 5 schools subplot. Prints to provided output file
    def get_csv_top5s(self, output):
        logging.debug(f'printing data to {output}')
        pd.DataFrame({"School Name": self.top_5s['School Name'], "Median Salary": self.top_5s['Starting Median Salary']}).to_csv(output)


def main():
    # initialize argument parser
    parser = argparse.ArgumentParser(
        description='analyze various data sets related to expected salaries based on college region, type, and major'
    )

    # required command plot to use file
    parser.add_argument('command', metavar='<command>', type=str, help="command to execute. Only acceptable input is 'plot'", default='plot')
    # optional argument -o to print csv output for final plots
    parser.add_argument('-o', '--ofile', metavar='<outfile>', dest='output', action='store', help='output file to store csv data associated with final plots')
    # optional argument -i to display initial data plots
    parser.add_argument('-i', '--initial_plots', dest='plot_initial', action='store_true', help='plot initial EDA (exploratory data analysis) plots for recent_grads.csv, salaries_by_college_type.csv, and salaries_by_region.csv')
    # optional argument -f to display final data plots. Requires a major category to be inputted to display top 5 majors and schools for that category
    parser.add_argument('-f', '--final_plots', dest='plot_final', metavar='<major category>', action='store', choices=['Education', 'Psychology & Social Work',
        'Biology & Life Science', 'Arts', 'Humanities & Liberal Arts', 'Health', 'Industrial Arts & Consumer Services',
        'Agriculture & Natural Resources', 'Social Science', 'Communications & Journalism', 'Business', 'Law & Public Policy',
        'Physical Sciences', 'Computers & Mathematics', 'Interdisciplinary', 'Engineering'], help="plot final geoplot exploring schools by location, median starting salary, and type, as well as barchart showing top 5 schools and majors for an inputted major category. Major category input is REQUIRED. Options are 'Education', 'Psychology & Social Work', 'Biology & Life Science', 'Arts', 'Humanities & Liberal Arts', 'Health', 'Industrial Arts & Consumer Services', 'Agriculture & Natural Resources', 'Social Science', 'Communications & Journalism', 'Business', 'Law & Public Policy', 'Physical Sciences', 'Computers & Mathematics', 'Interdisciplinary', 'Engineering'")

    args = parser.parse_args()
    
    
    if args.command == 'plot':
        # show initial data plots
        if args.plot_initial:
            gd = GradData()
            gd.plot_top10_median_salary()
            gd.plot_num_respondents_top10()
            t = SalaryData()
            t.plot_type_median()
            t.plot_type_spread()
            r = RegionData()
            r.region_plot()
        # show final data plots
        elif args.plot_final is not None:
            mp = MapPlot()
            mp.create_map()
            mc = MajCat(args.plot_final)
            mc.create_plot()
            # print csv output
            if args.output is not None:
                mp.get_csv("map" + args.output)
                mc.get_csv_top5m("5m" + args.output)
                mc.get_csv_top5s("5s" + args.output)
    else:
        logging.warning('unsupported command provided')

if __name__ == '__main__':
    # initialize logger and set level to debug
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # set file logger level at debug
    fh = logging.FileHandler('./log_files/analysis.log', 'w')
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)

    # set console logger level at info
    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(logging.INFO)
    logger.addHandler(sh)

    main()