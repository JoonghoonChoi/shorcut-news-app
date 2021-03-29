'''
다른 디렉토리에서 객체를 불러오는데 자꾸 경로 오류가 생김 
아래처럼 일단 해결은 했는데 이유를 모르겠음
지금 파일로부터 세번 위의 경로를 추가해서 지정해줌 (main_funcs.py > utils > news_app > section3-project)
이제 이게 경로로 지정되었기 때문에 news_app 디렉토리로 접근 가능한 것 같음
'''
# import os, sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
# import pickle
from textblob import TextBlob
from news_app.services.textblob_api import clf
from news_app.services.tweepy_api import get_timeline
import time
# from googletrans import Translator

# # pickle 모델 불러오기
# f = open('clf.pickle', 'rb')
# clf = pickle.load(f)
# f.close


def get_sentiment(headline):
    '''
    1. tweepy_api에서 get_timeline 모듈로 얻은 딕셔너리 중 headline 키값을 사용
    2. 각 헤드라인의 텍스트를 분석하여 sentiment(pos/neg) 값을 반환
    3. 텍스트를 분석하는 textblob 라이브러리 자체에서 구글 번역 API를 사용하도록 되어있음
    4. 디버깅 중 너무 많이 요청을 보내서인지 구글 api로부터 차단당한 상태..ㅠㅠ

    => 영어 헤드라인은 가능하겠는데 한국 기사의 경우 어떻게 해야할 지 고민
    '''

    sentiment_lst = []
    for i in range(len(headline)):
        detect = TextBlob(headline[i]).detect_language()
        
        if detect == 'en':
            sentiment_lst.append(clf.classify(headline[i]))

        else:
            translated = str(TextBlob(headline[i]).translate(to='en'))
            sentiment_lst.append(clf.classify(translated[i]))
        
        time.sleep(1)

    return sentiment_lst


# headline = get_timeline('bbcbreaking')['headline']
# print(get_sentiment(headline))
