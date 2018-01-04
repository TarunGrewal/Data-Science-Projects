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

client = MongoClient('163.172.130.232', 27017)
client.admin.authenticate('datateam', 'data@user*#', mechanism='SCRAM-SHA-1')
db = client.datateam
col=db.tripadvisorattraction

#e=col.find({'address.country': {'$regex': r'Cambodia|Thailand'},'attractionName': {'$regex': r'Temple|Temples|temple|Mandir|mandir|Mata |Hanuman|hanuman|Devi |Vishnu |Shiva |shivji|Shivji'}})
e=col.find({'address.country': {'$regex': r'Cambodia|Thailand|Myanmar|Bhutan|Mongolia|South Korea|Vietnam|Japan|Singapore|Bhutan|Laos|Taiwan|Vietnam|China'},'categories': {'$regex': r'Sacred & Religious Sites'}})

keep = set(re.sub(r'[^a-zA-Z ]+', '', i['attractionName'].replace('Church','').strip()) for i in e)
keep = set(re.sub(r'[^a-zA-Z ]+', '', i['attractionName'].replace('Cathedral','').strip()) for i in keep)
keep = set(re.sub(r'[^a-zA-Z ]+', '', i['attractionName'].replace('church','').strip()) for i in keep)


stop_words=set(stopwords.words('english'))
tt=[]
for j in e:
    words=word_tokenize(j['attractionName'])
    t=''
    for i in words:
        if i not in stop_words:
            t=t+i+' '
    if len(t)>3:
        tt.append(t.strip())
            
dfchurch=pd.DataFrame(tt)
dfchurch['y']=4

dfchurch.to_csv('budh2840.csv', sep='\t', encoding='utf-8')



dfchurch.to_csv('hindu1643.csv', sep='\t', encoding='utf-8')

muslim=pd.read_csv('muslim3520.csv',delimiter='\t')
muslim.drop('Unnamed: 0',axis=1,inplace=True)

christian=pd.read_csv('churches13666.csv',delimiter='\t')
christian.drop('Unnamed: 0',axis=1,inplace=True)
hindu=pd.read_csv('hindu3436.csv',delimiter='\t')
hindu.drop('Unnamed: 0',axis=1,inplace=True)
sikh=pd.read_csv('sikh375.csv',delimiter='\t')
sikh.drop('Unnamed: 0',axis=1,inplace=True)
budh=pd.read_csv('budh2840.csv',delimiter='\t')
budh.drop('Unnamed: 0',axis=1,inplace=True)
frames=[christian[0:3500],hindu,sikh,budh[0:2320],muslim[0:1600]]
result = pd.concat(frames)

from sklearn.utils import shuffle
df = shuffle(result)
df.reset_index(inplace=True)
df.drop('index',axis=1,inplace=True)

X=df.iloc[:,0].values
y=df.iloc[:,1].values

'''from sklearn.naive_bayes import GaussianNB
classifier=GaussianNB()
classifier.fit(X,y_train)
classifier = nltk.NaiveBayesClassifier.train(X_train)'''
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
#cv=CountVectorizer(max_features=1500)
cv=TfidfVectorizer(min_df=1,stop_words='english')
X=cv.fit_transform(X).toarray()
from sklearn.cross_validation import train_test_split
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.25,random_state=0)

from sklearn.naive_bayes import MultinomialNB
nb = MultinomialNB()
nb.fit(X_train, y_train)

import pickle
f = open('religion_classifier.pickle', 'wb')
pickle.dump(nb, f)
f.close()

import pickle
from sklearn.metrics import confusion_matrix
f = open('religion_classifier.pickle', 'rb')
nb = pickle.load(f)
f.close()

def r(f):
    x_t=cv.transform([f])
    y_pred=nb.predict(x_t)
    cm=confusion_matrix(y_test,y_pred)
    if(y_pred[0]==0):
        print('Christian')
    elif(y_pred[0]==1):
        print('Muslim')
    elif(y_pred[0]==3):
        print('Hindu')
    elif(y_pred[0]==2):
        print('Sikh')
    elif(y_pred[0]==4):
        print('Buddhism')
    
    

    

