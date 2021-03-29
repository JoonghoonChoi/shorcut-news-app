from flask import Blueprint, render_template, request, redirect, url_for
from news_app.services.tweepy_api import get_timeline
from news_app.utils.main_funcs import get_sentiment
from news_app.models.user_model import User
from news_app.models.timeline_model import Timeline
from news_app.models.sentiment_model import Sentiment
from news_app.models.feedback_model import Feedback
from news_app import db
import tweepy
import re
from datetime import datetime

bp = Blueprint('news', __name__)

@bp.route('/news', methods=['GET', 'POST'])
def add_user():
    '''
    1. 웹 사용자의 입력을 받아 뉴스 채널을 추가
    2. 트윗 추가 시 어떻게 뉴스채널인지 확인할건가???
    3. 잘못된 트윗이름이나 에러가 발생하면 이전 페이지로 돌아가기
    4. 현재 등록되어 있지 않은 채널이면 채널과 트윗 기사 모두 추가
    5. 현재 등록되어 있다면 전체 삭제하고 최신으로 업데이트 
    '''
    username = request.form.get('newsname') # news.html에서 받는 input name과 같아야 함
    username = username.lower()

    if request.method == "POST":
        if not username:
            return "Needs username", 400

        # 지정한 뉴스채널 관련 문구가 없으면 오류메세지 보냄
        mylst = ['news', 'breaking', 'brk', 'cnn', 'bbc']
        if not any(re.findall('|'.join(mylst), username)):
            return "Please input twit username including 'news/brk/breaking/cnn/bbc...'. \
                If you need a new keyword of news channel. Plase let me know in feedback tab!", 400
        
        # 위에서 키워드를 거르기 때문에 이부분은 없어도 될 것 같은데 ?
        try:
            get_timeline(username)
        except tweepy.error.TweepError as e:
            return redirect(url_for('main.news_index', msg_code=0), code=400)


        used_name = User.query.filter_by(username=username).first()

        if not used_name:
            new_timeline = get_timeline(username) # 리스트가 담긴 딕셔너리
            
            new_user = User(username=username, location=new_timeline['location'][0])
            db.session.add(new_user)

            user_id = db.session.query(User.id).filter_by(username=username)
            for headline, link in zip(new_timeline['headline'], new_timeline['link']):
                new_headline = Timeline(headline=headline, link=link, user_id=user_id)
            
                db.session.add(new_headline)
            
            db.session.commit()
        
        if used_name:
            user_id = db.session.query(User.id).filter_by(username=username)
            timeline = Timeline.query.filter_by(user_id=user_id).all()
            db.session.delete(used_name)
            for t in timeline:
                db.session.delete(t)
            db.session.commit()

            update_timeline = get_timeline(username)

            new_user = User(username=username, location=update_timeline['location'][0])
            db.session.add(new_user) 

            for headline, link in zip(update_timeline['headline'], update_timeline['link']):
                new_headline = Timeline(headline=headline, link=link, user_id=user_id)
                db.session.add(new_headline)

            db.session.commit()     


    return redirect(url_for('main.news_index'), code=200)


@bp.route('/news/<int:timeline_id>', methods= ['GET', 'POST'])
def delete_timeline(timeline_id=None):
    '''
    1. 데이터베이스에서 Timeline.id 와 일치하는 데이터를 불러옴
    2. 해당 데이터를 삭제
    3. 연관되어 있는 sentiment테이블의 해당 데이터도 삭제
    '''
    if not timeline_id:
        return '', 400
    
    timeline = Timeline.query.filter_by(id=timeline_id).first()
    headline = Timeline.query.with_entities(Timeline.headline).filter_by(id=timeline_id).first()
    headline_text = ', '.join(map("".join, headline))
    sentiment = Sentiment.query.filter_by(timeline_headline=headline_text).first()
    
    if not timeline:
        return '', 404
    
    if timeline:
        db.session.delete(timeline)
        db.session.commit()

    if sentiment:
        db.session.delete(sentiment)
        db.session.commit()
    

    return redirect(url_for('main.news_index'), code=200)


@bp.route('/sentiment', methods=['GET', 'POST'])
def update_sentiment():
    '''
    1. 데이터베이스에 저장된 기사 헤드라인을 불러옴
    2. 각 헤드라인의 텍스트를 분석하여 긍정적인 키워드가 많은지 아닌지 pos/neg 값으로 분류 (분류기 모델)
    3. 현재 데이터베이스 내 sentiment 데이터를 업데이트
    '''
    if request.method == "POST":

        headline = db.session.query(Timeline.headline).all()

        headline_lst = []
        for i in range(len(headline)):
            headline_lst.append(', '.join(map("".join, headline[i])))

        sentiment_lst = get_sentiment(headline_lst)
        alreadyin = Sentiment.query.with_entities(Sentiment.timeline_headline).all()

        if alreadyin:
            db.session.query(Sentiment).delete()
            db.session.commit()

            for s, t in zip(sentiment_lst, headline_lst):
                new_sentiment = Sentiment(type=s, timeline_headline=t)
                db.session.add(new_sentiment)
            db.session.commit()
        
        if not alreadyin:
            for s, t in zip(sentiment_lst, headline_lst):
                new_sentiment = Sentiment(type=s, timeline_headline=t)
                db.session.add(new_sentiment)
            db.session.commit()
                    
        return redirect(url_for('main.sentiment_index'), code=200)


@bp.route('/feedback', methods=['GET', 'POST'])
def update_feedback():
    text = request.form.get('feedback_text')
    now = datetime.now()

    if request.method == "POST":
        if not text:
            return 'Please let me know about this service :)', 400
        
        if text: 
            new_feedback = Feedback(text=text, date=now)
            db.session.add(new_feedback)
            db.session.commit()

    return redirect(url_for('main.feedback_index'), code=200)
