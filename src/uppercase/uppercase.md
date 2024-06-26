# UPPERCASE
Sever: 112.137.129.129:27017

Cho 1 xâu có độ dài *len*, biến xâu thành in hoa và gửi lại.

Mỗi gói tin gồm tối thiểu 2 trường:
- type: int 4 bytes, little endian, là loại gói tin.
- len: int 4 bytes, little endian, là độ dài của *data* đi kèm đằng sau.

Mỗi gói tin có thể kèm theo *data* có độ dài *len*.

## Types:
- 0: PKT_HELLO
  - là gói tin đầu tiên trao đổi, bắt buộc phải có.
  - Trường *len* là độ dài của mã sinh viên.
  - Trường *data* theo sau là string có độ dài *len* chứa mã sinh viên.
- 1: PKT_STRING
  - Server sẽ gửi xâu cần xử lý qua gói tin này.
  - Trường *len* là độ dài của xâu cần xử lý.
  - Trường *data* theo sau là string có độ dài *len* chứa xâu cần xử lý.
- 2: PKT_RESULT:
  - Client gửi kết quả bằng gói tin này sau khi nhận PKT_STRING.
  - Trường *len* chứa độ dài của xâu.
  - Trường *data* đằng sau chứa xâu sau khi thay đổi.
- 3: PKT_BYE
  - Server từ chối kết quả, kết nối chấm dứt.
- 4: PKT_FLAG
  - Server gửi gói tin này sau khi client trả lời hết toàn bộ câu hỏi.
  - Trường *len* có giá trị bằng độ dài *flag*.
  - Trường *data* theo sau là *flag* có độ dài *len*.
  - Kết nối chấm dứt.
  - Sinh viên nộp *flag* được trả về từ server lên máy chủ và điểm sẽ được công nhận.
