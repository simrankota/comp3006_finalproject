import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class GradData:
    def __init__(self):
        self.load_data()

    def load_data(self):
        self.data = pd.read_csv('./recent-grads.csv')

    def sort_data(self, sort_by):
        if sort_by not in self.data.columns:
            raise IndexError(f'Column {sort_by} not found. Please try again')
        else:
            self.data = self.data.sort_values(by=[sort_by], ascending=False)

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

    def __add_labels(self, x, y):
        for i in range(len(x)):
            plt.text(i, y[i], y[i], ha='center')

    def plot_num_respondents_top10(self):
        self.sort_data('Total')
        x = self.data['Major'][:10]
        men = self.data['Men'][:10]
        women = self.data['Women'][:10]
        plt.figure(figsize=(7, 6))
        plt.bar(x, men, label='men', color='navy')
        plt.bar(x, women, label='women', color='pink', bottom=men)
        plt.ylabel('Num Respondents')
        plt.xlabel('Major')
        plt.title('Num Respondents by Major (Top 10)')
        plt.xticks(rotation=60, ha='right')
        plt.legend(loc='upper right')
        plt.tight_layout()
        plt.show()

    def get_stats(self):
        self.dims = self.data.shape
        self.num_cats = self.data['Major_category'].nunique()
        self.median_sal_range = (self.data["Median"].min(), self.data["Median"].max())
        print(f'''There are {self.dims[0]} rows and {self.dims[1]} columns in the dataset.
        \nThere are {self.num_cats} major categories represented.
        \nThe range of salaries is from ${self.median_sal_range[0]} to ${self.median_sal_range[1]}.''')

    def get_csv_top10_salaries(self):
        self.sort_data('Median')
        x = self.data['Major'][:10]
        y = self.data['Median Salary'][:10]
        pd.DataFrame({'Major': x, "Median": y}).to_csv('top_10_median_salaries.csv')

    def get_csv_top10_respondents(self):
        self.sort_data('Total')
        x = self.data['Major'][:10]
        men = self.data['Men'][:10]
        women = self.data['Women'][:10]
        total = self.data['Total'][:10]
        pd.DataFrame({'Major': x, 'Total': total, "Men": men, 'Women': women}).to_csv('top_10_respondents.csv')

if __name__ == '__main__':
    d = GradData()
    # d.get_stats()
    # d.plot_top10_median_salary()
    # d.plot_num_respondents_top10()
    d.get_csv_top10_respondents()
