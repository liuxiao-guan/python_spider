# -*- coding:utf-8 -*-
#from urllib import request
import urllib.request
from bs4 import BeautifulSoup 
import re
import time
import json


url = "http://ugs.whu.edu.cn/"
request = urllib.request.Request(url)
request.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36 Edg/85.0.564.44")
#下载网页
response = urllib.request.urlopen(request).read()
#将网页解码成utf-8
response = response.decode("utf-8")
#打印出网页内容
#print (response)

#网页解析器
soup = BeautifulSoup(response, 'html.parser')
links =soup.find_all('a', href = re.compile(r'info/+\d'))
grab_url = [ ]
for link in links:
#	print(link['href'])
	url = "http://ugs.whu.edu.cn/" + str(link.get('href'))
#	url = str(link.get('href'))
	grab_url.append(url)
grab_data = [ ]
for url in grab_url:
	request = urllib.request.Request(url)
	request.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36 Edg/85.0.564.44")
	#下载网页
	response = urllib.request.urlopen(request).read()
	#将网页解码成utf-8
	response = response.decode("utf-8")
	#打印出网页内容
	#print (response)

	#网页解析器
	soup = BeautifulSoup(response, 'html.parser')
	time.sleep(0.1)
	data = { }
	partment = soup.find(class_ = "title")
	data[''] = partment.get_text()
	#获取标题
	title_node = soup.find(class_ = "title")
	data['title'] = title_node.get_text()
	#获取时间
	repattern = re.compile(r'\d\d\d\d-\d\d-\d\d')
	data['time'] = repattern.findall(response)[0]
	data['html_source'] = url
	
	content_node = soup.find_all('p')
	grab_text = [ ]
	for text in content_node:
		text = text.get_text()
		new_text = re.sub('\u3000|\xa0|\n|© 武汉大学本科生院版权所有 中国武汉珞珈山(430072) 鄂ICP备05003330','',text)
		grab_text.append(new_text)

	#	grab_text.append(text)
	for i in grab_text:
		if '' in grab_text:
			grab_text.remove('')
	#print(grab_text)
	separator = ''
	grab_text = separator.join(grab_text)
	data['content'] = grab_text
	grab_data.append(data)
	
	with open('data.json', 'w', encoding='utf-8') as file:
		file.write(json.dumps(grab_data, indent=2, ensure_ascii=False))

	


#http://travel.people.com.cn/n1/2020/0905/c41570-31850731.html

#http://renshi.people.com.cn/n1/2020/0904/c139617-31849991.html
#http://society.people.com.cn/n1/2020/0905/c1008-31850713.html
#http://ugs.whu.edu.cn/info/1039/9727.htm
#http://ugs.whu.edu.cn/__local/5/DD/16/7D56DB7AFDAD8D70D9CBEE031F7_A05E1856_37B8.jpg
#http://ugs.whu.edu.cn/__local/D/DC/07/0147FA942ECA58F491A1EA70E0F_47AF26C6_479C.jpg
