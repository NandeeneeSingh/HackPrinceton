import pandas as pd
from Person import Person

## Determine country of user 
select_country = ("Select the country you reside in: \n"  + 
            "1. United States \n" + 
            "2. France \n" + 
            "3. India \n" + 
            "4. China \n" + 
            "5. Ghana \n" + 
            "6. Burma \n" + 
            "7. Cambodia\n")
print(select_country)

country = input("Please enter the NAME of your country: " )
print("The country you selected is: " + country.upper())
print(" ")


id_number = 0
## Determine user identification based on country
if country == "United States":
    id_number = input("Please enter your Social Security Number: ")
    if (len(id_number) != 9):
        raise Exception("Invalid SSN")
    
elif country == "France":
    id_number = input("Please enter your National Membership Registry Number: ")
    if (len(id_number) != 15):
        raise Exception("Invalid NIR")

elif country == "India":
    id_number = input("Please enter your Aadhar Number: ")
    if (len(id_number) != 12):
        raise Exception("Invalid Aadhar Number")
    
elif country == "China":
    id_number = input("Please enter your Identity Card Number: ")
    if (len(id_number) != 18):
        raise Exception("Invalid Identity Card Number")
    
elif country == "Ghana": 
    id_number = input("Please enter your Social Security and National Trust Number: ")
    if (len(id_number) != 9):
        raise Exception("Invalid Social Security and National Trust Number")
    
elif country == "Burma":
    id_number = input("Please enter your Identity Card Number: ")
    if (len(id_number) > 64):
        raise Exception("Invalid UID number")
    
elif country == "Cambodia":
    id_number = input("Please enter your Identification Number: ")
    if (len(id_number) != 18):
        raise Exception("Invalid Identification Number")
print(" ")

## Create dictionary of doctor database with patients
patients = pd.read_csv(r'C:\Users\nande\Downloads\PatientsDatabase.csv')
patients_dict = patients.to_dict(orient = 'records')

## Dictionary of Persons with keys to their identification numbers 
persons_dict = {}

## Iterate through the dictionary
for data in patients_dict:
    visits = {data['Date 1']: data['Data 1'], 
              data['Date 2']: data['Data 2'],
              data['Date 3']: data['Data 3']} #Create a new dictionary of visits

    #Remove entries where there is no visit
    visits = {date: visit for date, visit in visits.items() if date != 'NONE'}
    
    #Assign variables to person
    p = Person(name = data['Name'], 
               dob = data['Date of Birth'], 
               coo = data['Country of Origin'], 
               visits = visits)
    
    #Populate Persons dictionary using ID number as key
    persons_dict[data['Identification Number']] = p

## Used to check if Persons dictionary is populated correctly
"""
for id_num, person in persons_dict.items():
    print(f"ID: {id_num}, {person}")


## Access a specific file for a person
"""


## Only access files according to your Identification number
if id_number.isdigit() and int(id_number) in persons_dict:
    person = persons_dict[int(id_number)]
    print(f"Visits for {person.name}:")
    for date, visit in person.visits.items():
        print(f"Date: {date} - File: {visit}")
else:
    print("Identification number not found in the database.")
print(" ")


## Access the contents of the file 
fileChosen = input("Enter the name of the file you would like to access: ")
file_opened = "./" + fileChosen + ".txt"
print(" ")

""""
try:
    with open(file_opened, 'r') as file:
        file_lines = file.readlines()

        print("File Content")
        for line in file_lines:
            print(line.strip())
except FileNotFoundError:
    print(f"File {file_opened} not found")
except Exception as e:
    print(f"An error occured: {e}")
"""

## Extract conditions, medications, and allergies
known_conditions = []
known_medications = []
known_allergies = []

#Open files and read lines
with open(file_opened, "r", encoding="utf-8") as file:
    lines = file.readlines()

#Determine if reached conditions, medications, and allergies lines
in_conditions = False
in_medications = False
in_allergies = False

#While there are lines in the file
for line in lines:
    line = line.strip()

    if line == "Known Conditions:":
        in_conditions = True
        in_medications = in_allergies = False
        continue
    elif line == "Known Medications:":
        in_medications = True
        in_conditions = in_allergies = False
        continue
    elif line == "Known Allergies:":
        in_allergies = True
        in_conditions = in_medications = False
        continue
    elif line == "":
        in_conditions = in_allergies = in_medications = False
        continue

    if in_conditions and line != "X":
        known_conditions.append(line)
    elif in_medications and line != "X":
        known_medications.append(line)
    elif in_allergies and line != "X":
        known_allergies.append(line)    

print("Known Conditions: ", known_conditions)
print("Known Medications: ", known_medications)
print("Known Allergies: ", known_allergies)