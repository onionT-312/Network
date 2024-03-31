Tìm số nguyên tố nhỏ hơn n ( n nhận từ server)
Server: 112.137.129.129:27003

Mỗi gói tin gồm tối thiểu 2 trường

- type: int 4 bytes, little endian, là loại gói tin

- len: int 4 bytes, little endian, là độ dài data đi kèm đằng sau

Mỗi gói tin có thể kèm theo data có độ dài len

Type:

- 0: PKT_HELLO

- là gói tin đầu tiên trao đổi, bắt buộc phải có

- data theo sau là string chứa mã sinh viên (bắt buộc)

- độ dài của mã sinh viên chứa trong trường len.

- 1: PKT_CALC

- Server sẽ gửi yêu cầu tính toán qua gói tin này

- Trường len có giá trị bằng 4

- data đằng sau sẽ gồm 4 bytes: int, little endian, là số a

- 2: PKT_RESULT:

- Client gửi kết quả bằng gói tin này sau khi nhận PKT_CALC

- Trường len có giá trị bằng 4

- data đằng sau gồm 4 bytes: int, little endian, là kết quả của bài toán trên

- 3: PKT_BYE

- Server từ chối kết quả, kết nối chấm dứt

- 4: PKT_FLAG

- Server gửi gói tin này sau khi client trả lời hết toàn bộ câu hỏi

- Trường len có giá trị bằng độ dài flag

- data theo sau là flag có độ dài len

- Kết nối chấm dứt

- Sinh viên nộp flag được trả về từ server lên máy chủ và điểm sẽ được công nhận
