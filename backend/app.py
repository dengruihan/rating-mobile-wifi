from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import bcrypt
import json
import os

app = Flask(__name__)
# 配置CORS，明确允许来自前端的请求
CORS(app, origins=['http://localhost:5173', 'http://127.0.0.1:5173'], 
     methods=['GET', 'POST', 'PUT', 'DELETE'], 
     headers=['Content-Type'])  # 允许跨域请求

# 数据库连接函数
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # 使查询结果可以通过列名访问
    return conn

# 初始化数据库
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # 读取并执行创建表的SQL语句
    with open('../database.sql', 'r') as f:
        sql_script = f.read()
    
    cursor.executescript(sql_script)
    conn.commit()
    conn.close()

# 密码哈希函数
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# 密码验证函数
def verify_password(hashed_password, password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

# 注册API
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if not username or not email or not password:
        return jsonify({'message': '缺少必要参数'}), 400
    
    conn = get_db_connection()
    
    # 检查用户名是否已存在
    existing_user = conn.execute('SELECT * FROM User WHERE username = ?', (username,)).fetchone()
    if existing_user:
        conn.close()
        return jsonify({'message': '用户名已存在'}), 400
    
    # 检查邮箱是否已存在
    existing_email = conn.execute('SELECT * FROM User WHERE email = ?', (email,)).fetchone()
    if existing_email:
        conn.close()
        return jsonify({'message': '邮箱已存在'}), 400
    
    # 插入新用户
    hashed_password = hash_password(password)
    conn.execute('INSERT INTO User (username, email, password) VALUES (?, ?, ?)', 
                 (username, email, hashed_password))
    conn.commit()
    conn.close()
    
    return jsonify({'message': '注册成功'}), 201

# 登录API
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'message': '缺少必要参数'}), 400
    
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM User WHERE email = ?', (email,)).fetchone()
    conn.close()
    
    if not user or not verify_password(user['password'], password):
        return jsonify({'message': '邮箱或密码错误'}), 401
    
    # 返回用户信息（不包含密码）
    return jsonify({
        'message': '登录成功',
        'user': {
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'registration_date': user['registration_date']
        }
    }), 200

# 获取所有WiFi型号
@app.route('/api/wifi-models', methods=['GET'])
def get_wifi_models():
    conn = get_db_connection()
    wifi_models = conn.execute('SELECT * FROM WifiModel').fetchall()
    conn.close()
    
    return jsonify([dict(model) for model in wifi_models]), 200

# 获取WiFi型号详情
@app.route('/api/wifi-model/<int:id>', methods=['GET'])
def get_wifi_model(id):
    conn = get_db_connection()
    wifi_model = conn.execute('SELECT * FROM WifiModel WHERE id = ?', (id,)).fetchone()
    data_plans = conn.execute('SELECT * FROM DataPlan WHERE wifiModelId = ?', (id,)).fetchall()
    reviews = conn.execute('SELECT * FROM Review WHERE wifiModelId = ?', (id,)).fetchall()
    conn.close()
    
    if not wifi_model:
        return jsonify({'message': 'WiFi型号不存在'}), 404
    
    return jsonify({
        'wifiModel': dict(wifi_model),
        'dataPlans': [dict(plan) for plan in data_plans],
        'reviews': [dict(review) for review in reviews]
    }), 200

if __name__ == '__main__':
    # 初始化数据库
    if not os.path.exists('database.db'):
        init_db()
    app.run(debug=True, port=5000)
