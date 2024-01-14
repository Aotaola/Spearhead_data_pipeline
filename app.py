from flask import Flask, request, render_template
#import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import pandas as pd


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://ota:jandro96ALE@localhost/spearhead_clicks' 
#os.environ.get('DATABASE_URL')
#print("Database URI:", os.environ.get('DATABASE_URL'))

db = SQLAlchemy(app)


class ArticleClick(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    title = db.Column(db.String(255), unique=True, nullable=False)
    count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now)

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
    labels = []
    counts = []
    time_spent_data = []

    for article in articles:
        total_time_spent = sum(time.time_spent for time in times if time.article_id == article.id) / article.count

        labels.append(article.title)
        counts.append(article.count)
        time_spent_data.append(total_time_spent/article.count)

        article_data.append({
            'title': article.title,
            'timestamp': article.created_at,
            'count': article.count,
            'time_spent': total_time_spent/article.count
        })

        data = {
            'count': counts,
            'time_spent': time_spent_data,
        }

            
    return render_template('root.html', data_points = data, labels = labels)

@app.route('/canvas')
def graph():
    articles = ArticleClick.query.all()
    labels = [article.title for article in articles]
    data_points = [article.count for article in articles]

    return render_template('canvas.html', labels = labels, data_points = data_points)


@app.route('/total_time_asc')
def total_time_asc():
    times = ArticleTimeSpent.query.order_by(ArticleTimeSpent.time_spent).all()
    return times

@app.route('/total_time_desc')
def total_time_desc():
    times = ArticleTimeSpent.query.order_by(ArticleTimeSpent.time_spent).all()
    return times

@app.route('/timestamps')
def timestamps():
    times = ArticleTimeSpent.query.order_by(ArticleTimeSpent.timestamp)
    return times

@app.route('/total_clicks_asc')
def total_clicks_asc():
    clicks = ArticleClick.query.order_by(ArticleClick.count).all()
    return render_template('track_time.html', clicks = clicks)


@app.route('/total_clics_desc')
def total_clics_desc():
    clicks = ArticleClick.query.order_by(ArticleClick.count)
    return clicks

@app.route('/clicks_in_24_hours')
def clicks_in_24_hours():
    last_twenty_four_hours = datetime.utcnow() - timedelta(hours=24)
    clicks = ArticleClick.query.filter(ArticleClick.created_at >= last_twenty_four_hours).order_by(ArticleClick.created_at).all()
    return render_template('track_24_time.html', clicks = clicks)



@app.route('/clicks_in_1_week')
def clicks_in_1_week():
    last_7_days = datetime.utcnow() - timedelta(days=7)
    clicks = ArticleClick.query.filter(ArticleClick.created_at >= last_7_days).order_by(ArticleClick.created_at)
    return render_template('track_time.html', clicks = clicks)

@app.route('/clicks_in_30_days')
def clicks_in_30_days():
    thirty_days = datetime.utcnow() - timedelta(days=30)
    clicks = ArticleClick.query.filter(ArticleClick.created_at >= thirty_days).order_by(ArticleClick.created_at).all()
    return render_template('track_time.html', clicks = clicks)


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

