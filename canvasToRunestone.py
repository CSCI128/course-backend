import csv

gradebook = input("Enter gradebook filename: ")

with open(gradebook, "r") as file: 
  # Ignore first three lines (gradebook stuff)
  for _ in range(0, 3): 
    next(file)

  for lines in csv.reader(file): 
        firstName = lines[0].split(", ")[1]
        lastName = lines[0].split(", ")[0]
        username = lines[2]
        email = lines[2] + "@mines.edu"
        cwid = lines[3]

with open("RunestoneStudents.csv", 'w') as file:
    # Runestone format: username,email,first_name,last_name,password,course
    csv.writer(file, delimiter=',').writerow([username, email, firstName, lastName, cwid, "thinkcspy"])

print("Gradebook successfully converted to Runestone!")
print("Output file: RunestoneStudents.csv")
