import pymongo
from pymongo import MongoClient
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.utils import shuffle
from bs4 import BeautifulSoup as bs
from requests import get
import re
df1=pd.read_csv('yelp_labelled.csv',delimiter='\t')
df1.columns=['rev','p']
df2=pd.read_csv('amazon_cells_labelled.csv',delimiter='\t')
df2.columns=['rev','p']
df3=pd.read_csv('twitter train.csv',delimiter=',',encoding='ISO-8859-1')
df3.drop('ItemID',axis=1,inplace=True)
df3 = df3.rename(columns={'SentimentText': 'rev','Sentiment':'p'})

frames = [df2, df1,df3]


result = pd.concat(frames)

result

df = shuffle(result)
df.reset_index(inplace=True)
df.drop('index',axis=1,inplace=True)

sw=set(stopwords.words('english'))
df=df
for i in range(len(df)):
    review=df['rev'][i]
    review=' '.join(review.split(' ')[1:])
    review=review.lower()
    review=re.sub('[^a-zA-Z]',' ',review)
    review=review.split(' ')
    
    review = ' '.join(list(filter(None, review)))
    words=word_tokenize(review)
    filt=[w for w in words if not w in sw]
    df['rev'][i]=' '.join(filt)

df.to_csv('finalmixrev.csv', sep='\t', encoding='utf-8')

from sklearn.utils import shuffle
df = shuffle(df)
df.reset_index(inplace=True)
df.drop('index',axis=1,inplace=True)
X=df.iloc[:,1].values
y=df.iloc[:,0].values
from sklearn.preprocessing import LabelEncoder,OneHotEncoder
lc=LabelEncoder()
y=lc.fit_transform(y)



from sklearn.feature_extraction.text import TfidfVectorizer
cv=TfidfVectorizer(min_df=1,stop_words='english')
X=cv.fit_transform(X)
from sklearn.cross_validation import train_test_split
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.25,random_state=0)
from sklearn.linear_model import SGDClassifier

from sklearn.naive_bayes import MultinomialNB
clf = MultinomialNB()
clf.fit(X_train, y_train)

from sklearn.linear_model import SGDClassifier
tc=SGDClassifier(loss='hinge',alpha=1e-3, n_iter=5, random_state=42)
tc.fit(X_train, y_train)

from sklearn.model_selection import GridSearchCV
parameters = {'vect__ngram_range': [(1, 1), (1, 2)],
               'tfidf__use_idf': (True, False),
               'clf__alpha': (1e-2, 1e-3),}

gs_clf = GridSearchCV(tc, parameters, n_jobs=-1,cv=2)
gs_clf = gs_clf.fit((X_train, y_train))

from sklearn.metrics import accuracy_score
y_pred0=tc.predict(X_test)
accuracy_score(y_test, y_pred0)
from sklearn.metrics import confusion_matrix
cm=confusion_matrix(y_test,y_pred0)


def cu(res):
    x_t=cv.transform([res])
    y_pred=tc.predict(x_t)
    r=lc.inverse_transform(y_pred)[0]
    if r==0:
        print('Negative')
    else:
        print('Positive')
    
