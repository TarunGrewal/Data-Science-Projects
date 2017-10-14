import sqlite3
from wrapper import *
import getpass
class s():
###############################################################################################################################################
 def __init__(self):
  x=''
  self.x=x
  conn=sqlite3.connect('phase2.db')
  cursor=conn.cursor()
  self.conn=conn
  self.cursor=cursor
  cursor.execute('''CREATE TABLE IF NOT EXISTS users (
     username text AUTO_INCREMENT PRIMARY KEY,
     Name text,
     password text,
     email_id text,
     contact number text,
     Balance INT,
     Earning INT);''')
  cursor.execute('''CREATE TABLE IF NOT EXISTS stocks (
     username text,
     Symbol text PRIMARY KEY,
     Stock_Numbers int,
     LastPrice INT,
     Timestamp text,
     High double,
     Low double,
     Value INT,
     FOREIGN KEY (username) REFERENCES users(username));''')
###############################################################################################################################################
 def regist(self):
  cursor=self.cursor
  conn=self.conn
  nam=input("Enter Name \n")
  usernam=input("Enter Userame \n")
  pasw=getpass.getpass("Enter Password \n")
  email=input("Enter email_id \n")
  cont=input("Enter contact number \n")
  cursor.execute('''INSERT INTO users VALUES ('{}','{}','{}','{}','{}',1000000,0);'''.format(usernam,nam,pasw,email,cont))
  conn.commit()
  print('Succussfully registered \n')
###############################################################################################################################################
 def login(self):
  cursor=self.cursor
  conn=self.conn
  conn.commit()
  q=False
  ppp=True
  ll=True
  while(q==False):
   oo=True
   if(ppp==True):
    if(ll==False):
     print('ERROR LOGIN TRY AGAIN!')
     o=input("Enter c for continue or q for quit \n")
     if(o=='q'):
      q=True
      break
    logi=input("Enter Username \n")
    paswl=getpass.getpass("Enter Password \n")
    if(oo==True):
     for i in cursor.execute('SELECT username,password,Name FROM users'):
      q=False
      if(i[0]==logi and i[1]==paswl):
       print("Successful Login")
       print("Hy",i[2])
       q=True
       self.x=i[0]
       y=['True']
       return(True)
      else:
       q=False
       ll=False
###############################################################################################################################################
 def st(self):
  x=self.x
  cursor=self.cursor
  conn=self.conn
  ff=input("Enter 1 for Portfolio \nEnter 2 to buy stocks \nEnter 3 to sell stocks\nEnter 4 to quit")
  ff=int(ff)
  return(ff)
###############################################################################################################################################
 def buy(self):
  x=self.x
  cursor=self.cursor
  conn=self.conn
  rt=cursor.execute("SELECT Balance FROM users WHERE username='{}'".format(x))
  uu=rt.fetchone()[0]
  print("current balance is ",uu)
  y=input("Enter Company Name: \n")
  p=look(y)
  ll=0
  print("Exchange:\n")
  x=self.x
  for i in p:
   ll=ll+1
   print(ll,i['Exchange'],i['Symbol'])
  pp=input("Enter Your Wish to get data: \n")
  pp=int(pp)
  rr=get_quote(p[pp-1]['Symbol'])
  ke=list(rr.keys())
  va=list(rr.values())
  for i in range(0,len(ke)-1):
   print(ke[i],va[i])
  buyin=input('Enter number of stocks to buy or Enter 0 to go to previous page\n')
  buyin=int(buyin)
  ee=rr['LastPrice']
  ee=int(ee)
  de=cursor.execute("SELECT Stock_Numbers FROM stocks WHERE (username='{}' and Symbol='{}'); ".format(x,rr['Symbol']))
  er=de.fetchall()
  if(buyin!=0):
   cursor.execute('''INSERT OR IGNORE INTO stocks VALUES ('{}','{}',{},{},'{}',{},{},{})'''.format(x,rr['Symbol'],buyin,ee,rr['Timestamp'],rr['High'],rr['Low'],buyin*ee))
   if(buyin*ee<=uu):
    print(er)
    cursor.execute('''UPDATE users SET Balance={} WHERE username='{}' '''.format(uu-(buyin*ee),x))
    if (er):
     cursor.execute('''UPDATE stocks SET Stock_Numbers='{}' WHERE (username='{}' and Symbol='{}'); '''.format(er[0][0]+buyin,x,rr['Symbol']))
     cursor.execute('''UPDATE stocks SET Value='{}' WHERE (username='{}' and Symbol='{}'); '''.format(er[0][0]+(buyin*ee),x,rr['Symbol']))

    conn.commit()
    print("Current Balance is:",uu-(buyin*ee))
   else:
    print("NOT ENOUGH MONEY!")
  elif(buyin==0):
   self.buy()
