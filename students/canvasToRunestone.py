import os
import csv

gradebook = input("Enter gradebook filename: ")

# find already added students
students = []
if os.path.exists('RunestoneStudents-master.csv'):
  with open("RunestoneStudents-master.csv", 'r') as file:
    for line in csv.reader(file):
      students.append(line[0])

  # Loop through a few of the students from last time
  print("Previously added students (first 10):")
  for i in range(0, 10):
    print(students[i])

with open(gradebook, "r") as gradebook: 
  # Ignore first two lines (irrelevant gradebook stuff)
  for _ in range(0, 3): 
    next(gradebook)

  # open (or create) master students file
  master = open('RunestoneStudents-master.csv', 'a')
  
  with open("RunestoneStudents.csv", 'w') as file:
    for line in csv.reader(gradebook):
      firstName = line[0].split(", ")[1]
      lastName = line[0].split(", ")[0]
      cwid = line[2]
      username = "mines_" + cwid
      email = line[3] + "@mines.edu"

      if not (firstName == 'Test' and lastName == 'Student'):      
        # Runestone format: username,email,first_name,last_name,password,course
        csv.writer(file, delimiter=',').writerow([username, email, firstName, lastName, cwid, "mines_csstem"])

        # update master spreadsheet with new additions
        if username not in students:
          print(f'New entry {username} added to master..')
          csv.writer(master, delimiter=',').writerow([username, email, firstName, lastName, cwid, "mines_csstem"])
        else:
          print(f'Found duplicate {username}, not adding..')

print("Gradebook successfully converted to Runestone!")
print("Output file: RunestoneStudents.csv")
