# Nature Studio — bắt đầu tại đây

Kho sản xuất nội dung thiên nhiên, lưu trên máy; khởi tạo 15/10/2026 (Asia/Saigon).

## Lệnh tạo bộ nội dung

Gửi `/chayvideo` kèm tên kênh, loài hoặc brief nếu có. AI đọc [skill chayvideo](.agents/skills/chayvideo/SKILL.md), tra nguồn hiện hành và lịch sử thực trước khi chọn ý tưởng; trả bốn mục: Ý TƯỞNG tiếng Việt; FIRST FRAME PROMPT và VIDEO PROMPT tiếng Anh; CAPTION tiếng Anh Mỹ tự nhiên kèm hashtag. Có thể chỉ nêu đặc trưng dự án trong yêu cầu tạo nội dung, skill tự tra kênh phù hợp; chỉ hỏi khi mơ hồ hoặc không có kênh khớp. Mỗi prompt là một đoạn văn. Khi thiếu lựa chọn bắt buộc, skill hỏi đúng phần còn thiếu. Lệnh chỉ tạo văn bản và hồ sơ local, không tự render/đăng.

Đây là quy ước nhận lệnh trong chat qua [AGENTS.md](AGENTS.md), không phải cam kết giao diện có menu slash riêng. Updated: 2026-10-16.

## Cách dùng với bất kỳ AI nào

Giao file này cùng yêu cầu và quyền đọc thư mục Nature-Studio. Nếu AI không truy cập ổ E:, gửi gói hướng dẫn độc lập ở 07-Releases/standalone-guides/. Không giả định AI nhớ lịch sử chat.

1. Đọc [SYSTEM.md](SYSTEM.md); xác định nhiệm vụ: nghiên cứu, ý tưởng, viết prompt, tạo media, review hay cập nhật hệ thống.
2. Xác định kênh; đọc CHANNEL.md của đúng kênh. Kênh đã cấu hình: [Under Fishing US](03-Channels/under-fishing-us/CHANNEL.md). Thiếu kênh và không suy được từ yêu cầu thì hỏi một câu ngắn.
3. Đọc format, đối tượng/giọng và hợp đồng đầu ra của kênh; sau đó lấy đúng hướng dẫn nhiệm vụ từ [Standards](00-Standards/INDEX.md).
4. Tra [Knowledge](01-Knowledge/INDEX.md) theo loài, môi trường, tương tác/dụng cụ; tra [Models](02-Models/INDEX.md) khi cần thông tin model/giao diện.
5. Tra [Memory](05-Memory/INDEX.md): chỉ áp dụng bài học active đúng phạm vi; đọc idea-ledger của kênh để tránh lặp. Kho hiện chưa có bài học active hoặc lịch sử ý tưởng được chuẩn hóa.
6. Khi sản xuất, tạo hồ sơ bằng mẫu trong 00-Standards/templates/. Ghi phiên bản tài liệu/đầu vào đã dùng; mỗi lần thử là một thư mục mới. Không tạo/render nếu yêu cầu chỉ viết prompt.
7. Review sản phẩm thực tế khi có; ghi phản hồi, chỉ đưa kết luận đủ cơ sở vào bộ nhớ theo memory-policy.md. Khi chỉ có prompt thì chỉ kiểm được prompt.

Không đọc toàn bộ kho mỗi lượt. Nếu không tìm thấy thông tin, tìm theo tiêu đề/thẻ/nội dung; thiếu chỉ mục không có nghĩa tài liệu không tồn tại. Không bắt người dùng tự điền mọi trường mẫu mới bắt đầu.

## Trạng thái khởi tạo

- Under Fishing có quy chuẩn kế thừa v1.9, đã phân tách theo phạm vi.
- Nguồn v1.9 được giữ nguyên ở bản phát hành nhập ban đầu; không kế thừa v1.8.
- Chưa nhập video/render cũ, chưa đo lại audio, chưa xác nhận hiệu quả retention hay viral.
- Chưa có model test mới, bài học active hoặc ca đánh giá đã chạy đạt.
