import tweepy
from dotenv import load_dotenv
import os
load_dotenv()
import re

api_key = os.getenv('api_key')
api_secret = os.getenv('api_secret')
access_token = os.getenv('access_token')
access_secret = os.getenv('access_secret')

auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

def get_timeline(screen_name):
    '''
    1. 뉴스채널 트위터 계정의 타임라인을 불러옴
    2. 불러온 타임라인에서 username, location, headline, link 추출
    3. 각 키에 맞는 값들을 딕셔너리에 담아서 리턴
    '''
    tweets = api.user_timeline(screen_name=screen_name,
                            tweet_mode='extended',
                            include_rts=False,
                            count=10,
                            exclude_replies=True)

    username = []
    location = []
    text = []
    headline = []
    link = []
    
    for t in tweets:
        username.append(t._json['user']['screen_name'])
        location.append(t._json['user']['location'])
        text.append(t.full_text)

    for i in range(len(text)):
        headline.append(text[i].split('https')[0])
        for word in text[i].split():
            http_link = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$\-@\.&+:/?=]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', word) # 정규식으로 http 링크 주소 찾아주기, 리스트로 돌려줌
            if http_link: # 값이 빈 []가 아니라면 링크 리스트에 넣어줌
                link.append(http_link[0])

    timeline_dict = {'username' : username,
                    'location' : location,
                    'headline' : headline,
                    'link' : link}


    return timeline_dict

