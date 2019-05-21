# RescueForest: Predicting Emergency Response with Random Forests

I'm finishing up the material in the fast.ai '[Introduction to ML](http://course18.fast.ai/ml)' course and it has been fantastic. The learning philosophy, which the instructor Jeremy describes as a top-down approach, worked really well for my learning style. The general idea is that you learn HOW to do ML before you learn WHY it works - the same way you learn HOW to play baseball before learning WHY you might use one particular strategy at a given time.

I wanted to do a small capstone project to practice and solidify what I learned, and decided to study emergency response prediction - particularly for an organization called [King County Search and Rescue](http://www.kingcountysar.org/) (SAR), which I volunteer as a member of. We do a variety of rescue missions, but the most common call is to help injured or lost hikers in the wilderness surrounding Seattle. It's mostly a volunteer-run organization, so resources are inherently limited. Having a method to predict the likelihood of a call on any given day might help us prioritize resources and preparation to best serve the community.

I broke the project into three general steps covered in the course:
1. Data Exploration and cleaning
2. Building a simple model and using it to study feature importance
3. Feature engineering and tuning the model

This post will cover my general approach and findings. Detailed code and notebooks can be found in my project's [repo](https://github.com/afederation/SAR_predict).

## Data Exploration, Cleaning

Before building the model, I want to understand the nature of the data we have. There are several data sources we're using, and we'll be linking all of them together by the date. Python's [datetime](https://docs.python.org/2/library/datetime.html) library was key for this and made these operations much easier.

### Outcome Data

The goal of the project was to predict whether or not a SAR call happened on a particular day. I've downloaded this from the organization's internal database and removed some information for privacy. Loading the data into python and pandas allows for some simple plots to make sure we're focusing on the most relevent data. I had to focus dates into a range from 2002 to current date, since the data before this was incomplete.

Some exploratory plots show that we have calls on 29% of days, which means the data is somewhat imbalanced, but not horribly so. Calls happen most frequently on weekends and in the summer. We know this by intuition, and the data backs this up. This also shows that there is probably some information in the date alone that may have some predictive power.

______plots

Lastly, to get a tidy dataset, we need to create a table with every date in the range we're considering and give a boolean that reports on the presence/absence of a call on that day. A simple script to convert the raw `sar_data` into a `clean_table` accomplished this by taking advantage of the panda's date_range function.

```python
date_range = pd.date_range(start='1/1/2002', end='4/01/2019')
clean_table = []
for d in date_range:
    if sar_data.date.isin([d]).any(): # check if date in in table containing all calls
        clean_table.append([d,1])
    else:
        clean_table.append([d,0])               
sar_clean = pd.DataFrame(clean_table)
sar_clean.columns = ['date','mission']
```

### Features

To start, we'll focus on extracting features from the dates and integrate some weather information from NOAA. Later on, we'll see if adding additional features including Google Trends and holiday information helps improve the model.



## Feature Engineering
