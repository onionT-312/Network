import socket
import struct

PKT_HELLO = 0
PKT_CALC = 1
PKT_RESULT = 2
PKT_BYE = 3
PKT_FLAG = 4

def send_packet(sock, packet_type, data=b''):
    packet_len = len(data)
    packet_type = packet_type.to_bytes(4, 'little')
    packet_len = packet_len.to_bytes(4, 'little')
    sock.sendall(packet_type + packet_len + data)

def receive_packet(sock):
    header = sock.recv(8)
    if not header:
        return None, None
    print("Header received:", header)
    packet_type, packet_len = struct.unpack('<ii', header)
    print("Packet received length:", packet_len)
    data = sock.recv(packet_len)
    return packet_type, data
    
def gcd(a, b):
    if(b == 0):
        return abs(a)
    else:
        return hcfnaive(b, a % b)

def main():
    server_address = ('112.137.129.129', 27005)
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Starting the client...")
        sock.connect(server_address)
        print("Connected to the server.")

        student_id = "21020456"
        send_packet(sock, PKT_HELLO, student_id.encode('utf-8'))
        print("Sent PKT_HELLO packet.")

        while True:
            packet_type, data = receive_packet(sock)
            print("Received packet type:", packet_type)
            if packet_type is None:
                break
            if packet_type == PKT_CALC:
                # Extracting values a and b from the received data
                a = int.from_bytes(data[0:4], 'little', signed=True)
                b = int.from_bytes(data[4:8], 'little', signed=True)
                #a = struct.unpack('<i', data[:4])[0]
                #b = struct.unpack('<i', data[4:])[0]
                print("Received a =", a, "and b =", b)
                
                # Calculate the gcd of a and b
                result = gcd(abs(a), abs(b))
                result_bytes = result.to_bytes(4, 'little')
                
                # Sending the result back to the server
                send_packet(sock, PKT_RESULT, result_bytes)
                print("Sent PKT_RESULT packet with the sum:", result)
            elif packet_type == PKT_FLAG:
                flag = data.decode('utf-8')
                print("Received PKT_FLAG packet with flag:", flag)
                break
            else:
                break
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()


