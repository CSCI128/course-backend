import csv
import math
import pandas as pd

# load the runestone stuff
runestone = input("Enter Runestone gradebook filename: ")
runestoneDF = pd.read_csv(runestone)

# drop due date, points, and class average rows (we just want user data)
runestoneDF = runestoneDF.drop([0, 1, 2])

# load gradebook stuff
gradebook = input("Enter Canvas gradebook filename: ")
gradebookDF = pd.read_csv(gradebook)
gradebookDF = gradebookDF.drop([0])

for row in gradebookDF['SIS User ID']:
  if not math.isnan(float(row)): # filter out from test student
    found_user_row = runestoneDF.loc[runestoneDF['UName'] == "mines_" + str(int(row))]

    if not found_user_row[['Week 1 Readings']].empty:
      # TODO do something with this value
      raw_grade = found_user_row[['Week 1 Readings']].values[0][0]

      print(raw_grade)
      
      final_grade = 0

      gradebookDF['Week 1 Readings (344225)'] = final_grade

# TODO export gradebook properly
gradebookDF.to_csv('test.csv')
