# Nature Studio v1.0

Workspace sản xuất nội dung thiên nhiên bằng AI, tổ chức theo **Project**. Tài liệu và lịch sử được lưu bằng file để tiếp tục công việc qua nhiều phiên làm việc.

Đọc [START-HERE.md](START-HERE.md) và [SYSTEM.md](SYSTEM.md) trước khi bắt đầu. AI đọc [AGENTS.md](AGENTS.md) để nhận quy tắc workspace.

## Dành cho AI nhận link GitHub

Đọc [VERSION](VERSION) và [CHANGELOG.md](CHANGELOG.md) để biết phiên bản toàn hệ thống, sau đó theo START-HERE/SYSTEM. Khi kiểm tra hoặc cập nhật từ GitHub, thực hiện [UPDATE.md](UPDATE.md): xác định commit đích, so với bản local và giữ chỉnh sửa riêng trước khi ghi. Chỉ có link repo chưa đủ để biết máy người dùng đã thay đổi gì; cần quyền đọc local hoặc gói workspace/manifest của họ.

Phiên bản hiện hành được đặt tên **Nature Studio v1.0**. Skill/project có số phiên bản riêng. VERSION không tự tạo Git tag/GitHub Release; main có thể chứa thay đổi sau một release, nên luôn ghi kèm commit và trạng thái local. Repository nguồn: [bandepdao123/Nature-Studio](https://github.com/bandepdao123/Nature-Studio).

## Dự án hiện tại

[Underwater](03-Projects/underwater/PROJECT.md): Reel camera dưới nước hướng người câu cá Mỹ. Video mục tiêu 10s, 9:16, một shot; quy chuẩn cụ thể nằm trong hồ sơ dự án. Tên cũ Under Fish US / Under Fishing US chỉ là alias; ID nội bộ và prefix UF được giữ để truy vết.

Đã có hồ sơ [UF-0001](04-Productions/underwater/UF-0001/SUMMARY.md) với lịch sử đến A04: video A03 được review chưa đạt; A04 có ảnh/prompt sửa, video mới chưa render. Đọc SUMMARY/review để biết đúng mức kiểm từng attempt. Các ca đánh giá khởi tạo và hai ca sáng tạo mở mới chưa chạy.

## Hướng dẫn sáng tạo cho AI trong v1.0

Khi được giao tạo mới, đọc [nguyên tắc sáng tạo chung](00-Standards/creativity.md), rồi hướng dẫn riêng của dự án; Underwater dùng [Sáng tạo mở](03-Projects/underwater/creative-direction.md). Luồng làm việc: **brief/dữ kiện → rà lịch sử → tiền đề độc lập → kiểm tính đúng → chọn chuyện → bố trí nhịp → kiểm độ mới → prompt/caption**.

Ví dụ không phải danh sách tình huống đóng. Độ mới được kiểm ở hành vi và nhân quả, không chỉ đổi cá/mồi/địa điểm. Revision giữ câu chuyện đã chốt. Đây là phần bắt buộc khi AI phát triển ý tưởng, kể cả khi chỉ nhận link repo và không gọi skill. Hướng dẫn không bảo đảm mọi kết quả sẽ hay hoặc chưa từng có.

## Gọi skill /chayvideo

Trong workspace, gửi `/chayvideo` kèm loài hoặc ý tưởng, hoặc yêu cầu tạo nội dung bằng đặc trưng dự án. Ví dụ:

```text
/chayvideo Underwater — Walleye, một bộ, tự phát triển ý tưởng mới
```

Skill [chayvideo](.agents/skills/chayvideo/SKILL.md) tự tìm dự án phù hợp, đọc quy chuẩn và rà lịch sử trước khi viết. Đầu ra gồm Ý TƯỞNG tiếng Việt; FIRST FRAME PROMPT và VIDEO PROMPT tiếng Anh, mỗi prompt một đoạn; CAPTION tiếng Anh Mỹ tự nhiên kèm hashtag. Lệnh chỉ tạo văn bản và hồ sơ local; không tự render hoặc đăng bài. `/chayvideo` là quy ước trong tin nhắn, không cam kết mọi giao diện có menu slash riêng.

## Cấu trúc

| Thư mục | Nội dung |
|---|---|
| 00-Standards | Phương pháp và mẫu hồ sơ |
| 01-Knowledge | Kiến thức, nguồn và phạm vi kiểm chứng |
| 02-Models | Hướng dẫn model và giới hạn đã biết |
| 03-Projects | Hồ sơ, quy chuẩn và lịch sử ý tưởng từng dự án |
| 04-Productions | Brief, các lần thử, prompt, review và media thực |
| 05-Memory | Bài học candidate / active / retired |
| 06-Evaluation | Tiêu chí, ca kiểm và kết quả thực |
| 07-Releases | Baseline, manifest và snapshot lịch sử |

Danh mục [dự án](03-Projects/INDEX.md) và [mẫu dự án](00-Standards/templates/project.md) hỗ trợ mở thêm dự án. Không áp quy chuẩn Underwater mặc định cho dự án khác.

## Di chuyển và đóng gói

Clone/tải toàn bộ repo vào một thư mục, mở thư mục đó làm workspace rồi đọc START-HERE.md. Không cần giữ đường dẫn ổ E:. Đường dẫn tuyệt đối trong một số hồ sơ cũ là provenance tại thời điểm tạo; các nguồn hiện hành dùng liên kết tương đối. Snapshot giữ tên Channel/đường dẫn cũ để truy lịch sử; không dùng làm cấu trúc hiện hành.

Tạo ZIP đầy đủ, gồm cả `.agents`, media hiện có và snapshot:

```text
python scripts/package_workspace.py
```

Gói nằm trong `07-Releases/packages/`, kèm manifest SHA256 từng file, phiên bản workspace, commit nguồn và trạng thái thay đổi local. Gói không chứa `.git`, file bí mật, cache hoặc chính các gói ZIP cũ. ZIP và manifest gói được bỏ qua khi commit để tránh lưu lặp nội dung. Khi dùng ZIP, giữ PACKAGE-MANIFEST.json làm baseline để lần cập nhật sau đối chiếu; tên file gói có phiên bản nhưng không thay việc kiểm hash.

Repo không chứa API key hoặc cấu hình đăng nhập. Nguồn bên ngoài và quyền sử dụng được ghi trong hồ sơ khi biết; việc đóng gói không cấp lại quyền cho tài liệu hoặc tài sản tham chiếu. Không có lịch sao lưu, render hoặc đăng bài tự động được cài trong bản này.
