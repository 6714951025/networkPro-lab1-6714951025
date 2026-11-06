# tcp_echo_server/server.py
# TCP Echo Server: รับข้อความจาก client แล้วส่งข้อความเดิมกลับไป

import socket

HOST = "127.0.0.1"  # IP ของเครื่องตัวเอง (localhost)
PORT = 5000         # พอร์ตที่ server เปิดรอ

def main():
    # สร้าง socket แบบ TCP (SOCK_STREAM)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # ให้ใช้พอร์ตเดิมซ้ำได้ทันทีหลังปิด server
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))  # ผูก socket กับ IP และพอร์ต
        s.listen()            # เริ่มรอการเชื่อมต่อ
        print(f"[TCP] Server รออยู่ที่ {HOST}:{PORT} (กด Ctrl+C เพื่อปิด)")

        while True:  # วนรับ client ได้หลายครั้ง
            conn, addr = s.accept()  # รอ client มาเชื่อมต่อ
            with conn:
                print(f"[TCP] มีการเชื่อมต่อจาก {addr}")
                while True:
                    data = conn.recv(1024)  # รับข้อมูลสูงสุด 1024 bytes
                    if not data:            # client ปิดการเชื่อมต่อแล้ว
                        break
                    print(f"[TCP] ได้รับ: {data.decode()}")
                    conn.sendall(data)      # ส่งข้อมูลเดิมกลับไป (echo)
                    print("[TCP] ส่งกลับเรียบร้อย")
                print(f"[TCP] {addr} ตัดการเชื่อมต่อ")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[TCP] ปิด server แล้ว")