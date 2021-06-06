# Final Project: College Choices vs Expected Salary Analysis

## Group Members
Arun Joseph, Navan Powers, and Simran Kota

<br /> <br />

## Research Question
How do different college education paths affect salary?
<br /> <br />

## Datasets utilized
We will be analyzing data sets for recent graduates that include location, type of college, and major obtained from https://www.Kaggle.com/

<br /> <br />

## Analysis Conclusion
Petroleum Engineering overall seemed to be the major with the highest median salary. Ivy League colleges seemed to have the highest range of salaries (difference between 10th percentile and 90th percentile), and they also had the highest difference between the starting salary and mid-career salary. However, they also had the highest overall starting salary. Similarly, California seemed to have the highest mid-career salary, although it was very close to northeastern for starting salary. This is likely due to the large number of ivies in the northeastern region. The northeastern region had the highest delta between starting salary and mid-career.
<br /> <br />

## Usage
*python3 final_analysis.py plot <**args**>*

### Dependencies
package dependencies listed in requirements.txt

### [command]

**plot**: plots various charts

### [optional arguments]

-**i**: plot initial EDA (exploratory data analysis) plots for recent_grads.csv, salaries_by_college_type.csv, and salaries_by_region.csv

-**o** *file name*: output file to store csv data associated with final plots

-**f** *major category*: plot final geoplot exploring schools by location, median starting salary, and type, as well as barchart showing top 5 schools and majors for an inputted major category. Major category input is REQUIRED. Options are 'Education', 'Psychology & Social Work', 'Biology & Life Science', 'Arts', 'Humanities & Liberal Arts', 'Health', 'Industrial Arts & Consumer Services', 'Agriculture & Natural Resources', 'Social Science', 'Communications & Journalism', 'Business', 'Law & Public Policy', 'Physical Sciences', 'Computers & Mathematics', 'Interdisciplinary', 'Engineering'