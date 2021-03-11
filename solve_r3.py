from data_process import process_data
from calendar import monthrange
import math
import plotly.express as px
import pandas as pd


def plot_animation(plot_data):
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
    plot.write_html("graph.html")


def match_date_to_column(arg, data):
    '''
    Matches...
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


def filter_data(data):
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


def main():
    zillow_data = pd.read_csv('zillow_data.csv')
    realtor_data = pd.read_csv('realtor_historical.csv')
    new_data = process_data(zillow_data, realtor_data)
    plot_data = filter_data(new_data)
    plot_animation(plot_data)


if __name__ == '__main__':
    main()
