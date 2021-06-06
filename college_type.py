import csv
import os
import logging
import argparse
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np

col_type = defaultdict(int)
col_typeOne = defaultdict(int)
col_typeTwo = defaultdict(int)
col_typeThree = defaultdict(int)
col_typeFour = defaultdict(int)
startTotal = defaultdict(float)
midTotal = defaultdict(float)
startAvg = defaultdict(float)
midAvg = defaultdict(float)
salDelta = defaultdict(float)
tenthTotal = defaultdict(float)
twentyfifthTotal = defaultdict(float)
seventyfifthTotal = defaultdict(float)
ninetiethTotal = defaultdict(float)
tenthAvg = defaultdict(float)
twentyfifthAvg = defaultdict(float)
seventyfifthAvg = defaultdict(float)
ninetiethAvg = defaultdict(float)

# rootLogger object level set to minimal "DEBUG" level to consider logging at all levels
rootlogger = logging.getLogger()
rootlogger.setLevel(logging.DEBUG)

# writes all logs meeting set level to log file 'college_type1.log'
logfile = logging.FileHandler('college_type1.log', 'w')
logfile.setLevel(logging.DEBUG)
rootlogger.addHandler(logfile)

# writes all "INFO" level logs to console
logstream = logging.StreamHandler()
logstream.setLevel(logging.INFO)
rootlogger.addHandler(logstream)

