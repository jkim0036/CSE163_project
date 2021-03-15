"""
CSE 163
James Chen, Julia Kim, Minjie Kim

This file calculates the median house prices from
month to month for the years 2016 - Jan 2021.
The price changes are graphed on a time series plot for
each state.
"""
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime
import math
from solve_r3 import match_date_to_column


def reformat_date(date):
    if math.isnan(date):
        return math.nan
    year = int(date // 100)
    month = "{:02d}".format(int(date % 100))
    date = datetime(year, int(month), 1)
    return date.strftime('%Y-%m')


def _listing_price(arg, data):
    if math.isnan(arg.zillow_avg_price):
        return arg.median_listing_price
    elif math.isnan(arg.median_listing_price):
        return arg.zillow_avg_price
    else:
        return (arg.median_listing_price + arg.zillow_avg_price) / 2


def transform_data(data):
    dates = data.loc[:, '2016-01-31':'2021-01-31']
    prices = data.loc[:, ['month_date_yyyymm', 'median_listing_price',
                      'state_r']]
    rq1 = pd.concat([dates, prices], axis=1)
    rq1['index'] = rq1.index
    rq1['zillow_avg_price'] = rq1.apply(match_date_to_column, data=rq1, axis=1)
    rq1 = rq1.loc[:, 'month_date_yyyymm':'zillow_avg_price']
    rq1['month_date_yyyymm'] = rq1['month_date_yyyymm'].apply(reformat_date)
    rq1['median_price_zr'] = rq1.apply(_listing_price, data=rq1, axis=1)
    rq1 = rq1.sort_values('month_date_yyyymm')
    rq1 = rq1.loc[:, ['month_date_yyyymm', 'state_r', 'median_price_zr']]
    rq1 = rq1.rename(columns={'month_date_yyyymm': 'date', 'state_r': 'State'})
    rq1 = rq1.set_index('date')
    return pd.pivot_table(rq1, values='median_price_zr', columns='State',
                          index='date')


def plot_timeseries(data):
    cols = list(data.columns)
    # Sets for list comprehension for graph legends
    far_west = set(['WA', 'OR', 'CA', 'NV', 'HI', 'AK'])
    rocky_mt = set(['ID', 'MT', 'WY', 'UT', 'CO'])
    sw = set(['AZ', 'NM', 'TX', 'OK'])
    plains = set(['ND', 'SD', 'NE', 'KS', 'MN', 'IA', 'MO'])
    great_lakes = set(['WI', 'IL', 'IN', 'MI', 'OH'])
    se = set(['AR', 'LA', 'KY', 'TN', 'MS', 'AL', 'GA', 'FL', 'WV', 'VA', 'NC',
              'SC'])
    me = set(['PA', 'NY', 'NJ', 'DE', 'MD'])
    ne = set(['ME', 'NH', 'VT', 'MA', 'RI', 'CT'])
    tech = set(['CO', 'WA', 'WI', 'VA', 'NC', 'MA', 'NY', 'CA', 'MI'])
    # Start figure
    fig = go.Figure()
    for state in cols:
        fig.add_trace(
            go.Scatter(
                mode='lines+markers',
                x=data.index,
                y=data[state],
                name=state
            )
        )

    fig.update_layout(
        width=1500,
        height=900,
        title_text='Median House Prices (month to month) \
                    from 2016 -2021',
        xaxis_title='Date',
        yaxis_title='Price in USD'
    )

    fig.update_layout(
        updatemenus=[
                    dict(
                        buttons=list([
                            dict(
                                method='restyle',
                                label='All',
                                args=[{'visible': [True for state in
                                                   range(len(cols))]},
                                      {'showlegend': True}]
                            ),
                            dict(
                                method='restyle',
                                label='Far West',
                                args=[{'visible': [True if state in far_west
                                                   else False for state in
                                                   cols]},
                                      {'showlegend': True}]
                            ),
                            dict(
                                method='restyle',
                                label='Rocky Mountains',
                                args=[{'visible': [True if state in rocky_mt
                                                   else False for state in
                                                   cols]},
                                      {'showlegend': True}]
                            ),
                            dict(
                                method='restyle',
                                label='Southwest',
                                args=[{'visible': [True if state in sw else
                                                   False for state in cols]},
                                      {'showlegend': True}]
                            ),
                            dict(
                                method='restyle',
                                label='Plains',
                                args=[{'visible': [True if state in plains else
                                                   False for state in cols]},
                                      {'showlegend': True}]
                            ),
                            dict(
                                method='restyle',
                                label='Great Lakes',
                                args=[{'visible': [True if state in great_lakes
                                                   else False for state in
                                                   cols]},
                                      {'showlegend': True}]
                            ),
                            dict(
                                method='restyle',
                                label='Southeast',
                                args=[{'visible': [True if state in se else
                                                   False for state in cols]},
                                      {'showlegend': True}]
                            ),
                            dict(
                                method='restyle',
                                label='Mideast',
                                args=[{'visible': [True if state in me else
                                                   False for state in cols]},
                                      {'showlegend': True}]
                            ),
                            dict(
                                method='restyle',
                                label='New England',
                                args=[{'visible': [True if state in ne else
                                                   False for state in cols]},
                                      {'showlegend': True}]
                            ),
                            dict(
                                method='restyle',
                                label='Tech Hub',
                                args=[{'visible': [True if state in tech else
                                                   False for state in cols]},
                                      {'showlegend': True}]
                            )
                        ]),
                    )
        ]
    )
    fig.write_html("r1.html")
    fig.show()
