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

def find_position_2d_array(x, N, M, array):
    for i in range(N):
        for j in range(M):
            if array[i][j] == x:
                return i, j
    return -1, -1

def main():
    server_address = ('112.137.129.129', 27006)
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(server_address)
        print("Connected to the server.")

        student_id = "21020456"
        send_packet(sock, PKT_HELLO, student_id.encode('utf-8'))
        print("Sent PKT_HELLO packet.")

        while True:
            packet_type, data = receive_packet(sock)
            if packet_type is None:
                break
            if packet_type == PKT_CALC:
                x, N, M, *array_data = struct.unpack('<' + 'i' * (3 + N * M), data)
                array = [array_data[i:i+M] for i in range(0, len(array_data), M)]
                print("Received PKT_CALC packet with x =", x, ", N =", N, ", M =", M, ", and array:", array)
                
                # Find the position of x in the 2D array
                i, j = find_position_2d_array(x, N, M, array)
                
                # Sending the result back to the server
                send_packet(sock, PKT_RESULT, struct.pack('<ii', i, j))
                print("Sent PKT_RESULT packet with result:", i, j)
            elif packet_type == PKT_FLAG:
                # Sending the flag back to the server
                flag = data.decode('utf-8')
                send_packet(sock, PKT_FLAG, flag.encode('utf-8'))
                print("Sent PKT_FLAG packet with flag:", flag)
                break
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()
