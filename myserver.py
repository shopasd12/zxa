from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Server is running!"

# ฟังก์ชันที่ใช้ในการเริ่มต้นเซิร์ฟเวอร์
def reu():
    app.run(host='0.0.0.0', port=8080)

# ฟังก์ชัน server_no ที่ใช้รันฟังก์ชัน reu ใน Thread
def server_no():
    t = Thread(target=reu)  # ใช้ target=reu แทน Tarhrt=run
    t.start()
