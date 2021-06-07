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
import math

#defalut dicts for region data
region = defaultdict(int)
startTotal = defaultdict (float)
midTotal = defaultdict (float)
startAvg = defaultdict (float)
midAvg = defaultdict (float)
salDelta = defaultdict (float)

LOG_FILE = 'salary_data.log'
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

#file handler
fh = logging.FileHandler(LOG_FILE, 'w')
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)

class RegionData:
    '''Class for cleaning and plotting regional salary data'''
    REGION_SALARY = 'salaries-by-region.csv'
    def __init__(self):
        self._load_data()
        # self.region_plot()

    def _load_data(self):
        #variable used to skip the header row
        header = True
        logging.debug("opening regional salary data file")
        with open(self.REGION_SALARY, "r") as rf:
            for row in csv.reader(rf):
                #skipps over header row
                if header == True:
                    header = False
                    continue
                else:
                    #converts currency to float by removing $ and comma and creates dicts for avg calc
                    region[row[1]] += 1
                    row[2]=row[2].replace(",","")
                    startTotal[row[1]] += float(row[2][1:])
                    row[3]=row[3].replace(",","")
                    midTotal[row[1]] += float(row[3][1:])

            logging.debug("creating dicts for chart")
            for key in startTotal:
                #calculates average from total and count and delta of averages
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
        logging.debug("creating regional data chart")
        #plots avg data by region
        width = 0.35
        N = len(self.x1)
        ind = np.arange(N)
        figure, axis = plt.subplots(2,figsize=(15,9))
        axis[0].bar(ind,self.y1, width, label='Starting Salary')
        axis[0].bar(ind+width, self.y2, width,label='Mid Salary')
        axis[0].set_xticks(ind+width/2)
        axis[0].set_xticklabels(self.x1)
        axis[0].set_ylim(0, 100000)
        axis[0].legend(loc='best')
        axis[1].bar(self.x3,self.y3, width, label='Salary Delta')
        axis[1].legend(loc='best')

        plt.show()
        plt.savefig('salary_by_region.jpg')

class MapData:
    '''Class for joining data sets and plotting on map'''

    #file name variables
    SALARY_FILE = 'salaries-by-region.csv'
    GEO_FILE = 'EDGE_GEOCODE_POSTSECSCH_2021.csv'
    SCHOOL_TYPE = 'salaries-by-college-type.csv'
    MAP_FILE = './base_map/cb_2019_us_state_500k.shp'

    def __init__(self):
        self._load_data()
        # self.plot_map()

    def _load_data(self):
        logging.debug("checking that required map files are present")
        if not (os.path.exists(self.GEO_FILE) and os.path.exists(self.SCHOOL_TYPE) and os.path.exists(self.MAP_FILE)):
            raise FileNotFoundError('Required file missing from directory!')
        else:
            #corrections for matching school name between data sets
            SCHOOL_LOOKUP = {"California Polytechnic State University-San Luis Obispo" : "Cal Poly San Luis Obispo",
            "University of California-Los Angeles" : "University of California at Los Angeles",
            "Brigham Young University-Provo" : "Brigham Young University",
            "University of Washington-Seattle Campus" : "University of Washington",
            "University of Colorado Denver/Anschutz Medical Campus" : "University of Colorado-Denver",
            "University of Hawaii at Manoa" : "University of Hawaii",
            "Missouri University of Science and Technology" : "University of Missouri-Rolla",
            "University of Michigan-Ann Arbor" : "University of Michigan",
            "Pennsylvania State University-Penn State Harrisburg" : "Penn State-Harrisburg"}

            #reads source files into pandas objects
            data = pd.read_csv(self.SCHOOL_TYPE)
            geo_data = pd.read_csv(self.GEO_FILE)

            logging.debug("creating mapping dataframe")
            #bulk modifications to school names to join data sets
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

if __name__ == '__main__':
    MapData()
    MapData().plot_map()
    RegionData()
    RegionData().region_plot()
