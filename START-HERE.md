# Nature Studio — bắt đầu tại đây

Kho sản xuất nội dung thiên nhiên, lưu trên máy; khởi tạo 15/10/2026 (Asia/Saigon).

Phiên bản toàn hệ thống: **Nature Studio v1.2**, nguồn máy đọc là [VERSION](VERSION); xem [CHANGELOG.md](CHANGELOG.md). Khi người dùng đưa link GitHub và yêu cầu so sánh/cập nhật, đọc [UPDATE.md](UPDATE.md) trước khi ghi: cần cả bản đích và trạng thái local, giữ dữ liệu riêng và không đoán bản mới từ tên file.

## Lệnh tạo bộ nội dung

Gửi `/chayvideo` kèm tên dự án, loài hoặc brief nếu có. AI đọc [skill chayvideo](.agents/skills/chayvideo/SKILL.md), tra nguồn hiện hành và lịch sử thực trước khi chọn ý tưởng; trả bốn mục: Ý TƯỞNG tiếng Việt; FIRST FRAME PROMPT và VIDEO PROMPT tiếng Anh; CAPTION tiếng Anh Mỹ tự nhiên kèm hashtag. Có thể chỉ nêu đặc trưng dự án trong yêu cầu tạo nội dung, skill tự tra dự án phù hợp; chỉ hỏi khi mơ hồ hoặc không có dự án khớp. Mỗi prompt là một đoạn văn. Khi thiếu lựa chọn bắt buộc, skill hỏi đúng phần còn thiếu. Lệnh chỉ tạo văn bản và hồ sơ local, không tự render/đăng.

Đây là quy ước nhận lệnh trong chat qua [AGENTS.md](AGENTS.md), không phải cam kết giao diện có menu slash riêng. Updated: 2026-10-16.

## Cách dùng với bất kỳ AI nào

Giao file này cùng yêu cầu và quyền đọc thư mục Nature-Studio. Nếu AI không truy cập ổ E:, gửi gói hướng dẫn độc lập ở 07-Releases/standalone-guides/. Không giả định AI nhớ lịch sử chat.

1. Đọc [SYSTEM.md](SYSTEM.md); xác định nhiệm vụ: nghiên cứu, ý tưởng, viết prompt, tạo media, review hay cập nhật hệ thống.
2. Tra [danh mục dự án](03-Projects/INDEX.md), xác định dự án; đọc PROJECT.md của đúng dự án. Dự án đã cấu hình: [Underwater](03-Projects/underwater/PROJECT.md). Thiếu dự án và không suy được từ yêu cầu thì hỏi một câu ngắn.
3. Đọc format, đối tượng/giọng và hợp đồng đầu ra của dự án; sau đó lấy đúng hướng dẫn nhiệm vụ từ [Standards](00-Standards/INDEX.md). Khi tạo ý tưởng mới, bắt buộc đọc [hướng dẫn sáng tạo chung](00-Standards/creativity.md) và tài liệu sáng tạo mà PROJECT.md dẫn tới; Underwater có [Sáng tạo mở](03-Projects/underwater/creative-direction.md). Khi sửa clip, giữ trọng tâm đã chốt.
4. Tra [Knowledge](01-Knowledge/INDEX.md) theo loài, môi trường, tương tác/dụng cụ; tra [Models](02-Models/INDEX.md) khi cần thông tin model/giao diện.
5. Tra [Memory](05-Memory/INDEX.md): đọc INDEX riêng Project và shared, mở bản gốc rồi chỉ áp active đúng điều kiện. Ghi ID/version/cách dùng vào INPUTS; không tự áp lesson Project khác. Đọc idea-ledger và hồ sơ thực để tránh lặp.
6. Khi sản xuất, tạo hồ sơ bằng mẫu trong 00-Standards/templates/. Ghi phiên bản tài liệu/đầu vào đã dùng; mỗi lần thử là một thư mục mới. Không tạo/render nếu yêu cầu chỉ viết prompt.
7. Review sản phẩm thực tế khi có; ghi phản hồi, chỉ đưa kết luận đủ cơ sở vào bộ nhớ theo memory-policy.md. Khi chỉ có prompt thì chỉ kiểm được prompt.

Không đọc toàn bộ kho mỗi lượt. Nếu không tìm thấy thông tin, tìm theo tiêu đề/thẻ/nội dung; thiếu chỉ mục không có nghĩa tài liệu không tồn tại. Không bắt người dùng tự điền mọi trường mẫu mới bắt đầu.

## Trạng thái khởi tạo

- Underwater có quy chuẩn kế thừa v1.9, đã phân tách theo phạm vi.
- Nguồn v1.9 được giữ nguyên ở bản phát hành nhập ban đầu; không kế thừa v1.8.
- Chưa nhập video/render cũ, chưa đo lại audio, chưa xác nhận hiệu quả retention hay viral.
- Chưa có model test mới, bài học active hoặc ca đánh giá đã chạy đạt.

## Cập nhật cấu trúc 2026-10-16

Workspace tổ chức theo Project. Dự án hiện hành: [Underwater](03-Projects/underwater/PROJECT.md), tên cũ Under Fish US / Under Fishing US. Quy chuẩn đã chuyển sang 03-Projects/underwater; hồ sơ sản xuất sang 04-Productions/underwater; mẫu dự án là 00-Standards/templates/project.md. Không có dự án mới được tạo từ lần đổi tên này.

Tên repo cố định là Nature-Studio; nâng VERSION không đổi URL. [REPOSITORY.json](REPOSITORY.json) ghi danh tính nguồn; UPDATE.md hướng dẫn đối chiếu bản đang dùng và bản mới.

## Tổng kết và học sau phiên — v1.1

Gửi `/dongvideo UF-0001` hoặc yêu cầu đóng phiên video cụ thể. Đọc [skill dongvideo](.agents/skills/dongvideo/SKILL.md): tổng kết dữ liệu thực, luôn xét bài học Project và shared; tự lưu candidate, chỉ tự kích hoạt phương pháp đã kiểm khách quan theo [policy](00-Standards/memory-policy.md). Kết luận rộng còn chờ kiểm/duyệt được gom trong báo cáo tiếng Việt. Đóng phiên không tự duyệt video hoặc đẩy GitHub. Gọi lại với cùng dữ liệu không tạo mục trùng.

Nâng từ v1.0: đọc phần migration trong [UPDATE.md](UPDATE.md); bảo toàn production/lesson/chỉnh sửa riêng trước khi chuyển cấu trúc. Chạy `python scripts/validate_memory.py` sau cập nhật.

## Mã video — Nature Studio v1.2

Video mới dùng **XXX-yyyyy**, ba chữ A–Z riêng từng Project local, số từ **00001**. [Quy tắc và công cụ](00-Standards/video-identifiers.md): init tạo prefix, reserve cấp mã an toàn và UUID. Không cấp mã từ câu hỏi hoặc revision. Registry `.nature-studio/` không lên Git, phải được giữ khi backup/di chuyển/cập nhật; không nằm trong gói mẫu. UF-0001 và các attempt lịch sử giữ nguyên. Xem UPDATE.md khi nâng từ v1.1.
