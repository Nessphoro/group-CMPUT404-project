#!/usr/bin/env python3
import requests 
import json
import base64

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
			"http://127.0.0.1:5454/author/91803881-10b8-495e-b1e5-7dc905bb25c2",
			"http://127.0.0.1:5454/author/91803881-10b8-495e-b1e5-7dc905bb25c2"
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


def request_g(url, auth=None, head=None):
	# print(url)
	if not auth:
		r=requests.get(url)
		data = r.json()
	if head:
		print(f'{auth}')
		r=requests.get(url, headers={head: f'{auth}'})
		data = r.json()
		
	return data
# 10cdf97e-6ce2-4d87-871c-887a146cffb9

post_id_1 = "eee13126-4dc2-4c0e-9e86-ffaa3e3fbac6"
id_1 = "http://127.0.0.1:8000/api/author/800612ed-07d6-41b8-bd5c-2ec19fded4c4"
host_1 = "http://127.0.0.1:8000"
name_1 = "jejewittt"
url_1 = "http://127.0.0.1:8000/api/author/800612ed-07d6-41b8-bd5c-2ec19fded4c4"
url_2 = "http://127.0.0.1:8000/api/posts/ece0551c-8107-4eb4-b2be-f145c3ae8263"
github_1 = "https://github.com/jejewittt"
url_3 = "http://127.0.0.1:8000/api/posts/9bcb740b-e0d6-42ca-b2c5-b2584e27668d/comments"
qtype_1 = "getPost"
qtype_2 = "comments"
qtype_4 = 'posts'
url_4 = 'http://127.0.0.1:8000/api/author/800612ed-07d6-41b8-bd5c-2ec19fded4c4/posts/'
pwd = "Pass!123"
name = "http://server.com"
concat = f"{name}${pwd}"
concat = base64.b64encode(concat.encode("utf-8"))
concat =f'Basic {concat.decode("utf-8")}'


#url_2 is the post url
#url_1 is the author url

# tests PostViewSet
# p = request_p(url_2,id_1,host_1,name_1,url_1,github_1,post_id_1,qtype_1)
# print(p.content)

# tests PostCommentsViewSet
# p_2 = request_p(url_3,id_1,host_1,name_1,url_1,github_1,post_id_1,qtype_2)
# print(p_2.content)

# AuthoredByPostsViewSet
# p_4 = request_p(url_4,id_1,host_1,name_1,url_1,github_1,post_id_1,qtype_4)
# print(p_4.content)

# p_4 = request_p('http://127.0.0.1:8000/api/author/800612ed-07d6-41b8-bd5c-2ec19fded4c4/friends',id_1,host_1,name_1,url_1,github_1,post_id_1,"friends")
# print(p_4.content)


# http://127.0.0.1:8000/api/author/3455ded2-474b-465d-8ddc-682eedbbc812

# get testing
# g = request_g(url=url_1)
# print(g)
# g_2 = request_g(url=url_2)
# print(g_2)

# g_3 = request_g(url="http://127.0.0.1:8000/api/posts")
# print(g_3)
# g_3 = request_g(url="http://127.0.0.1:8000/api/posts", auth=concat,  head="Authorization")
# print(g_3)


# g_2 = request_g(url="http://127.0.0.1:8000/api/posts/16dc9c58-5daf-434d-b430-fb4fdaa0f4c4", auth=concat)
# print(g_2)

# g_2 = request_g(url="http://127.0.0.1:8000/api/author/3455ded2-474b-465d-8ddc-682eedbbc812/friends/c3277495-b9d1-4325-a266-b211dea9e744", auth=concat)
# print(g_2)

g_2 = request_g(url="http://127.0.0.1:8000/api/author/800612ed-07d6-41b8-bd5c-2ec19fded4c4/friends", auth=concat , head="Authorization")   
print(g_2)

# concat = 'http://127.0.0.1:8001/api/author/800612ed-07d6-41b8-bd5c-2ec19fded4c4'
# concat = base64.b64encode(concat.encode("utf-8"))
# g_2 = request_g(url="http://127.0.0.1:8000/api/author/posts", auth=concat, head="X-USER")
# print(g_2)

# g_2 = request_g(url=url_2, auth=concat, head="X-USER")
# print(g_2)


# data = {
#     "query":"friendrequest",
#     "author":{ 
#         "id":"http://127.0.0.1:5454/author/10cdf97e-6ce2-4d87-871c-887a146cffb9",
#         "host":"http://127.0.0.1:5454/",
#         "displayName":"me",
#         "url":"http://127.0.0.1:5454/author/10cdf97e-6ce2-4d87-871c-887a146cffb9",
#         "github": "eh",
#     },
#     "friend":{ 
# 		"id":"http://127.0.0.1:5454/author/800612ed-07d6-41b8-bd5c-2ec19fded4c4",
#         "host":"http://127.0.0.1:5454/",
#         "displayName":"user1",
#         "url":"http://127.0.0.1:5454/author/800612ed-07d6-41b8-bd5c-2ec19fded4c4",
#         "github": "eh",
#     },
# }
# headers = {
#     "accept": "application/json",
#     'Content-Type': 'application/json',
#     # "HTTP_HOST": "127.0.0.1"
# }
# url = 'http://127.0.0.1:8000/friendrequest'
# r=requests.post(url,
#     data=json.dumps(data),
#     headers=headers)
# data = r#.json()
# print(data.json())