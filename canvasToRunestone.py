import csv

gradebook = input("Enter gradebook filename: ")

with open(gradebook, "r") as file: 
  # Ignore first three lines (gradebook stuff)
  for _ in range(0, 3): 
    next(file)

  for line in csv.reader(file):
    firstName = line[0].split(", ")[1]
    lastName = line[0].split(", ")[0]
    username = line[2]
    email = line[2] + "@mines.edu"
    cwid = line[3]

with open("RunestoneStudents.csv", 'w') as file:
    # Runestone format: username,email,first_name,last_name,password,course
    csv.writer(file, delimiter=',').writerow([username, email, firstName, lastName, cwid, "thinkcspy"])

print("Gradebook successfully converted to Runestone!")
print("Output file: RunestoneStudents.csv")
