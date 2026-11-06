# networkPro-lab1-6714951025

Lab 1 – Network Programming: TCP Echo Server และ UDP Server Test ด้วย Python Socket (รองรับการรันด้วย Docker)

- **ผู้จัดทำ:** Nathakorn
- **รหัสนักศึกษา:** 6714951025

## โครงสร้าง Repository

```
networkPro-lab1-6714951025/
├── tcp_echo_server/
│   ├── server.py           # TCP Echo Server
│   ├── client.py           # TCP Client
│   ├── Dockerfile.server   # Docker image ของ TCP server
│   └── Dockerfile.client   # Docker image ของ TCP client
├── udp_server_test/
│   ├── server.py           # UDP Server
│   ├── client.py           # UDP Client
│   ├── Dockerfile.server   # Docker image ของ UDP server
│   └── Dockerfile.client   # Docker image ของ UDP client
├── screenshots/            # ภาพผลการทดสอบ
└── README.md
```

## วิธีดาวน์โหลดและรัน

**ความต้องการ:** Python 3 (ไม่ต้องติดตั้ง library เพิ่ม) และ Docker Desktop (ถ้าต้องการรันแบบ Docker)

```bash
git clone https://github.com/6714951025/networkPro-lab1-6714951025.git
cd networkPro-lab1-6714951025
```

### แบบที่ 1: รันด้วย Python โดยตรง

**ทดสอบ TCP** (เปิด Terminal 2 หน้าต่าง)
```bash
# หน้าต่างที่ 1: เปิด server ก่อน
python tcp_echo_server/server.py

# หน้าต่างที่ 2: รัน client
python tcp_echo_server/client.py
```

**ทดสอบ UDP** (เปิด Terminal 2 หน้าต่าง)
```bash
# หน้าต่างที่ 1: เปิด server ก่อน
python udp_server_test/server.py

# หน้าต่างที่ 2: รัน client
python udp_server_test/client.py
```

### แบบที่ 2: รันด้วย Docker

รันจาก root ของ repo และต้องเปิด Docker Desktop ไว้ก่อน

```bash
# สร้างเครือข่ายให้ container คุยกันได้ (ทำครั้งเดียว)
docker network create labnet
```

**ทดสอบ TCP**
```bash
docker build -t tcp-server -f tcp_echo_server/Dockerfile.server tcp_echo_server
docker build -t tcp-client -f tcp_echo_server/Dockerfile.client tcp_echo_server

# หน้าต่างที่ 1: เปิด server
docker run --rm --name tcp-server --network labnet tcp-server

# หน้าต่างที่ 2: รัน client แล้วปิด server
docker run --rm --network labnet tcp-client
docker stop tcp-server
```

**ทดสอบ UDP**
```bash
docker build -t udp-server -f udp_server_test/Dockerfile.server udp_server_test
docker build -t udp-client -f udp_server_test/Dockerfile.client udp_server_test

# หน้าต่างที่ 1: เปิด server
docker run --rm --name udp-server --network labnet udp-server

# หน้าต่างที่ 2: รัน client แล้วปิด server
docker run --rm --network labnet udp-client
docker stop udp-server
```

## ผลการทดสอบ

### TCP Echo Server (พอร์ต 5000)
Client ส่งข้อความ `Hello TCP from 6714951025` ไปที่ server และได้รับข้อความเดิมกลับมาครบถ้วน

![TCP Result](screenshots/tcp_result.png)

### UDP Server Test (พอร์ต 5001)
Client ส่งข้อความ `Hello UDP from 6714951025` ไปที่ server และได้รับข้อความเดิมกลับมาครบถ้วน

![UDP Result](screenshots/udp_result.png)

### ทดสอบบน Docker
Server และ Client รันแยกกันคนละ container และสื่อสารกันผ่านเครือข่าย `labnet` (server เห็นการเชื่อมต่อจาก IP ของ container client เช่น `172.18.0.3`)

**TCP บน Docker**

![TCP Docker Result](screenshots/tcp_docker_result.png)

**UDP บน Docker**

![UDP Docker Result](screenshots/udp_docker_result.png)

### สรุปผล

| การทดสอบ | Python โดยตรง | Docker |
|---|---|---|
| TCP Echo | ✅ ผ่าน | ✅ ผ่าน |
| UDP | ✅ ผ่าน | ✅ ผ่าน |

## การเลือกใช้เทคนิคและเครื่องมือ

| หัวข้อ | TCP | UDP |
|---|---|---|
| ชนิด socket | `SOCK_STREAM` | `SOCK_DGRAM` |
| ต้องเชื่อมต่อก่อนส่ง | ต้อง (`connect` / `accept`) | ไม่ต้อง |
| คำสั่งส่ง / รับ | `sendall` / `recv` | `sendto` / `recvfrom` |
| การรับประกันข้อมูล | รับประกันว่าถึงครบและเรียงลำดับ | ไม่รับประกัน |
| เหมาะกับ | งานที่ข้อมูลต้องครบ เช่น เว็บ, ไฟล์ | งานที่ต้องการความเร็ว เช่น เกม, สตรีมมิ่ง |

**เหตุผลที่เลือก:**
- **Python** มีโมดูล `socket` ในตัว ไม่ต้องติดตั้งเพิ่ม โค้ดสั้นและอ่านง่าย
- **TCP** ใช้กับ Echo Server เพราะต้องการให้ข้อความกลับมาครบและถูกต้อง
- **UDP** ใช้ทดสอบการส่งแบบไม่ต้องเชื่อมต่อ จึงตั้ง `settimeout(5)` ไว้กันโปรแกรมค้างถ้าแพ็กเก็ตหาย
- ใช้ `127.0.0.1` (localhost) เพื่อทดสอบบนเครื่องเดียว และแยกพอร์ต TCP (5000) กับ UDP (5001) ไม่ให้ชนกัน
- ฝั่ง client มีการตรวจว่าข้อความที่ได้กลับมาตรงกับที่ส่งไป เพื่อยืนยันผลการทดสอบ
- **Docker** ใช้แยก server และ client ไว้คนละ container เพื่อจำลองการสื่อสารข้ามเครื่องจริง และให้รันได้เหมือนกันทุกเครื่อง
- โค้ดอ่าน IP จาก environment variable (`HOST`, `SERVER_HOST`) จึงรันได้ทั้งบนเครื่องปกติและใน Docker โดยไม่ต้องแก้โค้ด
- ใน Docker server ใช้ `HOST=0.0.0.0` เพื่อรับการเชื่อมต่อจาก container อื่น และ client เรียก server ด้วยชื่อ container (`tcp-server`, `udp-server`)

## แหล่งอ้างอิง

1. Python Software Foundation. *socket — Low-level networking interface.* https://docs.python.org/3/library/socket.html
2. Python Software Foundation. *Socket Programming HOWTO.* https://docs.python.org/3/howto/sockets.html
3. Git Documentation. *git clone.* https://git-scm.com/docs/git-clone
4. Docker Documentation. *Dockerfile reference.* https://docs.docker.com/reference/dockerfile/
5. Docker Documentation. *Networking overview.* https://docs.docker.com/engine/network/