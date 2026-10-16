# Nature Studio — điểm vào cho AI

Đọc START-HERE.md và SYSTEM.md trước khi thực hiện công việc trong kho.

Phiên bản toàn hệ thống đọc từ VERSION, thay đổi ở CHANGELOG.md. Khi nhận link GitHub để hiểu hệ thống hoặc yêu cầu cập nhật, đọc README.md và thực hiện UPDATE.md; đối chiếu commit/hash và thay đổi local trước khi ghi. Không coi link nguồn là bằng chứng đã biết bản đang dùng của người dùng.

Trước khi phát triển concept mới, đọc [hướng dẫn sáng tạo chung](00-Standards/creativity.md) và hướng dẫn riêng được PROJECT.md chỉ định. Ví dụ không giới hạn không gian câu chuyện; rà lịch sử và kiểm độ mới ở hành vi/nhân quả. Revision giữ ý định đã chốt.

Khi người dùng gửi `/chayvideo` hoặc yêu cầu tạo bộ nội dung qua đặc trưng dự án (loài, chủ đề, môi trường, thị trường, format), đọc và thực hiện [.agents/skills/chayvideo/SKILL.md](.agents/skills/chayvideo/SKILL.md). Đây là quy ước nhận lệnh trong nội dung tin nhắn; không giả định đã đăng ký một slash command của giao diện. Không kích hoạt sản xuất khi người dùng chỉ trích dẫn, giải thích hoặc sửa chính lệnh/skill này.

Skill đọc quy chuẩn và lịch sử đúng dự án trước khi tạo ý tưởng. Mặc định của skill: Ý TƯỞNG tiếng Việt; FIRST FRAME PROMPT và VIDEO PROMPT tiếng Anh, CAPTION tiếng Anh Mỹ tự nhiên kèm hashtag; mỗi prompt là một đoạn văn. Tự tra metadata các dự án để chọn dự án khớp rõ; chỉ hỏi khi mơ hồ hoặc chưa có dự án phù hợp. Không kích hoạt sản xuất từ câu hỏi kiến thức đơn thuần. Không khởi chạy tạo media chỉ từ lệnh này.

Version: 1.5 | Updated: 2026-10-16 | Reason: Nature Studio v1.1, /dongvideo và bộ nhớ Project/shared.

Khi người dùng gọi `/dongvideo` hoặc yêu cầu tổng kết/đóng phiên video và rút bài học, đọc [.agents/skills/dongvideo/SKILL.md](.agents/skills/dongvideo/SKILL.md). Không kích hoạt từ trích dẫn, câu hỏi hay sửa skill. Lệnh tổng kết tiếng Việt, luôn xét Project và shared, không tự render/push hay duyệt video. Bộ nhớ theo [memory-policy](00-Standards/memory-policy.md): /chayvideo chỉ áp active đúng điều kiện; /dongvideo có quyền tự kích hoạt phương pháp khách quan khi đạt đủ gate đã duyệt, không tự thay chính sách sáng tạo.
