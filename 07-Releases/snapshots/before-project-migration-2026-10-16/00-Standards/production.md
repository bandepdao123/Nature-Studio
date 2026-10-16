# Quy trình sản xuất — v1.0

## Trước sản xuất

- Đọc brief, đúng kênh và output-contract; phân biệt tạo mới với sửa sản phẩm cũ.
- Tra kiến thức, giới hạn model và bài học active liên quan; kiểm idea-ledger. Không bắt buộc phải có bài học cũ mới làm.
- Tạo vài hướng trong quá trình phát triển, chọn hướng phù hợp yêu cầu; giữ ý tưởng đã chốt khi chỉ sửa cục bộ. Tránh lặp cơ chế/key/kết cục chỉ bằng thay tên loài hoặc màu mồi.
- Khóa trạng thái đầu, chuỗi lực, diễn biến và hậu quả; áp nhịp riêng của kênh. Không thay chân thực bằng tính gây sốc.

## Hồ sơ và ID

- Mỗi kênh có prefix tại CHANNEL.md. Tra toàn bộ ID hiện có dưới thư mục kênh sản xuất và idea-ledger trước khi cấp số tiếp theo. Không tái dùng ID; nếu nhiều phiên cùng ghi, tạo thư mục giữ chỗ độc quyền rồi mới làm. Có thể dùng hậu tố thời gian để tránh va chạm khi cần và ghi rõ.
- Mỗi production có brief/research/concept/feedback/performance/SUMMARY theo template; mỗi attempt A01, A02... giữ inputs, prompt, settings, review và media thực sự có.
- INPUTS ghi đường dẫn và phiên bản, ảnh input chính xác và hash nếu công cụ có; ghi model/giao diện/thông số thực sự dùng. Không đoán seed hoặc setting ẩn.
- Viết prompt không đồng nghĩa sinh ảnh/video. Chỉ lưu file media khi thật sự có; không tạo file rỗng giả render. Không tạo clip hoặc lượt trả phí ngoài phạm vi giao việc.

## Sau lần thử

- Review đúng vật đã truy cập; phân biệt lỗi ở brief, dữ kiện, ảnh đầu, prompt, model, setting hoặc hậu kỳ. Không kết luận nguyên nhân duy nhất nếu chưa tách biến.
- Khi so sánh, giữ điều kiện khác ổn định khi khả thi; ghi chính xác thay đổi và đánh đổi.
- Cập nhật SUMMARY và idea-ledger bằng thông tin cần tra nhanh, liên kết bài học thay vì sao chép.
- Chỉ cập nhật quy chuẩn/bộ nhớ theo memory-policy; số view không thay thế QA kỹ thuật.
