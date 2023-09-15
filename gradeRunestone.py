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
    gradebookDF = gradebookDF[gradebookDF['SIS User ID'] != 'transcriber1']

    gradebook_type = input("Do you want to grade a Runestone gradebook or chapter activity export? Enter c or g: ")
    if gradebook_type == 'c':
        print('Grading in chapter activity mode..')

        runestone = input("Enter Runestone cahpter activity filename: ")
        runestoneDF = pd.read_csv(runestone)
        runestoneDF = runestoneDF.drop(runestoneDF.columns[0], axis=1)

        assignment_sections = []
        assignment_name = None
        print("Loaded assignments:")
        with open('assignments.json', 'r') as assignments:
            assignment_data = json.load(assignments)
            for key in assignment_data.keys():
                print(key)

            assignment = input("Enter assignment to grade: ")
            try:
                for key in assignment_data.keys():
                    if key in assignment:
                        assignment_sections = assignment_data[assignment]
                        assignment_name = assignment
            except KeyError:
                print("Could not find the specified assignment!")
                exit()

        # storing points for each activity as { row_index: [chapter_id, points] }
        activity_points: dict = {}
        for (columnName, columnData) in runestoneDF['chapter_label'].items():
            chapter_id: str = str(columnData).split(" ")[0]
            points: float = float(str(columnData).split(" ")[-1].replace(')', '').replace('(', ''))
            activity_points.update({ chapter_id: [int(columnName), points] })

        # Find maximum points
        points_maximum = 0
        for k, v in activity_points.items():
            if str(k) in assignment_sections:
                points_maximum += v[1]

        # formatted { studentName: score }
        students: dict = {}

        # get students from df
        for (columnName, columnData) in runestoneDF.items():
            if columnName != 'chapter_label':
                points = 0
                for k, v in activity_points.items():
                    for i in range(0, len(columnData.values)):
                        if i == v[0] and str(k) in assignment_sections and columnData.values[i] != ' ':
                            points += float(columnData.values[i])

                score = (points / points_maximum) * 100
                students.update({ str(columnName).replace('<br>', ' '): score })

        # update assignment name once found
        found_assignment = False
        for key in gradebookDF.keys():
            if assignment_name in key:
                assignment_name = key
                found_assignment = True

        if not found_assignment:
            print(f"Could not find assignment '{assignment_name}' in the Canvas gradebook! Make sure you published the assignment and downloaded the latest gradebook.")
            exit()

        file = open(f'{assignment_name}.csv', 'w')
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
                gradebookDF.loc[condition, assignment_name] = rounded_score
            except ValueError:
                log.write(f"{student} has an invalid Runestone username, skipping..\n")
                continue

        gradebookDF = gradebookDF.fillna(0)
        gradebookDF.to_csv('Grades-CSCI128_-_Fall_2023_-_All Sections.csv', index=False)
        
        file.close()
        log.close()
    elif gradebook_type == 'g':
        print('Grading in Runestone gradebook mode..')

        runestone = input("Enter Runestone gradebook filename: ")
        runestoneDF = pd.read_csv(runestone)

        assignment_sections = []
        assignment_name = None
        print("Loaded assignments:")
        with open('assignments.json', 'r') as assignments:
            assignment_data = json.load(assignments)
            for key in assignment_data.keys():
                print(key)

            assignment = input("Enter assignment to grade: ")
            try:
                for key in assignment_data.keys():
                    if key in assignment:
                        assignment_sections = assignment_data[assignment]
                        assignment_name = assignment
            except KeyError:
                print("Could not find the specified assignment!")
                exit()

        # TODO add max assignment pts to "loaded assignments"? or enter (to calculate percentage)
        max_points = int(input("Enter max score for this assignment: "))

        log = open('error.log', 'w')
        
        # find student by name and their best score (since there's no way to check for good emails)
        # also solves the issue of people doing it on the wrong account
        # formatted { first_last: score%}
        students: dict = {}
        for _, row in runestoneDF.iterrows():
            points = row[assignment_name]
            if math.isnan(row[assignment_name]):
                points = 0

            student_name = row['last_name'] + ', ' + row['first_name']
            if student_name in students:
                if points < students[student_name]:
                    log.write(f"{student_name} had another account with a lower score, not updating..\n")
                    continue

            students.update({ student_name : (points / max_points) * 100 })

        # update assignment name for the canvas CSV export
        found_assignment = False
        for key in gradebookDF.keys():
            if assignment_name in key:
                assignment_name = key
                found_assignment = True

        if not found_assignment:
            print(f"Could not find assignment '{assignment_name}' in the Canvas gradebook! Make sure you published the assignment and downloaded the latest gradebook.")
            exit()

        # grade students
        file = open(f'{assignment_name}.csv', 'w')
        for student, grade in students.items():
            rounded_score = math.ceil(grade / 12.5) * 0.125 * 4

            # Rounded score: round to the nearest multiple of 12.5%
            file.write(f'{student},{rounded_score}\n')

            condition = gradebookDF['Student'] == student
            gradebookDF.loc[condition, assignment_name] = rounded_score

        gradebookDF = gradebookDF.fillna(0)
        gradebookDF.to_csv('Grades-CSCI128_-_Fall_2023_-_All Sections.csv', index=False)
        
        file.close()
        log.close()
    else:
        exit()
    