from flask import Flask
import requests

app = Flask(__name__)
click_count = 0

@app.route('/track_click', methods=['POST'])
def track_click():
    global click_count
    click_count += 1
    data = requests.json
    title = data.get('title')
    print(f'{title} clicked {click_count} times')
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
