from flask import Flask, request, render_template
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

db = SQLAlchemy(app)

class ArticleClick(db.model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True, nullable=False)
    count = db.Column(db.Integer, default=0)

@app.route('/')
def home():
    articles = ArticleClick.query.all()
    return render_template('root.html', articles = articles)

def check():
    print ('article check', articles = ArticleClick.query.all())

@app.route('/track_click', methods=['POST'])
def track_click():
    data = request.json
    title = data.get('title')
    article = ArticleClick.query.filter_by(title=title).first()

    if article:
        article += 1
    else:
        article = ArticleClick(title=title, count = 1)
        db.session.add(article)
    db.session.commit()
    return 204




if __name__ == '__main__':
    app.run(debug=True)

