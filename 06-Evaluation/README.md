# Đánh giá cải tiến

Các ca khởi tạo có trạng thái not run; chưa xác nhận hệ thống/model đã đạt. Ghi mỗi lượt chạy ở results/ với input, model, phiên bản nguồn, output/bằng chứng, pass/fail/not checked và đánh đổi.

Tách kiểm prompt khỏi kiểm render; ca cần media không thể pass từ văn bản. Kết hợp ca cố định và ca mới để tránh chỉ làm tốt ví dụ quen. So sánh cùng điều kiện khi khả thi; lưu giới hạn khi không kiểm soát được model ngẫu nhiên. Thay đổi lesson/format thì chạy lại ca liên quan và ca hồi quy bị ảnh hưởng.

## Bộ nhớ v1.1

`python scripts/validate_memory.py` kiểm metadata, ID, phạm vi/đường dẫn và điều kiện kích hoạt có thể kiểm bằng cấu trúc. `python -m unittest discover -s scripts/tests` chạy fixture trong thư mục tạm; không tạo lesson trong kho thật. Cả hai không chứng minh quyết định skill hoặc hiệu quả media. Ca có actual not run vẫn chưa chạy. Chỉ ghi pass hành vi AI khi có lượt thực thi và artifacts tương ứng; dry-run QA tài liệu phải ghi đúng là review thiết kế.
