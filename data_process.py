'''
CSE 163
James Chen, Julia Kim, Minjie Kim

A file that contains a function to join the zillow
and realtor data.
'''

import pandas as pd


def process_data(zillow_data, realtor_data):
    '''
    Combines the zillow and realtor data on county and state name.
    Returns the combined data.
    '''
    zillow_data_clean = zillow_data
    zillow_data_clean['county_z'] = zillow_data_clean['RegionName']. \
        str.split(' County').str[0].str.lower()

    realtor_data_clean = realtor_data
    realtor_data_clean['county_r'] = realtor_data_clean['county_name']. \
        str.split(', ').str[0].str.lower()
    realtor_data_clean['state_r'] = realtor_data_clean['county_name']. \
        str.split(', ').str[1].str.upper()

    combined = pd.merge(zillow_data_clean,
                        realtor_data_clean,
                        how='outer',
                        left_on=['county_z', 'StateName'],
                        right_on=['county_r', 'state_r'])

    x = combined.loc[:, '1996-01-31':'2021-01-31']
    y = combined.loc[:, ['month_date_yyyymm', 'median_listing_price',
                         'active_listing_count', 'median_days_on_market',
                         'total_listing_count', 'county_r', 'state_r']]
    both = pd.concat([x, y], axis=1)
    return both
