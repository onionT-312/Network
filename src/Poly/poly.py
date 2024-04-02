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
    packet_type, packet_len = struct.unpack('<ii', header)
    data = sock.recv(packet_len)
    return packet_type, data

def main():
    server_address = ('112.137.129.129', 27002)
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
                # Extracting values N, M, x, and coefficients A0 to AN from the received data
                N = int.from_bytes(data[0:4], 'little', signed=True)
                M = int.from_bytes(data[4:8], 'little', signed=True)
                x = int.from_bytes(data[8:12], 'little', signed=True)
                coefficients = struct.unpack('<' + 'i' * (N + 1), data[12:])
                print("Received N =", N, ", M =", M, ", x =", x, ", and coefficients:", coefficients)

                # Calculate P(x) mod M
                result = sum(coeff * (x ** exp) for exp, coeff in enumerate(coefficients)) % M

                # Sending the result back to the server
                send_packet(sock, PKT_RESULT, struct.pack('<i', result))
                print("Sent PKT_RESULT packet with the result:", result)
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

