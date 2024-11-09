import pandas as pd
from Person import Person

class patientData:
    data = {}

    def __init__(self, file):
        patients = pd.read_csv(file)
        for p in patients.to_dict(orient = 'records'):
            #Create a new dictionary of visits
            visits = {p['Date 1']: p['Data 1'], 
                    p['Date 2']: p['Data 2'],
                    p['Date 3']: p['Data 3']} 

            #Remove entries where there is no visit
            visits = {date: visit for date, visit in visits.items() if date != 'NONE'}

            #Assign variables to person
            name = p['Name']
            dob = p['Date of Birth']
            coo = p['Country of Origin']

            per = Person(name, dob, coo, visits)

            self.data[p['Identification Number']] = per

    def display(self):
        for d in self.data:
            print('===')
            print(d)
            print(self.data[d])
        
# class main:
#     pats = patientData("./static/PatientsDatabase.csv").data
    
#     # pat.display()
#     print(pats[123456789].name)