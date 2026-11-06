# udp_server_test/udp_client.py
# UDP Client: พิมพ์ข้อความส่งไปหา server ได้หลายครั้ง พิมพ์ exit เพื่อออก

import os
import socket

# อ่านชื่อ server จาก Docker (ENV SERVER_HOST) ถ้าไม่มีใช้ localhost
HOST = os.environ.get("SERVER_HOST", "127.0.0.1")
PORT = 5001  # ต้องตรงกับพอร์ตของ server

def main():
    # สร้าง socket แบบ UDP (SOCK_DGRAM) ไม่ต้อง connect
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.settimeout(5)  # UDP ไม่รับประกันการส่ง จึงต้องตั้งเวลารอ
        print(f"[UDP] พร้อมส่งข้อความไปที่ {HOST}:{PORT}")

        count = 0  # นับจำนวนข้อความที่ส่งสำเร็จ
        while True:
            msg = input("พิมพ์ข้อความ (พิมพ์ exit เพื่อออก): ")
            if msg.lower() == "exit":
                break
            if not msg:  # ข้ามถ้ากด Enter เปล่าๆ
                continue

            s.sendto(msg.encode(), (HOST, PORT))  # ส่งข้อความ
            try:
                reply, addr = s.recvfrom(1024)    # รอรับคำตอบ
            except socket.timeout:
                print("[UDP] ❌ หมดเวลารอ: ข้อความนี้อาจหาย")
                continue

            print(f"[UDP] Server {addr} ตอบกลับ: {reply.decode()}")
            if reply.decode() == msg:
                count += 1
                print("[UDP] ✅ ข้อความตรงกัน")
            else:
                print("[UDP] ❌ ข้อความไม่ตรงกัน")

        print(f"[UDP] ส่งสำเร็จทั้งหมด {count} ข้อความ")

if __name__ == "__main__":
    try:
        main()
    except ConnectionResetError:
        print("[UDP] ❌ ไม่มี server รออยู่ที่พอร์ตนี้")
    except (KeyboardInterrupt, EOFError):
        print("\n[UDP] ปิด client แล้ว")