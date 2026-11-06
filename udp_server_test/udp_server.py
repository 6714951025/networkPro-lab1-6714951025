# udp_server_test/server.py
# UDP Server: รับข้อความจาก client แล้วส่งตอบกลับ (ไม่ต้องเชื่อมต่อก่อน)

import os
import socket

# อ่าน IP จาก Docker (ENV HOST) ถ้าไม่มีใช้ localhost
HOST = os.environ.get("HOST", "127.0.0.1")
PORT = 5001  # ใช้พอร์ตคนละอันกับ TCP

def main():
    # สร้าง socket แบบ UDP (SOCK_DGRAM)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOST, PORT))  # ผูก socket กับ IP และพอร์ต
        print(f"[UDP] Server รออยู่ที่ {HOST}:{PORT} (กด Ctrl+C เพื่อปิด)")

        while True:
            data, addr = s.recvfrom(1024)  # รับข้อมูลพร้อมที่อยู่ผู้ส่ง
            print(f"[UDP] ได้รับจาก {addr}: {data.decode()}")
            s.sendto(data, addr)           # ส่งกลับไปที่ผู้ส่ง
            print("[UDP] ส่งกลับเรียบร้อย")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[UDP] ปิด server แล้ว")