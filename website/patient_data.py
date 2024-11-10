import pandas as pd
from pandas import DataFrame


from typing import Dict
from enum import Enum
import os
from io import TextIOWrapper


class VisitDataReader:
    def __init__(self) -> None:
        self.conditions = None
        self.medications = None
        self.allergies = None

    def read_file(self, file_object : TextIOWrapper) ->  None:
        if not any(map(lambda data : data is None, [self.conditions, self.medications, self.allergies])):
            return

        class ParserState(Enum):
            OTHER = 0
            CONDITIONS = 1
            MEDICATIONS = 2
            ALLERGIES = 3

        self.conditions = []
        self.medications = []
        self.allergies = []
        parser_state = ParserState.OTHER
        for line in file_object.readlines():
            processed_line = line.strip()
            if "Known Conditions" in processed_line:
                parser_state = ParserState.CONDITIONS
            elif "Known Medications" in processed_line:
                parser_state = ParserState.MEDICATIONS
            elif "Known Allergies" in processed_line:
                parser_state = ParserState.ALLERGIES
            elif parser_state in [ParserState.CONDITIONS, ParserState.MEDICATIONS, ParserState.ALLERGIES] and line == "":
                parser_state = ParserState.OTHER

            if line != "X" and parser_state is not ParserState.OTHER:
                if parser_state is ParserState.CONDITIONS:
                    self.conditions.append(processed_line)
                elif parser_state is ParserState.MEDICATIONS:
                    self.medications.append(processed_line)
                elif parser_state is ParserState.ALLERGIES:
                    self.allergies.append(processed_line)


class PersonData:

    VISIT_DATA_PATH = "./static/visit_data/"
    VISIT_FILE_EXTENSION = "txt"

    def __init__(
        self,
        name: str,
        date_of_birth: str,
        country_of_origin: str,
        visits: Dict[str, str],
    ) -> None:
        self.name = name
        self.date_of_birth = date_of_birth
        self.country_of_origin = country_of_origin
        self.visits = dict()
        for visit_date, visit_file_name in visits.items():
            visit_file_path = os.path.join(PersonData.VISIT_DATA_PATH, f"{visit_file_name}.{PersonData.VISIT_FILE_EXTENSION}")
            try:
                with open(visit_file_path, 'r', encoding='utf-8') as visit_file:
                    visit_data_reader = VisitDataReader()
                    visit_data_reader.read_file()
            except FileNotFoundError:
                print(f"Patient visit data '{visit_file_path}' not found, skipping visit data.")
                continue

            self.visits[visit_date] = visit_data_reader


    def __str__(self):
        return f"Name: {self.name}, Date of Birth: {self.date_of_birth}, Country of Origin: {self.country_of_origin}, Visits: {self.visits}"


class PatientDatabase:
    def __init__(self, file_data: DataFrame):
        self.__data = dict()

        for patient_index, patient_data in file_data.iterrows():
            patient_visits = dict()
            for date_index in range(3):
                if (patient_data[f"Date {date_index}"] is None) or (
                    patient_data[f"Data {date_index}"] is None
                ):
                    continue

                patient_visits[patient_data[f"Date {date_index}"]] = patient_data[
                    f"Data {date_index}"
                ]

            self.__data[patient_data["Identification Number"]] = PersonData(
                patient_data["Name"],
                patient_data["Date of Birth"],
                patient_data["Country of Origin"],
                patient_visits,
            )

    def get_name(self, identification_number : int) -> str:
        return self.__data[identification_number].name
    
    def get_visits(self, identification_number : int) -> Dict[str, str]:
        return self.__data[identification_number].visits
    