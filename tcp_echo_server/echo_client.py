# tcp_echo_server/echo_client.py
# TCP Client: พิมพ์ข้อความส่งไปหา server ได้หลายครั้ง พิมพ์ exit เพื่อออก

import os
import socket

# อ่านชื่อ server จาก Docker (ENV SERVER_HOST) ถ้าไม่มีใช้ localhost
HOST = os.environ.get("SERVER_HOST", "127.0.0.1")
PORT = 5000  # ต้องตรงกับพอร์ตของ server

def main():
    # สร้าง socket แบบ TCP (SOCK_STREAM)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(5)          # รอ server ตอบได้สูงสุด 5 วินาที
        s.connect((HOST, PORT))  # เชื่อมต่อไปที่ server ครั้งเดียว
        print(f"[TCP] เชื่อมต่อกับ {HOST}:{PORT} สำเร็จ")

        count = 0  # นับจำนวนข้อความที่ส่งสำเร็จ
        while True:
            msg = input("พิมพ์ข้อความ (พิมพ์ exit เพื่อออก): ")
            if msg.lower() == "exit":
                break
            if not msg:          # ข้ามถ้ากด Enter เปล่าๆ
                continue

            s.sendall(msg.encode())  # ส่งข้อความ
            reply = s.recv(1024)     # รอรับข้อความที่ส่งกลับ
            print(f"[TCP] Server ตอบกลับ: {reply.decode()}")

            # เช็คว่าข้อความที่ได้กลับมาตรงกับที่ส่งไปไหม
            if reply.decode() == msg:
                count += 1
                print("[TCP] ✅ ข้อความตรงกัน")
            else:
                print("[TCP] ❌ ข้อความไม่ตรงกัน")

        print(f"[TCP] ส่งสำเร็จทั้งหมด {count} ข้อความ ปิดการเชื่อมต่อ")

if __name__ == "__main__":
    try:
        main()
    except ConnectionRefusedError:
        print("[TCP] ❌ เชื่อมต่อไม่ได้: ยังไม่ได้เปิด server")
    except socket.timeout:
        print("[TCP] ❌ หมดเวลารอ server ตอบกลับ")
    except (KeyboardInterrupt, EOFError):
        print("\n[TCP] ปิด client แล้ว")