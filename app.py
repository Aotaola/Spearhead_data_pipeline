from flask import Flask, request, render_template
#import os
from flask_sqlalchemy import SQLAlchemy
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
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('article_click.id'), nullable=False)
    time_spent = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def home():
    articles = ArticleClick.query.all()
    times = ArticleTimeSpent.query.all()

    article_data = []
    for article in articles:
        total_time_spent = sum(time.time_spent for time in times if time.article_id == article.id)
        article_data.append({
            'title': article.title,
            'count': article.count,
            'time_spent': total_time_spent
        })
    return render_template('root.html', articles = article_data)

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

    if article_id is not None and time_spent is not None:

        new_time_entry = ArticleTimeSpent(article_id=article_id, time_spent=time_spent)
        db.session.add(new_time_entry)
        db.session.commit()
        return '', 204
    else:
        return 'Invalid data', 400


if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
    app.run(debug=True)

