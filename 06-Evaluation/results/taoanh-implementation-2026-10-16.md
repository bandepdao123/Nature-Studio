# /taoanh — kiểm triển khai local

Date: 2026-10-16 | Skill version: 1.0 | Workspace VERSION: 1.4

Đã cài routing /taoanh, “tạo ảnh”, “tạo first frame”; phương pháp QA chung và guide riêng Underwater; mẫu review/handoff; profile ưu tiên Sunburst và helper quota local. Không tìm được Sunburst thì dùng model mặc định image_gen, không hỏi lại. Danh tính model không là tiêu chí QA; metadata không được nhận Sunburst khi tool không công bố.

Kiểm đã chạy:

- 52 unit test đạt, gồm 10 test mới về giới hạn 5 lượt, không reset khi init lại, lượt lỗi vẫn tính, grant có hồ sơ chấp thuận, cấp lượt đồng thời, tách production và kiểm đường dẫn.
- quick_validate của skill-creator: taoanh và chayvideo hợp lệ.
- validate_memory.py: valid, không lỗi.
- git diff --check với cấu hình CRLF: không lỗi whitespace.
- Rà phần hướng dẫn liên quan: đã bỏ cổng xác minh Sunburst và câu hỏi cho phép backend mặc định.

Chưa chạy sinh ảnh hoặc ca EV-IMAGE-01 bằng AI độc lập. Chưa xác nhận model thực, chất lượng ảnh, sự tuân thủ vòng QA khi gọi tool, hoặc kết quả video. Unit test kiểm sổ quota; agent vẫn phải reserve trước call và tự dừng đúng quy định. Không tiêu lượt production thật để kiểm thử.

Đã bổ sung hướng dẫn UPDATE, CHANGELOG ghi chưa phát hành. Không đổi VERSION, tạo video ID, ghi production/Memory, commit hoặc push. Các thay đổi story-development đang có được giữ nguyên. Manifest ghi hash bản local tại thời điểm hoàn tất, không phải release GitHub.
