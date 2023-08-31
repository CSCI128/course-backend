"""
Runestone Grading Script
Grades are based on the "Chapter Activity" CSV export, not the gradebook.
See Canvas gradebook format: https://community.canvaslms.com/t5/Instructor-Guide/How-do-I-import-grades-in-the-Gradebook/ta-p/807
"""
import json
import math
import pandas as pd

if __name__ == "__main__":
    # Load Canvas & Runestone gradebooks into DataFrames
    gradebook = input("Enter Canvas gradebook filename: ")
    gradebookDF = pd.read_csv(gradebook, dtype={'ID': str})
    gradebookDF = gradebookDF.drop([0]) # drop possible pts row
    
    # TODO unsure if this is necessary
    # gradebookDF['Week 2 Readings (345279)'] = gradebookDF['Week 2 Readings (345279)'].astype(float)
    
    gradebookDF = gradebookDF[gradebookDF['SIS User ID'] != 'transcriber1']

    runestone = input("Enter Runestone gradebook filename: ")
    runestoneDF = pd.read_csv(runestone)
    runestoneDF = runestoneDF.drop(runestoneDF.columns[0], axis=1)

    # TODO read in name of assignment and compare with gradebook AND assignments.json
    # also check if assignment column exists in gradebook
    # assignment = input("Enter the name of the assignment you are grading: ")
    # **dropdown: select from prebuilt assignments

    # storing points for each activity as { row_index: [chapter_id, points] }
    activity_points: dict = {}
    for (columnName, columnData) in runestoneDF['chapter_label'].items():
        chapter_id: str = str(columnData).split(" ")[0]
        points: float = float(str(columnData).split(" ")[-1].replace(')', '').replace('(', ''))
        activity_points.update({ chapter_id: [int(columnName), points] })

    # TODO make this taken in via the terminal or something
    # week 2, 3.1-3.10, 4.1-4.13
    ASSIGNMENT = [
        '3.1', '3.2', '3.3', '3.4', '3.5', '3.6', '3.7', '3.8', '3.9', '3.10',
        '4.1', '4.2', '4.3', '4.4', '4.5', '4.6', '4.7', '4.8', '4.9', '4.10', '4.11', '4.12', '4.13'
    ]

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

    file = open('output.csv', 'w') # TODO I'll remove this later, it's good for testing though
    log = open('error.log', 'w')
    for student, grade in students.items():
        rounded_score = math.ceil(grade / 12.5) * 0.125 * 4

        # Rounded score: round to the nearest multiple of 12.5%
        file.write(f'{student},{rounded_score}\n')

        if '@mines.edu' in str(student) or '_' not in str(student):
            log.write(f"{student} has an invalid Runestone username, skipping..\n")
            continue

        try:
            student_id = int(str(student).split("_")[-1].replace(")", ""))
            condition = pd.to_numeric(gradebookDF['SIS User ID']) == int(student_id)
            gradebookDF.loc[condition, 'Week 2 Readings (345279)'] = rounded_score
        except ValueError:
            log.write(f"{student} has an invalid Runestone username, skipping..\n")
            continue

    # filter out NaNs
    gradebookDF = gradebookDF.fillna(0)

    file.close()
    log.close()
    gradebookDF.to_csv('Grades-CSCI128_-_Fall_2023_-_All Sections.csv', index=False)
