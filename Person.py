class Person: 
    def __init__(self, name, dob, coo, visits):
        self.name = name; 
        self.dob = dob; 
        self.coo = coo
        self.visits = visits

    def __str__(self):
        return f"Name: {self.name}, Date of Birth: {self.dob}, Country of Origin: {self.coo}, Visits: {self.visits}"