class SalaryData:

    FILE_PATH = 'salaries-by-college-type.csv'

    # Initializes class and executes load_data, median_data, and spread_data modules
    def __init__(self):
        self.load_data()
        self.median_data(self.data)
        self.spread_data(self.data)

    def get_data(self):
        return self.data

    # Reads in the data from the salaries-by-college-type csv file.
    # If the file doesn't exist, raises a FileNotFoundError and initializes data to the data attribute
    def load_data(self):
        logging.debug('checking salaries-by-college-type.csv')
        if not os.path.exists(self.FILE_PATH):
            raise FileNotFoundError('This file does not exist inside the same directory, please try a valid file.')
        else:
            logging.debug('salaries-by-college-type.csv exists')
        first_line = True
        with open(self.FILE_PATH, 'r') as f:
            self.data = []
            logging.debug('Parsing salaries-by-college-type.csv')
            for row in csv.reader(f):
                if first_line == True:
                    first_line = False
                    continue
                else:
                    self.data.append(row)
    
    #Reads in list of rows list to only grab starting and mid-career median salary values per type of school and calculates average of each
    def median_data(self, var1):
        logging.debug('Parsing data by median starting and mid-career salaries for each school type')
        for f in var1:
            col_type[f[1]] += 1
            f[2] = f[2].replace(',','')
            startTotal[f[1]] += float(f[2][1:])
            f[3] = f[3].replace(',','')
            midTotal[f[1]] += float(f[3][1:])
        logging.debug('attempting calculations for averages of median starting and mid-career salaries for each school type')
        for key in startTotal:
            startAvg[key] = round(startTotal[key]/col_type[key],2)
            midAvg[key] = round(midTotal[key]/col_type[key],2)
            salDelta[key] = round(midAvg[key]-startAvg[key],2)
        self.d = startAvg
        self.e = midAvg
        logging.debug('salary averages calculated successfully')

    #Reads in list of rows list to only grab mid-career 10th, 25th, 75th, and 90th percentile salary values per type of school and calculates average of each
    def spread_data(self, var2):
        logging.debug('Parsing data by mid-career 10th, 25th, 75th, and 90th percentile salary for each school type')
        for f in var2:
            col_typeOne[f[1]] += 1
            if f[4] == 'N/A':
                col_typeOne[f[1]] -= 1
                f[4] = '$0.00'
            f[4] = f[4].replace(',','')
            tenthTotal[f[1]] += float(f[4][1:])
            
            col_typeTwo[f[1]] += 1
            if f[5] == 'N/A':
                col_typeTwo[f[1]] -= 1
                f[5] = '$0.00'
            f[5] = f[5].replace(',','')
            twentyfifthTotal[f[1]] += float(f[5][1:])
            
            col_typeThree[f[1]] += 1
            if f[6] == 'N/A':
                col_typeThree[f[1]] -= 1
                f[6] = '$0.00'
            f[6] = f[6].replace(',','')
            seventyfifthTotal[f[1]] += float(f[6][1:])

            col_typeFour[f[1]] += 1
            if f[7] == 'N/A':
                col_typeFour[f[1]] -= 1
                f[7] = '$0.00'
            f[7] = f[7].replace(',','')
            ninetiethTotal[f[1]] += float(f[7][1:])

        logging.debug('Calculate mid-career 10th, 25th, 75th, and 90th percentile salary averages for each school type')
        for key in tenthTotal:
            tenthAvg[key] = round(tenthTotal[key]/col_typeOne[key],2)
            twentyfifthAvg[key] = round(twentyfifthTotal[key]/col_typeTwo[key],2)
            seventyfifthAvg[key] = round(seventyfifthTotal[key]/col_typeThree[key],2)
            ninetiethAvg[key] = round(ninetiethTotal[key]/col_typeFour[key],2)
        self.g = tenthAvg
        self.h = twentyfifthAvg
        self.i = seventyfifthAvg
        self.j = ninetiethAvg
        logging.debug('salary averages calculated successfully')

    #Reads in defaultdicts of starting and mid-career averages per school type and graphs each on a double bar graph
    def plot_type_median(self):
        x1 = list(startAvg.keys())
        y1 = list(startAvg.values())
        x2 = list(midAvg.keys())
        y2 = list(midAvg.values())
        
        width = 0.35
        N = 5

        ind = np.arange(N)
        figure, axis = plt.subplots(2)
        
        axis[0].bar(ind,y1, width, label='Starting Salary')
        axis[0].bar(ind+width, y2, width,label='Mid-Career Salary')
        axis[0].set_xticks(ind+width/2)
        axis[0].set_xticklabels(x1)
        axis[0].set_ylim(0, 160000)
        axis[0].legend(loc='best')
        axis[0].set_title('Average Salary Vs Type')
        figure.tight_layout(pad=3.0)
        axis[1].set_title('Average Salary Vs Mid-Career Percentile Category')
        logging.debug('median salary graphs plotted successfully')

    #Reads in defaultdicts and plots a line graph for each school type which plots the defaultdict 10th, 25th, 75th, and 90th percentile avg values for each line
    def plot_type_spread(self):
        x1 = ['10th percentile', '25th percentile', '75th percentile', '90th percentile']
        y1 = [tenthAvg['Engineering'], twentyfifthAvg['Engineering'], seventyfifthAvg['Engineering'], ninetiethAvg['Engineering']]
        y2 = [tenthAvg['Party'], twentyfifthAvg['Party'], seventyfifthAvg['Party'], ninetiethAvg['Party']]
        y3 = [tenthAvg['Liberal Arts'], twentyfifthAvg['Liberal Arts'], seventyfifthAvg['Liberal Arts'], ninetiethAvg['Liberal Arts']]
        y4 = [tenthAvg['Ivy League'], twentyfifthAvg['Ivy League'], seventyfifthAvg['Ivy League'], ninetiethAvg['Ivy League']]
        y5 = [tenthAvg['State'], twentyfifthAvg['State'], seventyfifthAvg['State'], ninetiethAvg['State']]

        plt.plot(x1, y1, label = "Engineering", linestyle="-")
        plt.plot(x1, y2, label = "Party", linestyle="--")
        plt.plot(x1, y3, label = "Liberal Arts", linestyle="-.")
        plt.plot(x1, y4, label = "Ivy League", linestyle=":")
        plt.plot(x1, y5, label = "State", linestyle="--")
        plt.legend(loc='best')
        
        plt.legend()
        plt.savefig('final_testing_4.jpg')
        logging.debug('mid-career spread salary line graph plotted successfully')

def main():
    # Initializes SalaryData class
    saltype = SalaryData()
    saltype.plot_type_median()
    saltype.plot_type_spread()

if __name__ == '__main__':
    main()