from grads_data import GradData
import matplotlib.pyplot as plt
import argparse
import pandas as pd
import numpy as np

# school_type = 'Party'
# type_to_maj_cat = {'Party', 'Ivy League', 'Engineering', 'Liberal Arts', 'State'}

import descartes
import geopandas as gpd
from shapely.geometry import Point, Polygon
from re import sub
from decimal import Decimal
import math

gd = GradData()
print(gd.get_data())

FILE_PATH = './salaries-by-region.csv'
data = pd.read_csv(FILE_PATH)
all_data = pd.merge(data, pd.read_csv('./EDGE_GEOCODE_POSTSECONDARYSCH_2021/EDGE_GEOCODE_POSTSECSCH_2021.csv'), left_on='School Name', right_on='NAME', how='left')
all_data = pd.merge(all_data, pd.read_csv('./salaries-by-college-type.csv'), on='School Name', how='left')
state_map = gpd.read_file('./base_map/cb_2019_us_state_500k.shp')

geometry = [Point(xy) for xy in zip(all_data['LON'], all_data['LAT'])]
geo_df = gpd.GeoDataFrame(all_data, geometry=geometry)


fig, ax = plt.subplots(figsize=(8,4))
state_map.plot(ax=ax, alpha=0.4, color='grey')
geo_df.plot(column='School Type', cmap='jet', ax=ax, alpha=0.5, legend=True, markersize=[float(Decimal(sub(r'[^\d.]', '', i[1:]))) / 250 for i in geo_df['Starting Median Salary_x']])

# set latitiude and longitude boundaries for map display
plt.xlim(-125,-70)
plt.ylim(25,50)

# show map
plt.show()

def main():
    parser = argparse.ArgumentParser(
        description='analyze various data sets related to expected salaries based on college region, type, and major'
    )

    parser.add_argument('command', metavar='<command>', type=str, help='command to execute', default='plot')
    parser.add_argument('-o', '--ofile', metavar='<outfile>', dest='output', action='store')
    parser.add_argument('-g', '--grads_data', metavar='<plot name>', dest='plot_grads_data', choices=['median_salary', 'num_respondents'])
    args = parser.parse_args()
    
    
    if args.command == 'plot':
        if args.plot_grads_data is not None:
            if args.plot_grads_data == 'median_salary':
                gd.plot_top10_median_salary()
                if args.output is not None:
                    gd.get_csv_top10_salaries(args.output)
            elif args.plot_grads_data == 'num_respondents':
                gd.plot_num_respondents_top10()
                if args.output is not None:
                    gd.get_csv_top10_respondents(args.output)

if __name__ == '__main__':
    # main()
    pass