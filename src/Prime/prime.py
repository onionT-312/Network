import socket
import math

PKT_HELLO = 0
PKT_CALC = 1
PKT_RESULT = 2
PKT_BYTE = 3
PKT_FLAG = 4

def send_pack(sock, packet_type, data=b''):
    packet_len = len(data).to_bytes(4, 'little')
    packet_type = packet_type.to_bytes(4, 'little')
    sock.sendall(packet_type + packet_len + data)
    
def receive_pack(sock):
    header = sock.recv(8)
    packet_type = int.from_bytes(header[0:4], 'little')
    packet_len = int.from_bytes(header[4:8], 'little')
    data = sock.recv(packet_len)
    print(f'Receive: packet_type: {packet_type}, packet_len: {packet_len}')
    return packet_type, data

def isPrime(n):
    if n<2:
        return False
    else:
        for i in range(2,(int)(math.sqrt(n) + 1)):
            if n%i==0:
                return False
    return True

def main():
    server_address = ('112.137.129.129', 27003)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    sock.connect(server_address)
    
    student_id = '21020456'
    send_pack(sock, PKT_HELLO, student_id.encode('utf-8'))
    
    while True:
        packet_type, data = receive_pack(sock)
        if packet_type == PKT_CALC:
            a = int.from_bytes(data[0:4], 'little')
            x = a
            result = 0
            while True:
                if isPrime(x):
                    result = x
                    break
                x = x + 1
            print(f'a: {a}, result: {result}')
            result = result.to_bytes(4, 'little')
            send_pack(sock, PKT_RESULT, result)
        elif packet_type == PKT_FLAG:
            flag = data.decode('utf-8')
            print(flag)
            break
        else:
            break
    
if __name__ == "__main__":
    main()
    
