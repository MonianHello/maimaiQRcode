import cv2
from pyzbar.pyzbar import decode
import sqlite3
import tkinter as tk
from datetime import datetime

conn = sqlite3.connect('user_system.sqlite')
cursor = conn.cursor()

root = tk.Tk()
root.title("maimaiDX / Chunithm")

result_label = tk.Label(root, text="请扫描二维码：", font=("Arial", 14))
result_label.pack(pady=10)

def scan_qrcode():
    cap = cv2.VideoCapture(0)
    
    while True:
        _, frame = cap.read()
        decoded_objects = decode(frame)
        
        for obj in decoded_objects:
            if obj.type == 'QRCODE':
                token = obj.data.decode('utf-8')[4:]
                print(f"扫描到的Token: {token}")
                
                # 查询数据库获取用户名、数据和过期时间
                cursor.execute("SELECT username, data, expiration_time FROM users WHERE token = ?", (token,))
                user = cursor.fetchone()
                
                if user:
                    username, data, expiration_time = user
                    current_time = datetime.now().timestamp()
                    
                    if current_time <= expiration_time:
                        result_label.config(text=f"用户名: {username}\n数据: {data}")
                    else:
                        result_label.config(text="二维码已过期")
                    
                    # 关闭摄像头
                    cap.release()
                    cv2.destroyAllWindows()
                    return
                
                else:
                    result_label.config(text="二维码已过期")
        
        root.update()
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

scan_button = tk.Button(root, text="扫描二维码", command=scan_qrcode)
scan_button.pack(pady=10)


root.mainloop()
conn.close()
