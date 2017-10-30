import asyncio
import pymongo
from pymongo import MongoClient
cl=MongoClient()
db=cl.flip
col=db.flipcol
from aiohttp import ClientSession
from bs4 import BeautifulSoup
r=[]
async def prod(url):
 async with ClientSession() as session:
  async with session.get(url) as response:
   response = await response.read()
   soup2=BeautifulSoup(response.decode('utf-8'),'html.parser')
   for i in soup2.find_all('a',{'class':'_2cLu-l'}):
    r.append(i['href'])
   return (soup2)
loop = asyncio.get_event_loop()
pagen=1
tasks = []
url = 'https://www.flipkart.com/search?as=off&as-show=off&otracker=start&page={}&q={}&viewType=grid'
qw=input('Enter product name ')
qw1=int(input('Enter no of pages '))
qw1=qw1+1

for i in range(1,qw1):
    task = asyncio.ensure_future(prod(url.format(i,qw)))
    tasks.append(task)
loop.run_until_complete(asyncio.wait(tasks))
async def home(url):
 async with ClientSession() as session:
  async with session.get(url) as response:
    response=await response.read()
    soup1=  BeautifulSoup(response.decode('utf-8'),'html.parser')
    price=soup1.find('div',{'class':'_1vC4OE _37U4_g'})
    name=soup1.find('h1',{'class':'_3eAQiD'})
    post={'Price':price.text,'Name':name.text}
    rev=[]
    for k in soup1.find_all('li',{'class':'_1KuY3T row'}):
     post.update({k.find('div').text:k.find('ul').text})
    for j in soup1.find_all('div',{'class':'qwjRop'}):
     s=soup1.find('div',{'class':'_1i0wk8'})
     rev.append('{}={}'.format(s.text,j.text))
    post.update({'Reviews':rev})
#    print(post)
    col.insert_one(post).inserted_id
  #  rr.append(post)


   #print(name.text)
    # print(s.text)
   #print(price.text)

qloop = asyncio.get_event_loop()
tas=[]
ee=0
for i in r:
 task2 = asyncio.ensure_future(home('https://www.flipkart.com{}'.format(i)))
 tas.append(task2)
 ee=ee+1
qloop.run_until_complete(asyncio.wait(tas))
print(ee)
