# course-backend
Utilities for the course backend.

## Canvas to Runestone Student Script
This script converts Canvas students (from a CSV) to Runestone students (different CSV format) for uploading to Runestone via the instructor/admin page.

Run the Python script using `python canvasToRunestone.py`

Enter the full file name and path for the gradebook, e.g.: `Gradebook.csv`

That's it! The resultant file to upload to Runestone will be `RunestoneStudents.csv`, located in the same directory your Python script is in.

If the file does not already exist, `RunestoneStudents-master.csv` will be generated. This is for reference and should remain in the directory you're working in, but should **not** be uploaded to Runestone. Upon each run of the script, the master script will be updated with the new students from the uploaded `RunestoneStudents.csv`.
