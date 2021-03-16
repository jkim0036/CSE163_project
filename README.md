# CSE 163 Project

How to run our project:
Simple! We have created a main file called "run_project.py" that pulls
all our research questions and code together. By running this file, it
runs all the main files needed to run our project. This should produce
3 different graphs that hold information answering our research questions.

How to get our datasets:
We are using data from Realtor (https://www.realtor.com/research/data/).  To get the datasets that we are using, go to the Inventory Monthly - historical data download the dataset under county. (Note: realtor updates their datasets fairly often so the dataset you get from this website will be a little different from the dataset that we used. You can access the dataset we used at our Github repository: https://github.com/jkim0036/CSE163_project/blob/main/realtor_historical.csv )

We are also using data from Zillow (https://www.zillow.com/research/data/).  To get the dataset that we are using, go to the Home Values section under Housing Data and under data type choose: ZHVI (SFR, Condo/Co-op) Time series, Smoothed, Seasonally Adjusted($) and under geography choose: County and download to get dataset.

We also used the census tract files and food-access.csv from Take Home Assessment 5 to graph our results for our second research question.

Setup to run:
Depending on the setup of your environment and what libriaries are already
pre-existing, you may need to install a couple libraries to run our project,
but this is based on a case by case basis.

Libraries that we used that you may have to install are:
- pandas
- plotly graphing opjects (plotly.graph_objs, plotly.express)
- datetime
- math
- urlopen
- json
- geopandas
- calendar

To download these libraries, you can do it all locally on your machine
on Anaconda or through the Terminal.

These should be all the libraries needed to run our project.
As for datasets that we used, this is all included in our github repo
so there should be no need to download any files/data to run our project.


Other than that, you should be good to go to run our project and see the
graphs that we created! From these individual graphs, you will see information
that will help answer our research questions.

The link to our overall repository: https://github.com/jkim0036/CSE163_project
