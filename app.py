from flask import Flask, request, render_template
#import os
from flask_sqlalchemy import SQLAlchemy, DateTime
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ota:jandro96ALE@localhost/spearhead_clicks' 
# os.environ.get('DATABASE_URL')
#print("Database URI:", os.environ.get('DATABASE_URL'))

db = SQLAlchemy(app)


class ArticleClick(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    title = db.Column(db.String(255), unique=True, nullable=False)
    count = db.Column(db.Integer, default=0)

class ArticleTimeSpent(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey('article_click.id'))
    time_spent = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.estnow)

@app.route('/')
def home():
    articles = ArticleClick.query.all()
    return render_template('root.html', articles = articles)

# def check():
#     print ('article check', articles = ArticleClick.query.all())

@app.route('/track_click', methods=['POST'])
def track_click():
    data = request.json
    id = data.get('id')
    title = data.get('title')
    article = ArticleClick.query.filter_by(title=title).first()

    if article:
        article.count += 1
    else:
        article = ArticleClick(id = id, title = title, count = 1)
        db.session.add(article)
    db.session.commit()
    return '',204

@app.route('/track_time', methods=['POST'])
def track_time():
    data = request.json
    article_id = data.get('article_id')
    time_spent = data.get('time_spent')

    new_time_entry = ArticleTimeSpent.query.filter_by(article_id=article_id, time_spent=time_spent)
    db.session.add(new_time_entry)
    db.session.commit()


if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
    app.run(debug=True)

