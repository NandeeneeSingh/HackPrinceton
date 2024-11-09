from flask import Flask, redirect, url_for, request, render_template
app = Flask(__name__)

@app.route('/')
def home():
   return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
   id = request.form.get('id')
   woo = request.form.get('woo')

   return redirect(url_for('display', id=id, woo=woo))

@app.route('/display')
def display():
   # Retrieve the username and password from the query parameters
   id = request.args.get('id')
   woo = request.args.get('woo')
   return render_template('display.html', id=id, woo=woo)

if __name__ == '__main__':
   app.run(debug = True)