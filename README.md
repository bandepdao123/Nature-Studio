# Nature Studio v1.2

Workspace sản xuất nội dung thiên nhiên bằng AI, tổ chức theo **Project**. Tài liệu và lịch sử được lưu bằng file để tiếp tục công việc qua nhiều phiên làm việc.

Đọc [START-HERE.md](START-HERE.md) và [SYSTEM.md](SYSTEM.md) trước khi bắt đầu. AI đọc [AGENTS.md](AGENTS.md) để nhận quy tắc workspace.

## Dành cho AI nhận link GitHub

Đọc [VERSION](VERSION) và [CHANGELOG.md](CHANGELOG.md) để biết phiên bản toàn hệ thống, sau đó theo START-HERE/SYSTEM. Khi kiểm tra hoặc cập nhật từ GitHub, thực hiện [UPDATE.md](UPDATE.md): xác định commit đích, so với bản local và giữ chỉnh sửa riêng trước khi ghi. Chỉ có link repo chưa đủ để biết máy người dùng đã thay đổi gì; cần quyền đọc local hoặc gói workspace/manifest của họ.

Phiên bản hiện hành là **Nature Studio v1.2**. Skill/project có số phiên bản riêng. VERSION không tự tạo Git tag/GitHub Release; main có thể chứa thay đổi sau một release, nên luôn ghi kèm commit và trạng thái local. Repository nguồn: [bandepdao123/Nature-Studio](https://github.com/bandepdao123/Nature-Studio).

## Dự án hiện tại

[Underwater](03-Projects/underwater/PROJECT.md): Reel camera dưới nước hướng người câu cá Mỹ. Video mục tiêu 10s, 9:16, một shot; quy chuẩn cụ thể nằm trong hồ sơ dự án. Tên cũ Under Fish US / Under Fishing US chỉ là alias; ID nội bộ và prefix UF được giữ để truy vết.

Đã có hồ sơ [UF-0001](04-Productions/underwater/UF-0001/SUMMARY.md). Đọc SUMMARY và review thực để biết đúng lịch sử/mức kiểm; bản trên GitHub và production đang làm ở local có thể khác nhau. Nâng framework không đồng nghĩa đã QA hoặc duyệt video.

## Hướng dẫn sáng tạo cho AI

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
| 05-Memory | Bộ nhớ riêng Project và shared, mỗi nơi có candidate / active / retired |
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

## Tên repository cố định, phiên bản nằm trong nội dung

Repository luôn là [Nature-Studio](https://github.com/bandepdao123/Nature-Studio); không đổi tên khi nâng phiên bản. Tên hiển thị trong README, VERSION, CHANGELOG và gói ZIP thể hiện bản đang dùng, ví dụ Nature Studio v1.1. Khi chốt bản mới, cập nhật các nội dung đó; có thể tạo tag/release v1.1 khi được yêu cầu, giữ nguyên URL repo. [REPOSITORY.json](REPOSITORY.json) ghi danh tính nguồn ổn định.

## /dongvideo và bộ nhớ hai cấp — mới trong v1.1

Gửi `/dongvideo UF-0001` để [tổng kết phiên](.agents/skills/dongvideo/SKILL.md). Skill rà attempt/phản hồi thực, xét bài học riêng Project **và** đóng góp phương pháp/kinh nghiệm cho bộ nhớ chung. Không ép mỗi phiên có lesson; chạy lại không nhân đôi dữ liệu. Báo cáo bằng tiếng Việt, không tự render, duyệt video hay push.

[Memory](05-Memory/INDEX.md) tách `projects/<slug>/` và `shared/`. /chayvideo đọc active phù hợp ở cả hai nơi, ghi lesson ID/version vào INPUTS. /dongvideo tự lưu candidate; chỉ tự active phương pháp kiểm khách quan khi đạt đủ [gate](00-Standards/memory-policy.md). Kiểm cấu trúc bằng `python scripts/validate_memory.py` không chứng minh bài học đúng hay video tốt hơn.

Nâng cấp từ v1.0 theo [UPDATE.md — migration](UPDATE.md#nâng-từ-v10-lên-v11). Giữ dữ liệu riêng, phân loại lesson theo phạm vi, không chép đè cả thư mục và không đẩy production đang làm lên public chỉ vì nâng framework. GitHub main mang phiên bản workspace, không tự có GitHub Release/tag.

## Mã video — Nature Studio v1.2

Video mới dùng **XXX-yyyyy**, ba chữ A–Z riêng từng Project local, số từ **00001**. [Quy tắc và công cụ](00-Standards/video-identifiers.md): init tạo prefix, reserve cấp mã an toàn và UUID. Không cấp mã từ câu hỏi hoặc revision. Registry `.nature-studio/` không lên Git, phải được giữ khi backup/di chuyển/cập nhật; không nằm trong gói mẫu. UF-0001 và các attempt lịch sử giữ nguyên. Xem UPDATE.md khi nâng từ v1.1.

Gói ZIP phân phối loại `.nature-studio/` để không phát tán prefix local. Muốn di chuyển workspace cá nhân đang làm, sao lưu registry riêng khi không có tác vụ cấp mã; ZIP phân phối không thay bản sao lưu danh tính Project.
