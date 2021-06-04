import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# define GradData class to handle loading and processing of recent_grads datafile
class GradData:

    FILE_PATH = './recent-grads.csv'

    # constructor for GradData object. Calls the load data function to read in data
    def __init__(self):
        self.load_data()

    def get_data(self):
        return self.data

    # Reads in the data from the recent-grads csv file. If the file doesn't exist, raises a file
    # not found error
    # saves the data to the data attribute
    def load_data(self):
        if not os.path.exists(self.FILE_PATH):
            raise FileNotFoundError('This file does not exist! Please try again.')
        else:
            self.data = pd.read_csv(self.FILE_PATH)

    # inputs: attribute to sort data by. Defaults to descending, but can be overriden.
    # sorts data class attribute based on inputted sort_by attribute. If attribute does not exist
    # raises an Index Error
    def sort_data(self, sort_by, order=False):
        if sort_by not in self.data.columns:
            raise IndexError(f'Column {sort_by} not found. Please try again')
        else:
            self.data = self.data.sort_values(by=[sort_by], ascending=order)

    # sorts the data based on Median salary in descending order, and creates a bar chart of the top
    # 10 majors by median salary
    def plot_top10_median_salary(self):
        self.sort_data('Median')
        x = self.data['Major'][:10]
        y = self.data['Median'][:10]
        plt.figure(figsize=(7, 8))
        plt.bar(x, y)
        self.__add_labels(x, y)
        plt.xlabel('Major')
        plt.ylabel('Median Salary')
        plt.title('Top 10 Median Salaries by College Major')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

    # helper function to add data labels to plots. Takes an x and y series as inputs
    def __add_labels(self, x, y):
        for i in x.index:
            plt.text(x[i], y[i], int(y[i]), ha='center')

    # sorts the data based on number of respondents in descending order, and creates a stakced bar
    # chart of the top 10 majors by number of respondents. Bars show respondents split by male and
    # female respondents.
    def plot_num_respondents_top10(self):
        self.sort_data('Total')
        x = self.data['Major'][:10]
        men = self.data['Men'][:10]
        women = self.data['Women'][:10]
        total = self.data['Total'][:10]
        plt.figure(figsize=(8, 7))
        plt.bar(x, men, label='men', color='navy')
        plt.bar(x, women, label='women', color='pink', bottom=men)
        self.__add_labels(x, total)
        plt.ylabel('Num Respondents')
        plt.xlabel('Major')
        plt.title('Num Respondents by Major (Top 10)')
        plt.xticks(rotation=60, ha='right')
        plt.legend(loc='upper right')
        plt.tight_layout()
        plt.show()

    # computes basic statistics of the data including shape of data (num of rows/columns), number
    # of major categories represented, and range of median salaries. Stores these statistics as class
    # attributes and prints a brief summary
    def get_stats(self):
        self.dims = self.data.shape
        self.num_cats = self.data['Major_category'].nunique()
        self.median_sal_range = (self.data["Median"].min(), self.data["Median"].max())
        print(f'''There are {self.dims[0]} rows and {self.dims[1]} columns in the dataset.
        \nThere are {self.num_cats} major categories represented.
        \nThe range of salaries is from ${self.median_sal_range[0]} to ${self.median_sal_range[1]}.''')

    # outputs a csv file of the top 10 majors by median salary. Output columns are major and median salary
    def get_csv_top10_salaries(self, output):
        self.sort_data('Median')
        x = self.data['Major'][:10]
        y = self.data['Median'][:10]
        pd.DataFrame({'Major': x, "Median_Salary": y}).to_csv(output)

    # outputs a csv file of the top 10 majors by number of respondents. Output columns are major,
    # total respondents, male respondenets, and female respondents
    def get_csv_top10_respondents(self, output):
        self.sort_data('Total')
        x = self.data['Major'][:10]
        men = self.data['Men'][:10]
        women = self.data['Women'][:10]
        total = self.data['Total'][:10]
        pd.DataFrame({'Major': x, 'Total_Respondents': total, "Men": men, 'Women': women}).to_csv(output)

# runs through the basic functionality of the GradData class if script is being run directly, 
# and not being imported as a module
if __name__ == '__main__':
    d = GradData()
    d.get_stats()
    d.plot_top10_median_salary()
    d.plot_num_respondents_top10()
