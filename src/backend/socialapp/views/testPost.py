#!/usr/bin/env python3
import requests 
import json

def request_p(urlTo,authID,host,name,url,github, postId, qtype):
	# print(url)

	data = {
		"query":qtype,
		"postid":postId,
		"url":urlTo,
		"author":{ 
			"id":authID,
			"host":host,
			"displayName":name,
			"url":url,
			"github": github,
		},
		"friends":[
			"http://127.0.0.1:5454/author/eee13126-4fc2-4c0e-9e86-ffaa3e3fbac8",
			"http://127.0.0.1:5454/author/eee13126-4ac2-4c0e-9e86-ffaa3e3fbac9"
		]
	}
	headers = {
		"accept": "application/json",
		'Content-Type': 'application/json',
		# "HTTP_HOST": "127.0.0.1"
	}
	r=requests.post(urlTo,
		data=json.dumps(data),
		headers=headers)
	data = r#.json()
	return data


def request_g(url):
	# print(url)
	r=requests.get(url)
	data = r.json()
	return data

post_id_1 = "eee13126-4dc2-4c0e-9e86-ffaa3e3fbac6"
id_1 = "http://127.0.0.1:8000/api/author/eee13126-4dc2-4c0e-9e86-ffaa3e3fbac6"
host_1 = "http://127.0.0.1:8000"
name_1 = "jejewittt"
url_1 = "http://127.0.0.1:8000/api/author/eee13126-4dc2-4c0e-9e86-ffaa3e3fbac6"
url_2 = "http://127.0.0.1:8000/api/posts/af10a47f-4afe-4fc9-bd38-8794ecde3db6"
github_1 = "https://github.com/jejewittt"
url_3 = "http://127.0.0.1:8000/api/posts/af10a47f-4afe-4fc9-bd38-8794ecde3db6/comments?page=1&size=1"
qtype_1 = "getPost"
qtype_2 = "comments"
#url_2 is the post url
#url_1 is the author url
# p = request_p(url_2,id_1,host_1,name_1,url_1,github_1,post_id_1,qtype_1)
# print(p.content)
p_2 = request_p(url_3,id_1,host_1,name_1,url_1,github_1,post_id_1,qtype_2)
print(p_2.content)
# g = request_g(url=url_1)
# print(g)
# g_2 = request_g(url=url_2)
# print(g_2)
# g_3 = request_g(url="http://127.0.0.1:8000/api/posts")
# print(g_3)