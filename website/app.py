from flask import Flask, redirect, url_for, request, render_template, session
import pandas as pd

from patient_data import PatientDatabase, VisitDataReader
from llm_script import MedicalAssistant

app = Flask(__name__)
app.secret_key = "key"
patient_data = PatientDatabase(pd.read_csv("./static/PatientsDatabase.csv"))

medical_assistant = MedicalAssistant()


@app.route("/")
def home():
    return render_template("login.html", error=None)


@app.route("/login", methods=["POST"])
def login():
    identification_number = request.form.get("iden")
    country_of_origin = request.form.get("coo")

    if country_of_origin == "United States" and len(identification_number) != 9:
        return redirect(url_for("loginWError", error="Invalid SSN"))
    elif country_of_origin == "France" and len(identification_number) != 15:
        return redirect(url_for("loginWError", error="Invalid NIR"))
    elif country_of_origin == "India" and len(identification_number) != 12:
        return redirect(url_for("loginWError", error="Invalid Aadhar Number"))
    elif country_of_origin == "China" and len(identification_number) != 18:
        return redirect(url_for("loginWError", error="Invalid Identity Card Number"))
    elif country_of_origin == "Ghana" and len(identification_number) != 9:
        return redirect(
            url_for(
                "loginWError", error="Invalid Social Security and National Trust Number"
            )
        )
    elif country_of_origin == "Burma" and len(identification_number) > 64:
        return redirect(url_for("loginWError", error="Invalid UID number"))
    elif country_of_origin == "Cambodia" and len(identification_number) != 18:
        return redirect(url_for("loginWError", error="Invalid Identification Number"))
    else:
        return redirect(
            url_for(
                "display",
                identification_number=identification_number,
                country_of_origin=country_of_origin,
            )
        )


@app.route("/loginWError")
def loginWError():
    error = request.args.get("error")
    return render_template("loginWError.html", error=error)


@app.route("/display")
def display():
    # Retrieve the username and password from the query parameters
    identification_number = request.args.get("identification_number")
    country_of_origin = request.args.get("country_of_origin")
    # cast identification number to integer TODO: check for type errors
    identification_number = int(identification_number)

    name = patient_data.get_name(identification_number)
    visits = patient_data.get_visits(identification_number)
    return render_template("visits.html", name=name, visits=visits, identification_number=identification_number)

@app.route("/day/<date>/<identification_number>")
def day(date : str, identification_number : str):
    visit_data = patient_data.get_visits(int(identification_number))[date]
    simplified_diagnosis = medical_assistant.query_diagnosis(str(visit_data.conditions))

    return render_template("day.html", date = date, simplified_diagnosis = simplified_diagnosis)

if __name__ == "__main__":
    app.run(debug=True)
