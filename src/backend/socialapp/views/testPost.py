#!/usr/bin/env python3
import requests 


def request_p(urlTo,authID,host,name,url,github):
	print(url)
	data = {
	    "id": authID,
	    "host":host,
	    "displayName":name,
	    "url":url,
	    "github": github
	}
	headers = {
	    "accept": "application/json"
	}
	r=requests.post(urlTo,
	    data=data,
	    headers=headers)
	data = r.json()
	return data


def request_g(url):
	print(url)
	r=requests.get(url)
	data = r.json()
	return data

id_1 = "http://127.0.0.1:8000/api/author/40519df2-e3af-4d48-a735-30c64d6d43d3"
host_1 = "http://127.0.0.1:8000"
name_1 = "jejewittt"
url_1 = "http://127.0.0.1:8000/api/author/40519df2-e3af-4d48-a735-30c64d6d43d3"
url_2 = "http://127.0.0.1:8000/api/posts/63a73b1e-2c6c-4d11-816f-544abc2a17f7"

github_1 = "https://github.com/jejewittt"
p = request_p(urlTo=url_2,authID=id_1,host=host_1,name=name_1,url=url_1,github=github_1)
print(p)
g = request_g(url=url_1)
print(g)
g_2 = request_g(url=url_2)
print(g_2)