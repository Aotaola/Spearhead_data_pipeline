from flask import Flask, request, render_template
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

db = SQLAlchemy(app)

@app.route('/')
def hello_world():
    return render_template('root.html', click_counts = click_counts)


click_counts = {}

@app.route('/track_click', methods=['POST'])
def track_click():
    data = request.json
    title = data.get('title')

    if title in click_counts:
        click_counts[title] += 1
    else:
        click_counts[title] = 1

    print(f'{title} clicked {click_counts} times')
    return click_counts, 204



if __name__ == '__main__':
    app.run(debug=True)

