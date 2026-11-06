# udp_server_test/client.py
# UDP Client: ส่งข้อความไปหา server แล้วรอรับคำตอบ

import os
import socket

# อ่านชื่อ server จาก Docker (ENV SERVER_HOST) ถ้าไม่มีใช้ localhost
HOST = os.environ.get("SERVER_HOST", "127.0.0.1")
PORT = 5001  # ต้องตรงกับพอร์ตของ server

def main():
    # สร้าง socket แบบ UDP (SOCK_DGRAM)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.settimeout(5)  # UDP ไม่รับประกันการส่ง จึงต้องตั้งเวลารอ

        msg = "Hello UDP from 6714951025"
        s.sendto(msg.encode(), (HOST, PORT))  # ส่งได้เลย ไม่ต้อง connect
        print(f"[UDP] ส่ง: {msg}")

        reply, addr = s.recvfrom(1024)  # รอรับคำตอบ
        print(f"[UDP] Server {addr} ตอบกลับ: {reply.decode()}")

        # เช็คว่าข้อความตรงกับที่ส่งไปไหม
        if reply.decode() == msg:
            print("[UDP] ✅ ทดสอบสำเร็จ: ข้อความตรงกัน")
        else:
            print("[UDP] ❌ ข้อความไม่ตรงกัน")

if __name__ == "__main__":
    try:
        main()
    except socket.timeout:
        print("[UDP] ❌ หมดเวลารอ: server อาจยังไม่เปิด")
    except ConnectionResetError:
        print("[UDP] ❌ ไม่มี server รออยู่ที่พอร์ตนี้")