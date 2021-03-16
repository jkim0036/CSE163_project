'''
CSE 163
James Chen, Julia Kim, Minjie Kim

A file that gives insight into the housing market in
Washington State for each month based on historical
data from Zillow and Realtor. This pulls together
various datasets and culminates in a plot of Washington
counties with the ability to hover over a month and see
information regarding average days on the market and price
for a typical home in that county.
'''

from urllib.request import urlopen
import json
import pandas as pd
import geopandas as gpd
import plotly.express as px
import math
from solve_r3 import match_date_to_column

with urlopen('https://raw.githubusercontent.com/' +
             'plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)


def get_month(date):
    '''
    Returns the month formatted in mm format.
    Will return NaN if the date given is NaN.
    '''
    if math.isnan(date):
        return math.nan
    month = "{:02d}".format(int(date % 100))
    return month


def wa_combine(combined_data):
    '''
    Combines washington data with zillow/realtor data and
    adds columns for zillow average price, month, and county.
    Returns the combined data.
    '''
    combined_data['index'] = combined_data.index
    combined_data['zillow_avg_price'] = combined_data.apply(
                                            match_date_to_column,
                                            data=combined_data,
                                            axis=1)
    combined_data = combined_data.drop(combined_data.loc[:,
                                       '1996-01-31':'2021-01-31'].columns,
                                       axis=1)

    combined_data['month'] = combined_data['month_date_yyyymm'].apply(
                                                                get_month)

    wa_county = combined_data[combined_data['state_r'] == 'WA']

    shape = gpd.read_file('tl_2010_53_tract00/tl_2010_53_tract00.shp')
    csv = pd.read_csv('food-access.csv')
    merged_left = shape.merge(csv, left_on='CTIDFP00',
                              right_on='CensusTract', how='left')

    filter_wa = merged_left.loc[:, ['STATEFP00',
                                    'COUNTYFP00',
                                    'State',
                                    'County']]
    filter_wa['County'] = filter_wa['County'].str.lower()

    final_data = pd.merge(wa_county,
                          filter_wa,
                          how='left',
                          left_on=['county_r', 'state_r'],
                          right_on=['County', 'State'])

    return final_data


def filter_data(final_data):
    '''
    Filters the data passed in to be plotted by adding
    FIPS, avg_price, County, and month columns.
    Returns the filtered data.
    '''
    final_data['FIPS'] = final_data['STATEFP00'] + final_data['COUNTYFP00']
    final_data = final_data.drop(['STATEFP00',
                                  'COUNTYFP00',
                                  'county_r',
                                  'state_r'], axis=1)
    final_data['avg_price'] = (final_data['median_listing_price'] +
                               final_data['zillow_avg_price']) / 2
    final_data = final_data.sort_values(by=['month'])
    final_data = final_data.drop(['month_date_yyyymm', 'active_listing_count',
                                  'total_listing_count', 'index',
                                  'zillow_avg_price', 'State',
                                  'median_listing_price'], axis=1)

    group = final_data.groupby(['FIPS',
                                'month',
                                'County'])[['median_days_on_market',
                                           'avg_price']].mean()

    group['County'] = group.index.get_level_values('County')
    group['FIPS'] = group.index.get_level_values('FIPS')
    group['month'] = group.index.get_level_values('month')

    return group


def plot_data(group):
    '''
    Plots the data and saves it to a file name r2.html.
    '''
    fig = px.choropleth(group, geojson=counties,
                        facet_col="month",
                        facet_col_wrap=3,
                        locations='FIPS',
                        hover_data=['median_days_on_market',
                                    'avg_price', 'County'])
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(title_text='Real Estate Market in Washington by Month')
    fig.write_html("r2.html")
    fig.show()
