'''
CSE 163
James Chen, Julia Kim, Minjie Kim

A file that tests the functions in solve_r3 to verify
that the data processing is correct.
'''

import pandas as pd
from r2 import match_date_to_column
from data_process import process_data


def assert_equals(first, second):
    '''
    Checks to see if the first value is equivalent to the
    second. Prints out error messages if they are unequal.
    '''
    if first != second:
        print("expected: " + str(second))
        print("received: " + str(first))


def test_val(data):
    '''
    Tests multiple rows in the r3_data.csv dataset to
    make sure that the total average between the zillow
    average price and the realtor median price is correct.
    '''
    avg_zillow = data.loc[0, 'zillow_avg_price']
    avg_realtor = data.loc[0, 'median_listing_price']
    total_avg = data.loc[0, 'avg_price']
    assert_equals((avg_zillow + avg_realtor) / 2, total_avg)
    avg_zillow = data.loc[500, 'zillow_avg_price']
    avg_realtor = data.loc[500, 'median_listing_price']
    total_avg = data.loc[500, 'avg_price']
    assert_equals((avg_zillow + avg_realtor) / 2, total_avg)
    avg_zillow = data.loc[346, 'zillow_avg_price']
    avg_realtor = data.loc[346, 'median_listing_price']
    total_avg = data.loc[346, 'avg_price']
    assert_equals((avg_zillow + avg_realtor) / 2, total_avg)


def test_match_date(data):
    '''
    Tests multiple dates to check that the
    match date apply function in solve_r3.py is
    finding the correct values.
    '''
    row = data.loc[0]
    return_date = match_date_to_column(row, data)
    assert_equals(return_date, 715152.0)
    row = data.loc[56]
    return_date = match_date_to_column(row, data)
    assert_equals(return_date, 267536.0)
    row = data.loc[112]
    return_date = match_date_to_column(row, data)
    assert_equals(return_date, 210332.0)


def main():
    zillow_data = pd.read_csv('zillow_data.csv')
    realtor_data = pd.read_csv('realtor_historical.csv')
    data = process_data(zillow_data, realtor_data)
    data['index'] = data.index
    test_match_date(data)
    processed_data = pd.read_csv('r2_data.csv')
    test_val(processed_data)


if __name__ == '__main__':
    main()
