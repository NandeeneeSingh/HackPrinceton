from flask import Flask, redirect, url_for, request, render_template
from patientData import patientData

app = Flask(__name__)
patdata = patientData("./static/PatientsDatabase.csv").data

@app.route('/')
def home():
    return render_template('login.html', error = None)

@app.route('/login', methods=['POST'])
def login():
    iden = request.form.get('iden')
    coo = request.form.get('coo')

    if (coo == "United States" or coo == "USA") and (len(iden) != 9):
        return redirect(url_for('loginWError', error = "Invalid SSN"))
    
    elif (coo == "France" or coo == "france") and (len(iden) != 15):
        return redirect(url_for('loginWError', error = "Invalid NIR"))

    elif (coo == "India" or coo == "india") and (len(iden) != 12):
        return redirect(url_for('loginWError', error = "Invalid Aadhar Number"))

    elif (coo == "China" or coo == "china") and (len(iden) != 18):
        return redirect(url_for('loginWError', error = "Invalid Identity Card Number"))
        
    elif (coo == "Ghana" or coo == "ghana") and (len(iden) != 9):
        return redirect(url_for('loginWError', error = "Invalid Social Security and National Trust Number"))
        
    elif (coo == "Burma" or coo == "burma") and (len(iden) > 64):
        return redirect(url_for('loginWError', error = "Invalid UID number"))
        
    elif (coo == "Cambodia" or coo == "cambodia") and (len(iden) != 18):
        return redirect(url_for('loginWError', error = "Invalid Identification Number"))
    
    else:
        return redirect(url_for('display', iden=iden, coo=coo))

@app.route('/loginWError')
def loginWError():
    error = request.args.get('error')
    return render_template('loginWError.html', error = error)


@app.route('/display')
def display():
    # Retrieve the username and password from the query parameters
    iden = request.args.get('iden')
    coo = request.args.get('coo')
    # print(patdata[int(iden)])
    name = patdata[int(iden)].name
    return render_template('display.html', iden=iden, coo=coo, name = name)

if __name__ == '__main__':
    app.run(debug = True)