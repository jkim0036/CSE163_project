import pandas as pd
import geopandas as gpd
import plotly.express as px
import json
import math
from calendar import monthrange

from urllib.request import urlopen
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)


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


def get_month(date):
    if math.isnan(date):
        return math.nan
    month = "{:02d}".format(int(date % 100))
    return month


zillow_data = pd.read_csv('zillow_data.csv')
realtor_data = pd.read_csv('realtor_historical.csv')

zillow_data_clean = zillow_data
zillow_data_clean['county_z'] = zillow_data_clean['RegionName'].str.split(' County').str[0].str.lower()

realtor_data_clean = realtor_data
realtor_data_clean['county_r'] = realtor_data_clean['county_name'].str.split(', ').str[0].str.lower()
realtor_data_clean['state_r'] = realtor_data_clean['county_name'].str.split(', ').str[1].str.upper()

combined = pd.merge(zillow_data_clean,
                    realtor_data_clean,
                    how='outer',
                    left_on=['county_z','StateName'],
                    right_on = ['county_r','state_r'])

x = combined.loc[:, '1996-01-31':'2021-01-31']
y = combined.loc[:, ['month_date_yyyymm', 'median_listing_price', 'active_listing_count', 'median_days_on_market', 'total_listing_count', 'county_r', 'state_r']]
both = pd.concat([x, y], axis=1)

both['index'] = both.index
both['zillow_avg_price'] = both.apply(match_date_to_column, data=both,
                                          axis=1)
both = both.drop(both.loc[:, '1996-01-31':'2021-01-31'].columns,
                     axis=1)

both['month'] = both['month_date_yyyymm'].apply(get_month)

wa_county = both[both['state_r'] == 'WA']

shape = gpd.read_file('tl_2010_53_tract00/tl_2010_53_tract00.shp')
csv = pd.read_csv('food-access.csv')
merged_left = shape.merge(csv, left_on='CTIDFP00',
                          right_on='CensusTract', how='left')

filter_wa = merged_left.loc[:, ['STATEFP00', 'COUNTYFP00', 'State', 'County']]
filter_wa['County'] = filter_wa['County'].str.lower()

final_data = pd.merge(wa_county,
                    filter_wa,
                    how='left',
                    left_on=['county_r','state_r'],
                    right_on = ['County','State'])

final_data['FIPS'] = final_data['STATEFP00'] + final_data['COUNTYFP00']
final_data = final_data.drop(['STATEFP00', 'COUNTYFP00', 'county_r', 'state_r'], axis=1)
final_data['avg_price'] = (final_data['median_listing_price'] + final_data['zillow_avg_price']) / 2
final_data = final_data.sort_values(by=['month'])
final_data = final_data.drop(['month_date_yyyymm', 'active_listing_count', 'total_listing_count', 'index', 'zillow_avg_price', 'State', 'median_listing_price'], axis=1)

group = final_data.groupby(['FIPS', 'month', 'County'])['median_days_on_market', 'avg_price'].mean()

group['County'] = group.index.get_level_values('County')
group['FIPS'] = group.index.get_level_values('FIPS')
group['month'] = group.index.get_level_values('month')

# print(group)

fig = px.choropleth(group, geojson=counties, facet_col="month", facet_col_wrap=3,
                    locations='FIPS',
                    hover_data=['median_days_on_market', 'avg_price', 'County'])
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(title_text = 'Monthly Home Report in Washington by County')
fig.show()