# Backup Runestone Grading Script
# Grades based on the "Chapter Activity" CSV export
import math
import pandas as pd

runestone = input("Enter Runestone chapter activity gradebook filename: ")
runestoneDF = pd.read_csv(runestone)
runestoneDF = runestoneDF.drop(runestoneDF.columns[0], axis=1)

# storing points for each activity as { row_index: [chapter_id, points] }
activity_points: dict = {}
for (columnName, columnData) in runestoneDF['chapter_label'].items():
    chapter_id: str = str(columnData).split(" ")[0]
    points: float = float(str(columnData).split(" ")[-1].replace(')', '').replace('(', ''))
    activity_points.update({ chapter_id: [int(columnName), points] })

# TODO make this taken in via the terminal or something
ASSIGNMENT = ['1.1', '1.2', '1.3', '1.4', '1.5', '1.6', '1.7', '1.8', '1.9', '1.10', '1.11', '1.12', '1.13', '1.14'
        '2.1', '2.2', '2.3', '2.4', '2.5', '2.6', '2.7', '2.8', '2.9', '2.10', '2.11', '2.12', '2.13' ]

# Find maximum points
points_maximum = 0
for k, v in activity_points.items():
    if str(k) in ASSIGNMENT:
        points_maximum += v[1]

# formatted { studentName: score }
students: dict = {}

# get students from df
for (columnName, columnData) in runestoneDF.items():
    if columnName != 'chapter_label':
        points = 0
        for k, v in activity_points.items():
            for i in range(0, len(columnData.values)):
                if i == v[0] and str(k) in ASSIGNMENT and columnData.values[i] != ' ':
                    points += float(columnData.values[i])

        score = (points / points_maximum) * 100
        students.update({ str(columnName).replace('<br>', ' '): score })

file = open('output.csv', 'w')
for student, grade in students.items():
    # we're only writing out students who didn't complete it
    rounded_score = math.ceil(grade / 12.5) * 0.125 * 4
    if rounded_score != 4.0:
        # Rounded score: round to the nearest multiple of 12.5%
        file.write(f'{student},{rounded_score}\n')

file.close()
