from pymongo import MongoClient
import re, json

link_pattern = re.compile(r'(https?|ftp)://[^\s/$.?#].[^\s;\\<"]*')
domain_pattern = re.compile(r'https?://(?:www\.|)([\w.-]+).*') #  $1
# link_pattern = re.compile('https?')
# result = prog.match(string)

# mongodb://edupower:Education4mySoul@10.122.2.100:27017/edupower
# client = MongoClient('mongodb://edupower:Education4mySoul@10.122.2.100:27017/edupower')

print('---- get data from mongo')
client = MongoClient('mongodb://edupower:Education4mySoul@172.31.0.49:27017/edupower')
db = client['edupower']
res = db.base_content.find({ "data": { "$regex": ".*(https?|ftp):\/\/[^\s\/$.?#].[^\s]*.*"} })
client.close()

res_dict = {}
type(res)

print('---- transform data')

for i in res:
    # print(type(i))
    # tmp_dict = json.loads(str(i))
    res_dict[str(i['_id'])] = i['data']

print('---- work with data')

for i in res_dict:
    # print('%s --> %s' % (i, res_dict[i]))
    for y in link_pattern.search(res_dict[i]):  #  ALL???
        print('%s   ----->   %s' % (domain_pattern.findall(y), y))

# print(res_dict)

# 5f4a818f3f787c00012b7ab1 --> <p><a href="https://ru-static.z-dn.net/files/d6e/8fc6b5b1cb983e539eaab24a315a56ba.jpg">https://ru-static.z-dn.net/files/d6e/8fc6b5b1cb983e539eaab24a315a56ba.jpg</a><br /><br /><em><strong>Рассмотрите картинку из известного мультика. Расскажите об увиденном, не глядя на иллюстрацию. </strong></em><br /><br /><br />Выпиши в тетрадь как можно больше существительных, описывающих иллюстрацию. Подготовьтесь к аукциону слов на уроке. Правила игры: каждая группа говорит по одному слову, вычеркивая каждое названное соперником. Побеждает та команда, у которой остались слова.&nbsp;</p>

# 5f4f9d61777a9c0001b10872 --> ﻿<p>В джунглях о. Борнео учёные обнаружили летающую змею и целый род ящериц, названных «Летучими драконами» (Draco sp.). Конечно, они не способны летать, как птицы, однако могут перелетать на расстояния до 100 метров! Несмотря на интересные особенности жизни, эти животные не произвели революции в биологической классификации. Это не мифические создания, а вполне реальные биологические виды, в целом вполне соответствующие признакам своих групп (змеи, ящерицы).</p>
# <p>Представь, как могли бы выглядеть летающая змея и летающая ящерица. Нарисуй их или вылепи. Принеси результат своей работы в класс для представления одноклассникам и последующего обсуждения. При подготовке к работе воспользуйся нашей <a href="https://docs.google.com/document/d/1BGlk9INmOyut7GXLebLR0_GvND2iUmwgCXdwhCD_l7w/edit?usp=sharing">подсказкой</a>.</p>
# <p>Твоя работа будет оцениваться с использованием этого <a href="https://docs.google.com/document/d/15zc1PKrQ7dfwfyaUFCbu68S6zdYS2R23tWO6yTwLg94/edit">рубрикатора</a>.</p>
# <p><em>Идея: покажи свою работу учителю ИЗО и подтверди свой уровень во втором предмете!</em></p>