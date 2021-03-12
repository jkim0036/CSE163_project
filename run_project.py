'''
CSE 163
James Chen, Julia Kim, Minjie Kim

A file that runs a script to examine changes in the
housing market over time. Produces graphs to answer
questions such as what isthe average % change of home
prices from 2016-2021, what is the average house price
and days on the market for a home in a specific county
and how has Covid-19 affected the housing price and days
on the market for homes in different counties.
'''

import pandas as pd
from solve_r3 import get_animation_data, plot_animation
from data_process import process_data
from RQ1 import transform_data, plot_timeseries
from r2 import wa_combine, filter_data, plot_data


def main():
    '''
    Runs the script to see results for the project for
    all 3 research questions.
    '''
    zillow_data = pd.read_csv('zillow_data.csv')
    realtor_data = pd.read_csv('realtor_historical.csv')
    new_data = process_data(zillow_data, realtor_data)

    # research question 1
    piv_table = transform_data(new_data)
    plot_timeseries(piv_table)

    # research question 2
    total_data = wa_combine(new_data)
    final_data = filter_data(total_data)
    plot_data(final_data)

    # research question 3
    animation_data = get_animation_data(new_data)
    plot_animation(animation_data)


if __name__ == '__main__':
    main()
