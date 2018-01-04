import re
import codecs
from requests import get
from bs4 import BeautifulSoup as bs
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
hotel_name=['Maya hotel']
for i in hotel_name:
    reg=re.sub(' ','+',i)
    response=get('https://duckduckgo.com/?q={}&t=hf&ia=web'.format(reg))   
    dcod=codecs.decode(response.text, 'unicode_escape')
    soup=bs(dcod,'lxml')
    regfirstlink=re.compile("'/d.js.*sp=1'")
    string=str(soup)
    regoutput=regfirstlink.findall(string)
    regoutput=r[0].split(',')[0]
    flink=re.sub("[']",'',regoutput)
    response=get('https://duckduckgo.com{}'.format(flink))
    dcod=codecs.decode(response.text, 'unicode_escape')
    soup=bs(dcod,'lxml')
    regfinal=re.compile(r'"en":[[]"[h,t,p,s,w,/,:].*[A-Za-z][a-z]*[A-Za-z.][A-Za-z.]*,')
    regfinal=regfinal.findall(str(soup))[0]
    regfinal=regfinal.split(',')[0]
    url=regfinal[7:-1]
    test_string_one=url.split("/")[2]
    match_percentile=fuzz.ratio(hotel_name[0],test_string_one)
    if match_percentile>30:
            print url
    else:
            print "no url"
