from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.jungletube   
mycol = db.users

# MongoDB에 insert 하기
# db.users.insert_one({'category':'week0','comment':'session_cookie', 'url':'https://youtu.be/tosLBcAX1vk', 'like' : 2})
# db.users.insert_one({'category':'week0','comment':'cookie_token', 'url':'https://youtu.be/GhrvZ5nUWNg',  'like' : 0 })
# db.users.insert_one({'category':'week0','comment':'jinja_Flask', 'url':'https://youtu.be/NKJV0ekmo4U',  'like' : 1 })
# db.users.insert_one({'category':'week2','comment':'dijkstra', 'url':'https://youtu.be/611B-9zk2o4', 'like' : 3})

# MongoDB에서 전체 delete 하기
# db.users.delete_many({})

# MongoDB count하기
count_number = db.users.estimated_document_count()
print(count_number)

# db.users에서 category 찾아서 week만 분류해놓기
category_list = []
for name in db.users.find():
    temp = name['category']
    if temp not in category_list:
        category_list.append(temp)
    category_list.sort(reverse=True)

# 분류된 week를 기준으로 like 순으로 정렬하여 리스트 만들기
# week 올림차순, like 순으로 dictionary 넣기
dict = {}
for i in category_list:
    video_list = list(db.users.find({'category' : i}, {'_id': 0}).sort('like', -1))
    dict[i] = video_list

print(dict)
