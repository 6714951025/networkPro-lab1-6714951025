# tcp_echo_server/client.py
# TCP Client: ส่งข้อความไปหา server แล้วรอรับข้อความที่ส่งกลับมา

import os
import socket

# อ่านชื่อ server จาก Docker (ENV SERVER_HOST) ถ้าไม่มีใช้ localhost
HOST = os.environ.get("SERVER_HOST", "127.0.0.1")
PORT = 5000  # ต้องตรงกับพอร์ตของ server

def main():
    # สร้าง socket แบบ TCP (SOCK_STREAM)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(5)          # รอได้สูงสุด 5 วินาที
        s.connect((HOST, PORT))  # เชื่อมต่อไปที่ server
        print(f"[TCP] เชื่อมต่อกับ {HOST}:{PORT} สำเร็จ")

        msg = "Hello TCP from 6714951025"
        s.sendall(msg.encode())  # แปลงข้อความเป็น bytes แล้วส่ง
        print(f"[TCP] ส่ง: {msg}")

        reply = s.recv(1024)     # รอรับข้อความที่ server ส่งกลับ
        print(f"[TCP] Server ตอบกลับ: {reply.decode()}")

        # เช็คว่าข้อความที่ได้กลับมาตรงกับที่ส่งไปไหม
        if reply.decode() == msg:
            print("[TCP] ✅ ทดสอบสำเร็จ: ข้อความตรงกัน")
        else:
            print("[TCP] ❌ ข้อความไม่ตรงกัน")

if __name__ == "__main__":
    try:
        main()
    except ConnectionRefusedError:
        print("[TCP] ❌ เชื่อมต่อไม่ได้: ยังไม่ได้เปิด server")
    except socket.timeout:
        print("[TCP] ❌ หมดเวลารอ server ตอบกลับ")