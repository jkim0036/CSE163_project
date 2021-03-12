'''
CSE 163
James Chen, Julia Kim, Minjie Kim

A file that examines the changes of house prices and
days on the market for houses in each county in the
United States over the course of the pandemic (2019-2020)
by parsing data and plotting an animated graph to show
the results.
'''

from calendar import monthrange
import math
import plotly.express as px


def plot_animation(plot_data):
    '''
    Plots an animated graph showing the changes in house
    prices and days on the market
    over the period of the pandemic (2019-2020).
    '''
    # inverse data to get dates from 2019-2020
    plot_data = plot_data.iloc[::-1]
    plot = px.scatter(plot_data,
                      x="median_days_on_market", y="total_avg",
                      animation_frame="date_reformat",
                      animation_group="county_r",
                      color="state_r", hover_name="county_r",
                      size="active_listing_count",
                      size_max=55, range_x=[10, 670],
                      title="Housing Market Affected by COVID",
                      labels={"state_r": "State",
                              "median_days_on_market": "Median Days on Market",
                              "total_avg": "Average House Price",
                              "date_reformat": "Current Date ",
                              "active_listing_count": "Active Listing Count"},
                      range_y=[60000, 1600000])
    plot.update_layout(title={'x': 0.5, 'xanchor': 'center'})
    plot.write_html("r3.html")
    plot.show()


def match_date_to_column(arg, data):
    '''
    Matches the date in the column 'month_date_yyyymm' in the
    given row arg to the column name with the same date and
    returns the zillow average house price at that date.
    Will return NaN if the date in the 'month_date_yyyymm'
    column for the given row is NaN.
    '''
    if math.isnan(arg.month_date_yyyymm):
        return math.nan
    date = arg.month_date_yyyymm
    row_num = arg['index']
    year = int(date // 100)
    month = int(date % 100)
    num_days = monthrange(year, month)[1]
    month = "{:02d}".format(int(date % 100))
    full_date = str(year) + '-' + month + '-' + str(num_days)
    return data.loc[row_num, full_date]


def reformat_date(date):
    '''
    Reformats the given date in a MM/YYYY format.
    Will return NaN if the date given is NaN.
    '''
    if math.isnan(date):
        return math.nan
    year = int(date // 100)
    month = "{:02d}".format(int(date % 100))
    return month + '/' + str(year)


def get_animation_data(data):
    '''
    Filters and alters the combined zillow and realtor data from
    data_process.py to make it useful to solving research question 3.
    '''
    data['index'] = data.index
    data['zillow_avg_price'] = data.apply(match_date_to_column, data=data,
                                          axis=1)
    data = data.drop(data.loc[:, '1996-01-31':'2021-01-31'].columns,
                     axis=1)
    data['date_reformat'] = data['month_date_yyyymm'].apply(reformat_date)
    covid_years = (data['month_date_yyyymm'] // 100 == 2019) | \
        (data['month_date_yyyymm'] // 100 == 2020)

    data = data[covid_years]
    price_cols = data.loc[:, ['median_listing_price',
                              'zillow_avg_price']]
    data['total_avg'] = price_cols.mean(axis=1)
    data = data.sort_values(by=['state_r', 'month_date_yyyymm'],
                            ascending=[False, False])
    data.to_csv('r3_data.csv')
    return data
