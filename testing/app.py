from flask import Flask, redirect, url_for, request, render_template
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    iden = request.form.get('iden')
    coo = request.form.get('coo')

    return redirect(url_for('display', iden=iden, coo=coo))

@app.route('/display')
def display():
    # Retrieve the username and password from the query parameters
    iden = request.args.get('iden')
    coo = request.args.get('coo')
    return render_template('display.html', iden=iden, coo=coo)

if __name__ == '__main__':
    app.run(debug = True)