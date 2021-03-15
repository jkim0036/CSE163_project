'''
CSE 163
James Chen, Julia Kim, Minjie Kim

A file that tests the if percent change was calculated correctly
in rq1
'''
import pandas as pd
from data_process import process_data
from RQ1 import transform_data


def test_pct_change(data, test_data):
    test = list(test_data['WA'])
    test = test.reverse()
    testing = list(data['WA'])
    testing = testing[41:54]
    length = len(testing)
    for i in range(0, length):
        diff = test[i] - testing[i]
        if (diff > 0.015) | (diff < -0.015):
            return False
    return True


def main():
    zillow_data = pd.read_csv('zillow_data.csv')
    realtor_data = pd.read_csv('realtor_historical.csv')
    data = process_data(zillow_data, realtor_data)
    data = transform_data(data)
    test_data = pd.read_csv('test_rq1.csv')
    works = test_pct_change(data, test_data)
    if works:
        print('All is good!')
    else:
        print('Almost there :(')


if __name__ == '__main__':
    main()
