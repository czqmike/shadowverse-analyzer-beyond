from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)  # 允许跨域请求

client = MongoClient("mongodb://localhost:27017/")
db = client["game_records"]
collection = db["matches"]

@app.route('/add_record', methods=['POST'])
def add_record():
    data = request.json
    print("data:", data)
    required_fields = [
        'my_class',      # 己方职业
        'my_deck',       # 己方卡组
        'enemy_class',# 敌方职业
        'enemy_deck', # 敌方卡组
        'is_first', # 先/后手
        'is_win',    # win/lose
    ]
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400

    # 插入数据库
    record = {
        'my_class': data['my_class'],
        'my_deck': data['my_deck'],
        'enemy_class': data['enemy_class'],
        'enemy_deck': data['enemy_deck'],
        'is_first': data['is_first'],
        'is_win': data['is_win']
    }
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

def get_recent_matches(n=20):
    cursor = collection.find().sort([('_id', -1)]).limit(n)
    return list(cursor)[::-1]


if __name__ == "__main__":
    app.run(debug=True)