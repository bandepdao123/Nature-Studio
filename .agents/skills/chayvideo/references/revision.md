# Sửa/tiếp tục clip

Version: 1.1 | Updated: 2026-10-17 | Dùng chung revision tạo mới và chuyển thể

Đọc packet revision và production cụ thể: brief/concept, SUMMARY, attempt được chọn, INPUTS/feedback và media/handoff khi được cung cấp. Không mặc định attempt số lớn nhất là được chọn. Thiếu ngữ cảnh clip cần xác định thì hỏi đúng phần thiếu; chưa rõ không viết chuyện thay thế.

Dùng resolve và base_attempt/base_sha256 theo [lõi chung](../../../../00-Standards/video-prompt-workflow.md#tiếp-tục-đúng-bộ-đầu-vào) để giữ nguồn từng trường. Đối chiếu frame_state khi sửa chuyện/prompt; thiếu xác nhận t=0 thì unverified. Nếu tiếp tục dùng ảnh đã QA, kiểm handoff theo first-frame.md; sửa văn bản không tự ghi lại handoff hoặc sinh ảnh.

Giữ loài/ý định/key/kết cục đã chốt ngoài phần người dùng yêu cầu đổi. Không chạy brainstorm hoặc rà toàn bộ lịch sử để buộc mới; nếu yêu cầu thực sự là concept mới thì chuyển new. Mở thêm Knowledge/nguồn ngoài chỉ phần thay đổi và liên đới; sửa rig có thể ảnh hưởng mồi/móc/dây/lực/ảnh đầu/âm/caption, phải kiểm cả chuỗi. Sửa prompt ảnh không có nghĩa được tạo ảnh.

Yêu cầu thay đổi rõ thì sửa đúng phần được giao, không bắt chẩn đoán lỗi hoặc có render mới được sửa. Khi xử lý lỗi, dựa trên vật thực sự đã kiểm để xét nơi cần sửa: brief/concept, bố cục/trạng thái đầu, bộ đầu vào/media được chọn, cách diễn đạt prompt hoặc kết quả/model/settings. Ghi gọn quan sát → nguyên nhân nghi ngờ → phần sửa và phần cần kiểm lại trong INPUTS/review/revision hiện có; chưa rõ thì giữ là giả thuyết, không suy một lần render lỗi thành model không có khả năng. Nếu chỉ có phản hồi người dùng thì ghi nguồn phản hồi, không nhận AI đã quan sát media. Với chuyện/prompt đã đổi, đối chiếu phần liên quan theo bước G của Story Development; caption-only giữ nhánh nhẹ, không mở lại chuyện/QA ảnh khi không liên quan.

Giữ quy chuẩn hiện hành trừ ngoại lệ người dùng chốt cho clip; phát hiện mâu thuẫn thực tế thì nêu/correct gần ý định. Kiểm chéo các mục bị ảnh hưởng. Trả đúng phần được giao, lưu attempt mới với before/after hoặc tham chiếu phần giữ nguyên; không ghi đè lịch sử/quota ảnh. Cập nhật SUMMARY/concept/ledger khi cơ chế hoặc trạng thái thật thay đổi; fingerprint cũ hết hạn khi có thêm nguồn, không tự giữ kết luận cũ.