###############################################################################################################################################
 def sell(self):
  x=self.x
  cursor=self.cursor
  conn=self.conn
  sy=[]
  st=[]
  rtt=cursor.execute("SELECT symbol FROM stocks WHERE username='{}'".format(x))
  for i in rtt.fetchall():
   sy.append(i)
  rt=cursor.execute("SELECT Balance FROM users WHERE username='{}'".format(x))
  uu=rt.fetchone()[0]
  print('Current Balance:',uu)
  eee=cursor.execute('''SELECT Stock_Numbers FROM stocks WHERE username='{}'; '''.format(x))
  for i in eee.fetchall():
   st.append(i)
  iw=1
  for i in range(0,len(sy)):
   print('{}.'.format(iw),sy[i][0],st[i][0])
   iw=iw+1
  rq=eee.fetchall()
  selin=input('Enter your Symbol option \n')
  selin=int(selin)
  rr=get_quote(sy[selin-1][0])
  err=rr['LastPrice']
  err=int(err)
  how=input('How much you want to sell\n')
  how=int(how)
  if(how<=st[selin-1][0]):
   cursor.execute('''UPDATE stocks SET Stock_Numbers='{}' WHERE (username='{}' and Symbol='{}'); '''.format(st[selin-1][0]-how,x,sy[selin-1][0]))
   wq=cursor.execute('''SELECT Earning from users WHERE username='{}' '''.format(x))
   ui=wq.fetchall()
   wwq=cursor.execute('''SELECT LastPrice from stocks WHERE (username='{}' and Symbol='{}'); '''.format(x,sy[selin-1][0]))
   ui2=wwq.fetchall()
   y=(((err*how)-(ui2[0][0]*how))+ui[0][0])
   cursor.execute('''UPDATE users SET Earning='{}' WHERE username='{}' '''.format(y,x))
   cursor.execute('''UPDATE users SET Balance='{}' WHERE username='{}' '''.format(uu+(how*err),x))
   conn.commit()
  else:
   print("Error!You entered more than you have")
  print("Current Balance is:",(uu+(how*err)))
######################################################################################################################################################
 def portfolio(self):
  x=self.x
  cursor=self.cursor
  conn=self.conn
  r=cursor.execute("SELECT Name,Balance from users WHERE username='{}'; ".format(x))
  for i in r.fetchall():
   print('_______________')
   print('----------Name:',i[0],'----------')
   print('----------Balance:',i[1],'----------')
   print('________________')
  er=cursor.execute("SELECT Symbol,Stock_Numbers,LastPrice,High,Low,Balance from users NATURAL JOIN stocks WHERE username='{}'; ".format(x))
  for i in er.fetchall():
   print('Symbol:',i[0])
   print('Stock Quantity:',i[1])
   print('LastPrice:',i[2])
   print('High:',i[3])
   print('Low:',i[4])
   print('___________________________________________________________________________________________________________________________')
###############################################################################################################################################
 def superuser(self):
  x=self.x
  cursor=self.cursor
  conn=self.conn
  r=cursor.execute("SELECT Name,Earning from users ORDER BY Earning ASC; ")
  for i in r.fetchall():
   print('_______________')
   print('----------Name:',i[0],'----------')
   print('----------Earning:',i[1],'----------')
   print('________________')


t=True
while(t==True):
 conn=sqlite3.connect('phase2.db')
 cursor=conn.cursor()
 reg=input("Enter 1 for Registration \nEnter 2 for Login \nEnter 3 to clear all data\nEnter 4 to superuser\nEnter 5 to quit\n")
 reg=int(reg)
 rr=s()
 if(reg==1):
  rr.regist()
 elif(reg==2):
  if(rr.login()==True):
   log=True
   while(log==True):
    o=input("Enter 1 for Portfolio \nEnter 2 to buy stocks \nEnter 3 to sell stocks\nEnter 4 to logout\nEnter 5 to quit\n")
    o=int(o)
    if(o==1):
     rr.portfolio()
    elif(o==2):
     rr.buy()
    elif(o==3):
     rr.sell()
    elif(o==4):
     print("Logged Out!")
     log=False
    elif(o==5):
     t=False
     log=False
     print('BYE :-)')
 elif(reg==3):
  y=input('Admin Id\n')
  r=getpass.getpass("Admin Password \n")
  if(y=='blue' and r=='car'):
   cursor.execute('''DROP TABLE IF EXISTS stocks''')
   cursor.execute('''DROP TABLE IF EXISTS users''')
   conn.commit()
   print('Done')
  else:
   print('Wrong Password')
 elif(reg==5):
  t=False
  print('BYE :-)')
 elif(reg==4):
  rr.superuser()
