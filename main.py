from flask import Flask, request, render_template, url_for
import sqlite3
import qrcode
from datetime import datetime

import time

app = Flask(__name__)

def generate_token():
    import random
    import string
    token_length = 76
    characters = "ABCDEF" + string.digits
    return "MAID"+''.join(random.choice(characters) for _ in range(token_length))

@app.route('/')
def index():
    return "maimaiDX / Chunithm"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        data = request.form['data']
        
        conn = sqlite3.connect('user_system.sqlite')
        cursor = conn.cursor()
        
        cursor.execute("INSERT INTO users (username, password, data) VALUES (?, ?, ?)", (username, password, data))
        
        conn.commit()
        conn.close()
        
        return "注册成功"
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_message = ""
    expiration_time = 0
    image_url = ""
    login_successful = False

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('user_system.sqlite')
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        
        if user:
            login_successful = True
            new_token = generate_token()
            expiration_time = int(time.time()) + 600
            
            cursor.execute("UPDATE users SET token = ?, expiration_time = ? WHERE username = ?", (new_token, expiration_time, username))
            conn.commit()
            
            conn.close()
            
            # qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
            # qr.add_data(new_token)
            # qr.make(fit=True)
            # img = qr.make_image(fill_color="black", back_color="white", size=(200, 200))
            # img.save(f"static/{username}_qrcode.png")
            # image_url = url_for('static', filename=f"{username}_qrcode.png")

            image_url = "http://wq.sys-all.cn/qrcode/img/{}.png?v".format(new_token)
            login_message = f"登录成功"
        else:
            conn.close()
            login_message = f"登录失败，请检查你的用户名和密码"
    
    return render_template('login.html', login_message=login_message, expiration_time=datetime.fromtimestamp(expiration_time).strftime('%#m/%#d %H:%M'), image_url=image_url, login_successful=login_successful)


if __name__ == '__main__':
    app.run(host='192.168.100.3', port=5000, debug=True)
