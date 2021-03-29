# import os, sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier
# import pandas as pd

'''
heroku 배포시 memory quota exceeded 문제로 해당 훈련데이터를 불러오지 않고 적은 임의의 값으로만 모델 훈련시킴
'''
# data1 = pd.read_csv('./news_app/services/amazon_cells_labelled.txt', delimiter="\t", header=None)
# data2 = pd.read_csv('./news_app/services/imdb_labelled.txt', delimiter="\t", header=None)
# data3 = pd.read_csv('./news_app/services/yelp_labelled.txt', delimiter="\t", header=None)

# data = pd.concat([data1, data2, data3])

# text = data[0].tolist()
# sentiment = data[1].replace(1, 'pos').replace(0, 'neg').tolist()


train = [('I love this sandwich.', 'pos'),
        ('this is an amazing place!', 'pos'),
        ('I feel very good about these beers.', 'pos'),
        ('this is my best work.', 'pos'),
        ("what an awesome view", 'pos'),
        ('I do not like this restaurant', 'neg'),
        ('I am tired of this stuff.', 'neg'),
        ("I can't deal with this", 'neg'),
        ('he is my sworn enemy!', 'neg'),
        ('my boss is horrible.', 'neg')
        ]

# test = []

# for i in range(0, 2400):
#     tup_rev_sen = text[i], sentiment[i]
#     train.append(tup_rev_sen)

# for i in range(2400, 2748):
#     tup_for_test = text[i], sentiment[i]
#     test.append(tup_for_test)

clf = NaiveBayesClassifier(train)

# print(clf.accuracy(test))


# '''
# heroku 업로드 용량 때문에 문제가 생길 것 같은 불안감
# 모델을 pickle 파일에 담기
# '''
# f = open('clf.pickle', 'wb')
# pickle.dump(clf, f)
# f.close
