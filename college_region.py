import csv
import os
import sys
from collections import defaultdict
import logging
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import descartes
import geopandas as gpd
from shapely.geometry import Point, Polygon
import re
# from re import sub
# from decimal import Decimal
import math
region = defaultdict(int)
startTotal = defaultdict (float)
midTotal = defaultdict (float)
startAvg = defaultdict (float)
midAvg = defaultdict (float)
salDelta = defaultdict (float)

class RegionData:
    REGION_SALARY = 'salaries-by-region.csv'
    def __init__(self):
        self._load_data()

    def _load_data(self):
        global x
        global y
        header = True
        with open(self.REGION_SALARY, "r") as rf:
            for row in csv.reader(rf):
                if header == True:
                    header = False
                    continue
                else:
                    region[row[1]] += 1
                    row[2]=row[2].replace(",","")
                    startTotal[row[1]] += float(row[2][1:])
                    row[3]=row[3].replace(",","")
                    midTotal[row[1]] += float(row[3][1:])

            for key in startTotal:
                startAvg[key] = round(startTotal[key]/region[key],2)
                midAvg[key] = round(midTotal[key]/region[key],2)
                salDelta[key] = round(midAvg[key]-startAvg[key],2)

            self.x1 = list(startAvg.keys())
            self.y1 = list(startAvg.values())
            self.x2 = list(midAvg.keys())
            self.y2 = list(midAvg.values())
            self.x3 = list(salDelta.keys())
            self.y3 = list(salDelta.values())


    def region_plot(self):
        width = 0.35
        N = len(self.x1)
        ind = np.arange(N)
        figure, axis = plt.subplots(2)
        axis[0].bar(ind,self.y1, width, label='Starting Salary')
        axis[0].bar(ind+width, self.y2, width,label='Mid Salary')
        axis[0].set_xticks(ind+width/2)
        axis[0].set_xticklabels(self.x1)
        axis[0].set_ylim(0, 100000)
        axis[0].legend(loc='best')

        axis[1].bar(self.x3,self.y3, width, label='Salary Delta')
        axis[1].legend(loc='best')

        plt.show()
        plt.savefig('final_testing_3.jpg')

class MapData:
    SALARY_FILE = 'salaries-by-region.csv'
    GEO_FILE = 'EDGE_GEOCODE_POSTSECSCH_2021.csv'
    SCHOOL_TYPE = 'salaries-by-college-type.csv'
    MAP_FILE = 'base_map/cb_2019_us_state_500k.shp'

    def __init__(self):
        self._load_data()

    def _load_data(self):
        if not (os.path.exists(self.GEO_FILE) and os.path.exists(self.SCHOOL_TYPE) and os.path.exists(self.MAP_FILE)):
            raise FileNotFoundError('Required file missing from directory!')
        else:
            SCHOOL_LOOKUP = {"California Polytechnic State University-San Luis Obispo" : "Cal Poly San Luis Obispo",
            "University of California-Los Angeles" : "University of California at Los Angeles",
            "Brigham Young University-Provo" : "Brigham Young University",
            "University of Washington-Seattle Campus" : "University of Washington",
            "University of Colorado Denver/Anschutz Medical Campus" : "University of Colorado-Denver",
            "University of Hawaii at Manoa" : "University of Hawaii",
            "Missouri University of Science and Technology" : "University of Missouri-Rolla",
            "University of Michigan-Ann Arbor" : "University of Michigan",
            "Pennsylvania State University-Penn State Harrisburg" : "Penn State-Harrisburg"}



            data = pd.read_csv(self.SCHOOL_TYPE)#(SALARY_FILE)
            geo_data = pd.read_csv(self.GEO_FILE)
            # type_data = pd.read_csv(self.SCHOOL_TYPE)



            # all_data = pd.merge(data, type_data, on='School Name', how='right')
            # all_data.drop_duplicates(subset='School Name', keep='first', inplace=True)
            data['School Name'] = data['School Name'].str.replace(re.compile("\((.+)\)"),'')
            data['School Name'] = data['School Name'].str.strip()
            data['School Name'] = data['School Name'].str.replace("  "," ")
            data['School Name'] = data['School Name'].str.replace(" , ","-")
            data['School Name'] = data['School Name'].str.replace(" ,","-")
            data['School Name'] = data['School Name'].str.replace(" - ", "-")
            data['School Name'] = data['School Name'].str.replace(", ","-")
            data['School Name'] = data['School Name'].str.replace("- ","-")
            geo_data['NAME'] = geo_data['NAME'].replace(SCHOOL_LOOKUP)
            self.all_data = pd.merge(data, geo_data, left_on='School Name', right_on='NAME', how='left')
            self.all_data.drop_duplicates(subset='School Name', keep='first', inplace=True)
            # self.all_data.to_csv('all_data3.csv')
            # print(self.all_data)



    def plot_map(self):
        state_map = gpd.read_file(self.MAP_FILE)
        geometry = [Point(xy) for xy in zip(self.all_data['LON'], self.all_data['LAT'])]
        geo_df = gpd.GeoDataFrame(self.all_data, geometry=geometry)
        fig, ax = plt.subplots(figsize=(30,20))
        state_map.plot(ax=ax, alpha=0.4, color='grey')
        geo_df.plot(column='School Type', cmap='jet', ax=ax, alpha=0.5, legend=True, markersize=[float(re.sub(r'[^\d.]', '', i[1:])) / 250 for i in geo_df['Starting Median Salary']])

        # set latitiude and longitude boundaries for map display
        plt.xlim(-125,-63)
        plt.ylim(25,50)

        # show map
        # plt.show()
        plt.savefig('final_map6.jpg')

if __name__ == '__main__':
    MapData()
    MapData().plot_map()
    # RegionData()
    # RegionData.region_plot()
