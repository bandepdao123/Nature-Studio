# Quy trình sản xuất — v1.3

## Trước sản xuất

- Đọc brief, đúng dự án và output-contract; phân biệt tạo mới với sửa sản phẩm cũ.
- Tra kiến thức, giới hạn model và bài học active liên quan; kiểm idea-ledger. Không bắt buộc phải có bài học cũ mới làm.
- Tạo vài hướng trong quá trình phát triển, chọn hướng phù hợp yêu cầu; giữ ý tưởng đã chốt khi chỉ sửa cục bộ. Tránh lặp cơ chế/key/kết cục chỉ bằng thay tên loài hoặc màu mồi.
- Khóa trạng thái đầu, chuỗi lực, diễn biến và hậu quả; áp nhịp riêng của dự án. Không thay chân thực bằng tính gây sốc.

## Hồ sơ và ID

- Video mới theo [quy tắc mã](video-identifiers.md): XXX-yyyyy, ba chữ riêng Project local và số từ 00001. Dùng scripts/video_ids.py init/reserve, registry local và IDENTITY.json; không tự thêm hậu tố thời gian hoặc đoán mã. Revision dùng mã cũ và attempt mới; giữ nguyên ID legacy.
- Mỗi production có brief/research/concept/feedback/performance/SUMMARY theo template; mỗi attempt A01, A02... giữ inputs, prompt, settings, review và media thực sự có.
- INPUTS ghi đường dẫn và phiên bản, ảnh input chính xác và hash nếu công cụ có; ghi model/giao diện/thông số thực sự dùng. Không đoán seed hoặc setting ẩn.
- Viết prompt không đồng nghĩa sinh ảnh/video. Chỉ lưu file media khi thật sự có; không tạo file rỗng giả render. Không tạo clip hoặc lượt trả phí ngoài phạm vi giao việc.

## Sau lần thử

- Review đúng vật đã truy cập; phân biệt lỗi ở brief, dữ kiện, ảnh đầu, prompt, model, setting hoặc hậu kỳ. Không kết luận nguyên nhân duy nhất nếu chưa tách biến.
- Khi so sánh, giữ điều kiện khác ổn định khi khả thi; ghi chính xác thay đổi và đánh đổi.
- Cập nhật SUMMARY và idea-ledger bằng thông tin cần tra nhanh, liên kết bài học thay vì sao chép.
- Chỉ cập nhật quy chuẩn/bộ nhớ theo memory-policy; số view không thay thế QA kỹ thuật.

Cập nhật 2026-10-16: đơn vị quản lý là Project; đọc Slug trong PROJECT.md để ghi `04-Productions/<slug>/`. Không suy thư mục từ ID ổn định sau đổi tên. Production ID cũ tiếp tục dùng cho lịch sử/revision; video mới theo chuẩn XXX-yyyyy và prefix local, không đổi mã vì đổi tên dự án.

## Tổng kết phiên và vòng học — v1.2, 2026-10-16

/dongvideo dùng SESSION-REVIEW.md theo mẫu để tổng kết phần dữ liệu đã truy cập; luôn đánh giá riêng Project và shared. Không tự đóng từ /chayvideo, không nhầm đóng phiên với selected/QA pass. INPUTS ghi ID/version/cách áp dụng lesson để lần sau đối chiếu kết quả. Thẩm quyền đổi trạng thái chỉ theo memory-policy, không biến giả thuyết thành quy chuẩn.

## Riêng tư khi cập nhật hệ thống

Production, attempt, SESSION-REVIEW và idea-ledger giữ local theo publication.md. Repo chỉ phân phối mẫu ledger. /chayvideo vẫn rà lịch sử local và ghi đầy đủ; tách bài học tái sử dụng sang Memory, không dùng việc đồng bộ hệ thống để tự upload toàn bộ lịch sử.
