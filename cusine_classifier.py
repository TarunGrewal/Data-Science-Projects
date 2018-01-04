
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
df=pd.read_csv('cus.csv',delimiter='\t')
from sklearn.utils import shuffle
df = shuffle(df)
df.reset_index(inplace=True)
df.drop('index',axis=1,inplace=True)
X=df.iloc[:,0].values
y=df.iloc[:,1].values
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
    y_pred=clf.predict(x_t)
    return lc.inverse_transform(y_pred)[0]
    
    
