import json
from requests import get
def get_quote(symbol):
 q={'symbol':symbol}
 s = "http://dev.markitondemand.com/Api/v2/Quote/json/"
 res = get(s,q)
 rr = res.json()
 
 ke=list(rr.keys())
 va=list(rr.values())
 
 return rr
def look(l):
 q={'input':l}
 o='http://dev.markitondemand.com/Api/v2/Lookup/json/'
 res=get(o,q)
 r=res.json()
 return r

