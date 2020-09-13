from pymongo import MongoClient
import re, json
from urllib.parse import urlparse

link_pattern = re.compile(r'[htpsf]{3,5}://[^\s/$.?#].[^\s\\<"]*')
# domain_pattern = re.compile(r'[htpsf]{3,5}://(.*?)/{0,1}.*') #  $1
domain_pattern = re.compile(r'[htpsf]{3,5}://([^/]*)/?.*') #  $1
# link_pattern = re.compile('https?')
# result = prog.match(string)

# mongodb://edupower:Education4mySoul@10.122.2.100:27017/edupower
# client = MongoClient('mongodb://edupower:Education4mySoul@10.122.2.100:27017/edupower')

print('---- get data from mongo')
client = MongoClient('mongodb://edupower:Education4mySoul@172.31.0.49:27017/edupower')
db = client['edupower']
res = db.base_content.find({ "data": { "$regex": ".*(https?|ftp):\/\/[^\s\/$.?#].[^\s\\<\"]*.*"} })
client.close()

res_dict = {}
type(res)

print('---- transform data')

for i in res:
    # print(type(i))
    # tmp_dict = json.loads(str(i))
    res_dict[str(i['_id'])] = i['data']

print('---- load content_id of tasks')

tasks = {}
with open('tasks.json', 'r') as f:
    tasks = json.load(f)

task_dict = {}
for i in tasks:
    task_dict[i['content_id']] = ''

# print(task_dict)

print('---- work with data')

data = {}

stats = {'in': 0, 'notin': 0}

for i in res_dict:
    # print('%s --> %s' % (i, res_dict[i]))
    if i in task_dict:
        stats['in'] += 1
        res = link_pattern.findall(res_dict[i])
        if len(res) == 0:
            print('!!! %s' % res_dict[i])
        else:
            # print('-------------------------------------------------------------------------------------------')
            for y in res:
                # print(y)
                link = domain_pattern.findall(y)[0]
                link_split = str.split(link, '.')
                if len(link_split) > 1:
                    domain = '.'.join(str.split(link, '.')[-2:])
                else:
                    domain = link

                if domain not in data:
                    data[domain] = {}
                    data[domain][y] = 1
                else:
                    if y not in data[domain]:
                        data[domain][y] = 1
                    else:
                        data[domain][y] += 1
    else:
        stats['notin'] += 1
        print('%s not in task list!' % i)

print('Stats: %s' % stats)

with open('result.json', 'w', encoding='UTF-8') as f:
    f.write(json.dumps(data, ensure_ascii=False))
