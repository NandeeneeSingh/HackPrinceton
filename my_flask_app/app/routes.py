from flask import render_template, url_for
from . import create_app

app = create_app()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')