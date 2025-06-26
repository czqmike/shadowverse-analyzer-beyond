from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_cors import CORS
from pymongo import MongoClient
from utils import *

app = Flask(__name__)
CORS(app)  # 允许跨域请求

client = MongoClient("mongodb://localhost:27017/")
db = client["game_records"]
collection = db["matches"]

class Match:
    def __init__(self, my_class=0, my_deck='', enemy_class=0, enemy_deck='', 
                 is_first=None, is_win=None, time_stamp=0, user_identifier=''):
        self.my_class = my_class               # 己方职业
        self.my_deck = my_deck                 # 己方卡组
        self.enemy_class = enemy_class         # 敌方职业
        self.enemy_deck = enemy_deck           # 敌方卡组
        self.is_first = is_first               # 先/后手
        self.is_win = is_win                   # win/lose
        self.time_stamp = time_stamp           # 时间戳
        self.user_identifier = user_identifier # 用户标识
   
    def get_keys(self):
       return list(self.__dict__.keys())

    def to_dict(self):
        ret = {}
        for key in self.get_keys():
            ret[key] = getattr(self, key)
        return ret
        

@app.route('/add_record', methods=['POST'])
def add_record():
    data = request.json
    if not is_user_identifier_valid(data):
        return jsonify({'error': 'user_identifier illegal!'}), 400
    required_fields = Match().get_keys()
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400

    # 插入数据库
    record = Match(**data).to_dict()
    result = collection.insert_one(record)
    return jsonify({'message': 'Record added', 'id': str(result.inserted_id)}), 201

# 可选：获取所有战绩（调试用）
@app.route('/records', methods=['GET'])
def get_records():
    records = []
    for r in collection.find():
        r['_id'] = str(r['_id'])
        records.append(r)
    return jsonify(records)

## 获取指定用户的记录
@app.route('/get_records', methods=['POST'])
def get_records_by_userid():
    data = request.json
    if not is_user_identifier_valid(data):
        return jsonify({'error': 'user_identifier illegal!'}), 400
    records = []
    for r in collection.find({'user_identifier': data['user_identifier']}):
        r['_id'] = str(r['_id'])
        records.append(r)
    return jsonify(records)

def get_recent_matches(n=20):
    cursor = collection.find().sort([('_id', -1)]).limit(n)
    return list(cursor)[::-1]


if __name__ == "__main__":
    app.run(debug=True)