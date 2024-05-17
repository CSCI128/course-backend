# Course Backend
Utilities for the 128 course backend.

## Runestone to Canvas Grade Script
This script grades Runestone based on the Runestone Gradebook CSV export.

First, sign into [Runestone](https://runestone.academy/ns/course/index).
- Login to the [Instructor Page](https://runestone.academy/runestone/admin/admin).
- Click **Grade Book (Alpha)**, do **not** click the normal gradebook, this crashes the site because of our large class size.
- Click the **Download Gradebook** button at the bottom.
- Move the downloaded csv to the `course-backend` folder, optionally renaming it something nice like `Runestone.csv`.
- Do the same with Canvas: go to Canvas and download the entire course gradebook.
- Move the downloaded csv to the `course-backend` folder, optionally renaming it something nice like `Canvas.csv`.

This script uses a hack Greg found with Azure to get student emails from CWIDs, which is necessary because
neither Canvas nor Runestone gradebooks actually store student emails; Canvas's stores CWIDs.

Create a file called `.env` in the `course-backend` folder. Inside, write:
`TENANT_ID=""`

Ask Ethan/Greg for details on how to get the `TENANT_ID`. Note that when the script runs for the first time,
it will take a long time because it needs to query Mines Azure services for every single student. Following the first run,
a file called `cwids.db` will be generated; this is a cache of student CWIDs -> emails. Leave this file alone; it will help the script run quicker. These files are gitignored, but ensure that you *never* commit a `cwids.db` or gradebook csv for legal reasons.

Next, create and activate a venv, then run the script:
`python3 -m venv venv`
`pip install -r requirements.txt`
`source venv/bin/activate`
`python gradeRunestone.py`

Enter the full file name and path for the Canvas gradebook, e.g.: `Canvas.csv`

Enter the full file name and path for the Runestone gradebook, e.g.: `Runestone.csv`

Enter the *exact* name of the assignment you're grading, e.g.: `Week 1 Readings`

Enter the maximum points in Runestone; you can see this under the 'Assignments' tab in the Runestone admin,
or it may just be evident if you look at what the majority of students did in the gradebook. You can also
curve slightly with this if something goes wrong with a chapter.

The resultant file to upload to Canvas will be `Grades-CSCI128_-_Spring_2024_-_All Sections.csv`, located in the same directory your Python script is in.

For verification/testing purposes, students are outputted in a simpler format in `{assignment name}.csv`.

### Other Notes

We curve grades just a little! We round to the nearest multiple of 12.5%; this normally equates to a boost of ~0.25-1 points per assignments.

There is a file called `assignments.json` which has the valid sections, but this is actually outdated. `assignments.json` is just used for the list of assignment names, which should match exactly in this program, Runestone, Canvas, and all gradebooks.

## Canvas to Runestone Student Script (deprecated)
*This script should no longer be used, in favor of actual Canvas linking to Runestone via ITS. This is a backup for if things break*

This script converts Canvas students (from a CSV) to Runestone students (different CSV format) for uploading to Runestone via the instructor/admin page.

Run the Python script using `python canvasToRunestone.py`

Enter the full file name and path for the gradebook, e.g.: `Gradebook.csv`

That's it! The resultant file to upload to Runestone will be `RunestoneStudents.csv`, located in the same directory your Python script is in.

If the file does not already exist, `RunestoneStudents-master.csv` will be generated. This is for reference and should remain in the directory you're working in, but should **not** be uploaded to Runestone. Upon each run of the script, the master script will be updated with the new students from the uploaded `RunestoneStudents.csv`.
