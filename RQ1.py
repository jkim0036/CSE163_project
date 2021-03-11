import pandas as pd
import plotly.graph_objs as go
from calendar import monthrange
from datetime import datetime
import math


def combine_data(zillow, realtor):
    zillow_data_clean = zillow
    zillow_data_clean['county_z'] = zillow_data_clean['RegionName'].str.split(' County').str[0].str.lower()
    realtor_data_clean = realtor
    realtor_data_clean['county_r'] = realtor_data_clean['county_name'].str.split(', ').str[0].str.lower()
    realtor_data_clean['state_r'] = realtor_data_clean['county_name'].str.split(', ').str[1].str.upper()

    combined = pd.merge(zillow_data_clean,
                        realtor_data_clean,
                        how='outer',
                        left_on=['county_z', 'StateName'],
                        right_on=['county_r', 'state_r'])

    x = combined.loc[:, '1996-01-31':'2021-01-31']
    y = combined.loc[:, ['month_date_yyyymm', 'median_listing_price', 'active_listing_count', 'median_days_on_market', 'total_listing_count', 'county_r', 'state_r']]
    return pd.concat([x, y], axis=1)


def reformat_date(date):
    if math.isnan(date):
        return math.nan
    year = int(date // 100)
    month = "{:02d}".format(int(date % 100))
    date = datetime(year, int(month), 1)
    return date.strftime('%Y-%m')


def match_date_to_column(arg, data):
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


def listing_price(arg, data):
    if math.isnan(arg.zillow_avg_price):
        return arg.median_listing_price
    elif math.isnan(arg.median_listing_price):
        return arg.zillow_avg_price
    else:
        return (arg.median_listing_price + arg.zillow_avg_price) / 2


def transform_data(data):
    dates = data.loc[:, '2016-01-31':'2021-01-31']
    prices = data.loc[:, ['month_date_yyyymm', 'median_listing_price', 'state_r']]
    rq1 = pd.concat([dates, prices], axis=1)
    rq1['index'] = rq1.index
    rq1['zillow_avg_price'] = rq1.apply(match_date_to_column, data=rq1, axis=1)
    rq1 = rq1.loc[:, 'month_date_yyyymm':'zillow_avg_price']
    rq1['month_date_yyyymm'] = rq1['month_date_yyyymm'].apply(reformat_date)
    rq1['median_price_zr'] = rq1.apply(listing_price, data=rq1, axis=1)
    rq1 = rq1.dropna()
    rq1 = rq1.sort_values('month_date_yyyymm')
    rq1['%_change_mm'] = rq1['median_price_zr'].pct_change()
    rq1['%_change_mm'] = rq1['%_change_mm'].fillna(0)
    rq1 = rq1.loc[:, ['month_date_yyyymm', 'state_r', '%_change_mm']]
    rq1 = rq1.rename(columns={'month_date_yyyymm': 'date', 'state_r': 'State'})
    rq1 = rq1.set_index('date')
    return pd.pivot_table(rq1, values='%_change_mm', columns='State', index='date')


def plot_data(data):
    fig = go.Figure()
    for column in list(data.columns):
        fig.add_trace(
            go.Scatter(
                mode='lines+markers',
                x=data.index,
                y=data[column],
                name=column
            )
        )

    fig.update_layout(
        width=1500,
        height=900,
        title_text='Percent Change on Median House Prices (month to month) from 2016 -2021',
        xaxis_title='Date',
        yaxis_title='Percent Change'
    )

    fig.update_layout(
        updatemenus=[
            dict(
                buttons=list([
                    dict(
                        method='restyle',
                        label='Far West',
                        args=[{'y': [data['WA'], data['OR'], data['CA'], data['NV'], data['HI']]},
                              {'showlegend':True}]
                    ),
                    dict(
                        method='restyle',
                        label='Rocky Mountain',
                        args=[{'y': [data['ID'], data['MT'], data['WY'], data['UT'], data['CO']]},
                              {'showlegend':True}]
                    ),
                    dict(
                        method='restyle',
                        label='Southwest',
                        args=[{'y': [data['AZ'], data['NM'], data['TX'], data['OK']]},
                              {'showlegend':True}]
                    ),
                    dict(
                        method='restyle',
                        label='Plains',
                        args=[{'y': [data['ND'], data['SD'], data['NE'], data['KS'], data['MN'], data['IA'], data['MO']]},
                              {'showlegend':True}]
                    ),
                    dict(
                        method='restyle',
                        label='Great Lakes',
                        args=[{'y': [data['WI'], data['IL'], data['IN'], data['OH'], data['MI']]},
                              {'showlegend':True}]
                    ),
                    dict(
                        method='restyle',
                        label='Southeast',
                        args=[{'y': [data['AR'], data['MS'], data['AL'], data['GA'], data['FL'], data['TN'], data['KY'], data['WV'], data['VA'], data['NC'], data['SC']]},
                              {'showlegend':True}]
                    ),
                    dict(
                        method='restyle',
                        label='Mideast',
                        args=[{'y': [data['NY'], data['PA'], data['NJ'], data['DE'], data['MD']]},
                              {'showlegend':True}]
                    ),
                    dict(
                        method='restyle',
                        label='New England',
                        args=[{'y': [data['NH'], data['ME'], data['VT'], data['MA'], data['RI'], data['CT']]},
                              {'showlegend':True}]
                    )
                ]),
            )
        ]  
    )

    fig.show()  
      

def main():
    zillow_data = pd.read_csv('zillow.csv')
    realtor_data = pd.read_csv('realtor_historical_project.csv')
    rq1 = combine_data(zillow_data, realtor_data)
    rq1 = transform_data(rq1)
    plot_data(rq1)


if __name__ == '__main__':
    main()
