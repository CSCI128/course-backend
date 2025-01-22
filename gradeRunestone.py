# Runestone Grading Script
import os
import asyncio
import json
import math
import shelve
import pandas as pd
from AzureAD import AzureAD
from dotenv import load_dotenv
load_dotenv() 

azure = AzureAD(os.getenv("TENANT_ID"))

async def get_cwid(email: str) -> str:
    return await azure.getCWIDFromEmail(email)

async def main() -> None:
    # Load Canvas & Runestone gradebooks into DataFrames
    gradebook = input("Enter Canvas gradebook filename: ")
    gradebookDF = pd.read_csv(gradebook, dtype={'ID': str})
    gradebookDF = gradebookDF.drop([0]) # drop possible pts row
    gradebookDF = gradebookDF[gradebookDF['SIS User ID'] != 'transcriber1']

    runestone = input("Enter Runestone gradebook filename: ")
    runestoneDF = pd.read_csv(runestone)
    runestoneDF = runestoneDF.drop([0]) # drop empty row

    assignment_name = None
    with open('assignments.json', 'r') as assignments:
        assignment_data: dict = json.load(assignments)
        print("Loaded assignments:", ", ".join(assignment_data.keys()))

        assignment = input("Enter assignment to grade: ")
        try:
            for key in assignment_data.keys():
                if key in assignment:
                    assignment_name = assignment
        except KeyError:
            print("Could not find the specified assignment!")
            exit()

    max_points = int(input("Enter max score for this assignment: "))

    curved_score_max = int(input("Enter whether this is a 4 or 5 assignment: "))
    if curved_score_max != 4 and curved_score_max != 5:
        print("Invalid score curve")
        exit()

    # Find students from Runestone, formatted { first_last: score%}
    students: dict = {}
    for _, row in runestoneDF.iterrows():
        points = 0 if math.isnan(row[assignment_name]) else row[assignment_name]
        students.update({ row['email'] : (points / max_points) * 100 })

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
    with shelve.open('cwids') as cache:
        for student, grade in students.items():
            if not str(student).endswith("@mines.edu"):
                continue

            # Rounded score: round to the nearest multiple of 12.5%
            rounded_score = math.ceil(grade / 12.5) * 0.125 * curved_score_max

            file.write(f'{student},{rounded_score}\n')

            if student in cache.keys():
                cwid = cache[student]
            else:
                try:
                    cwid = await azure.getCWIDFromEmail(student)
                    cache[student] = cwid
                except:
                    print(f"Couldn't find CWID for student {student}..")
                    pass

            condition = gradebookDF['SIS User ID'] == float(cwid)
            gradebookDF.loc[condition, assignment_name] = rounded_score

    gradebookDF = gradebookDF.fillna(0)
    gradebookDF.to_csv('Grades.csv', index=False)

    file.close()

if __name__ == "__main__":
    asyncio.run(main())
