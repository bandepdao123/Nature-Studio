# Đánh giá cải tiến

Các ca khởi tạo có trạng thái not run; chưa xác nhận hệ thống/model đã đạt. Ghi mỗi lượt chạy ở results/ với input, model, phiên bản nguồn, output/bằng chứng, pass/fail/not checked và đánh đổi.

Tách kiểm prompt khỏi kiểm render; ca cần media không thể pass từ văn bản. Kết hợp ca cố định và ca mới để tránh chỉ làm tốt ví dụ quen. So sánh cùng điều kiện khi khả thi; lưu giới hạn khi không kiểm soát được model ngẫu nhiên. Thay đổi lesson/format thì chạy lại ca liên quan và ca hồi quy bị ảnh hưởng.
