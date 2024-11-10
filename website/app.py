from flask import Flask, redirect, url_for, request, render_template, session
from patientData import patientData

app = Flask(__name__)
app.secret_key = "key"
patient_data = patientData("./static/PatientsDatabase.csv").data


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

    name = patient_data[int(identification_number)].name
    visits = patient_data[int(identification_number)].visits
    return render_template("visits.html", name=name, visits=visits)

@app.route("/day/<date>")
def day(date):
    return render_template("day.html", date = date)

if __name__ == "__main__":
    app.run(debug=True)
