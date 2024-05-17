# course-backend
Utilities for the course backend.

## Runestone to Canvas Grade Script
This script grades Runestone based on the Runestone chapter activity CSV export.

Run the Python script using `python gradeRunestone.py`

Enter the full file name and path for the Canvas gradebook, e.g.: `Gradebook.csv`

Delete all the assignment columns that aren't the one being graded.

Enter the full file name and path for the Runestone chapter activity gradebook, e.g.: `Runestone.csv`

The resultant file to upload to Canvas will be `Grades-CSCI128_-_Fall_2023_-_All Sections.csv`, located in the same directory your Python script is in.

For verification/testing purposes, students are outputted in a simpler format in `output.csv`.

## Canvas to Runestone Student Script (deprecated)
*This script should no longer be used, in favor of actual Canvas linking to Runestone via ITS. This is a backup for if things break*

This script converts Canvas students (from a CSV) to Runestone students (different CSV format) for uploading to Runestone via the instructor/admin page.

Run the Python script using `python canvasToRunestone.py`

Enter the full file name and path for the gradebook, e.g.: `Gradebook.csv`

That's it! The resultant file to upload to Runestone will be `RunestoneStudents.csv`, located in the same directory your Python script is in.

If the file does not already exist, `RunestoneStudents-master.csv` will be generated. This is for reference and should remain in the directory you're working in, but should **not** be uploaded to Runestone. Upon each run of the script, the master script will be updated with the new students from the uploaded `RunestoneStudents.csv`.
