from grads_data import GradData
import matplotlib.pyplot as plt
import argparse


def main():
    parser = argparse.ArgumentParser(
        description='analyze various data sets related to expected salaries based on college region, type, and major'
    )

    parser.add_argument('command', metavar='<command>', type=str, help='command to execute', default='plot')
    parser.add_argument('-o', '--ofile', metavar='<outfile>', dest='output', action='store')
    parser.add_argument('-g', '--grads_data', metavar='<plot name>', dest='plot_grads_data', choices=['median_salary', 'num_respondents'])
    args = parser.parse_args()
    
    gd = GradData()
    
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
    main()