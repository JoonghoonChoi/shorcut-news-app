from flask import Blueprint, render_template, request
from news_app.models.user_model import User
from news_app.models.timeline_model import Timeline
from news_app.models.sentiment_model import Sentiment
from news_app.models.feedback_model import Feedback
from news_app import db
from news_app.utils.main_funcs import get_sentiment

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET'])
def index():
    '''
    1. 데이터베이스에 쿼리를 날려서 user(뉴스트윗채널)을 불러옴
    2. 각 계정의 username과 location 추출
    3. 웹의 메인 페이지에 현재 데이터베이스에 보유하고 있는 채널과 지역정보를 보여줌
    '''
    news = User.query.distinct(User.username).all()
    header = ['No.', 'Channel', 'Location']
    
    # 쿼리날려서 받은 데이터의 id는 항상 1부터 시작하지 않으므로 1부터 데이터 수만큼 뽑아서 웹에 넣어줌    
    id = []
    for num in range(1, (len(news) + 1)):
        id.append(num)

    data = []
    for i in range(0, len(news)):
        data.append([id[i], news[i].username, news[i].location])

    return render_template('index.html', header=header, data=data)


@bp.route('/news', methods=['GET'])
def news_index():
    '''
    1. 데이터베이스에서 타임라인을 모두 불러옴
    2. 불러온 데이터에서 타임라인의 각 기사 헤드라인과, 링크, 계정이름 추출
    3. 리스트에 담아 template html 파일로 넘겨줌
    '''
    msg_code = request.args.get('msg_code', None)
    alert_msg = main_funcs.msg_processor(msg_code) if msg_code is not None else None

    timelines = Timeline.query.all()
    timeline_user = db.session.query(User.username).filter(User.id==Timeline.user_id).all()
    
    # 쿼리날려서 받은 데이터의 id는 항상 1부터 시작하지 않으므로 1부터 데이터 수만큼 뽑아서 웹에 넣어줌
    # num = []
    # for n in range(1, (len(timelines) + 1)):
    #     num.append(n)

    timeline_lst = []
    for i in range(len(timelines)):
        username = ', '.join(map("".join, timeline_user[i])) # 튜플 (string, ) 형식의 텍스트 변환해주기
        read = {'id' : timelines[i].id, 'headline' : timelines[i].headline, 
            'link' : timelines[i].link, 'username' : username}
        timeline_lst.append(read)
    
    return render_template('news.html', alert_msg=alert_msg, timeline_lst=timeline_lst)


@bp.route('/sentiment', methods=['GET'])
def sentiment_index():
    '''
    1. 현재 데이터베이스 내 sentiment 데이터를 쿼리로 불러옴
    2. 현재 데이터가 없다면 업데이트 버튼만 있는 페이지를 보여줌
    3. 데이터가 있으면 데이터의 pos/neg 비율을 계산해서 보여줌
    '''
    sentiments = Sentiment.query.with_entities(Sentiment.type).all()

    sentiment_lst = []
    for i in range(len(sentiments)):
        sentiment_type = ', '.join(map("".join, sentiments[i]))
        sentiment_lst.append(sentiment_type)
    
    if not sentiment_lst:
        return render_template('sentiment.html')

    else:     
        pos_rate = (sentiment_lst.count('pos') / len(sentiment_lst))
        neg_rate = (1 - pos_rate)

        
        rate_lst = [f"{round(pos_rate, 2)*100}%", f"{round(neg_rate, 2)*100}%"]
        header = ['Positive', 'Negative']

        return render_template('sentiment.html', header=header, data=rate_lst)


@bp.route('/feedback', methods=['GET'])
def feedback_index():
    msg_code = request.args.get('msg_code', None)
    alert_msg = main_funcs.msg_processor(msg_code) if msg_code is not None else None

    feedbacks = Feedback.query.all()

    feedback_lst = []
    for i in range(len(feedbacks)):
        read = {'id' : feedbacks[i].id, 'text' : feedbacks[i].text, 'datetime' : feedbacks[i].date.replace(microsecond=0)}
        feedback_lst.append(read)

    return render_template('feedback.html', alert_msg=alert_msg, feedback_lst=feedback_lst)


