# Nature Studio — lịch sử phiên bản

Phiên bản toàn workspace được đọc từ [VERSION](VERSION). Phiên bản của từng skill/tài liệu được quản lý riêng; không đổi tất cả thành 1.0. Commit và hash dùng để phân biệt các bản có cùng số phiên bản hoặc có chỉnh sửa local.

## v1.0 — 2026-10-16

Bản đầu tiên được đặt phiên bản toàn hệ thống theo yêu cầu người dùng. Các thay đổi trước ngày này được gom vào nền v1.0, không suy ra rằng workspace từng phát hành v1.1/v1.2 từ số phiên bản module.

- Tổ chức theo Project, với dự án Underwater; giữ ID/prefix và lịch sử tên cũ.
- Có Standards, Knowledge, Models, Productions, Memory, Evaluation và Releases.
- Skill chayvideo v1.3 nhận diện dự án theo đặc trưng, rà lịch sử và kiểm độ mới ở nhân quả; ý tưởng tiếng Việt, hai prompt tiếng Anh một đoạn và caption tiếng Anh Mỹ.
- Hướng dẫn sáng tạo mở tránh dùng ví dụ làm danh sách tình huống đóng; revision giữ ý định đã chọn.
- Bổ sung UPDATE.md để AI đọc repo, xác định phiên bản đích và đối chiếu thay đổi với workspace local trước khi cập nhật.
- Script đóng gói ghi VERSION, nguồn repository, commit và trạng thái local vào PACKAGE-MANIFEST.json, cùng hash từng file.
- Giữ hồ sơ UF-0001 và các attempt hiện có đến A04. Chốt v1.0 không có nghĩa các attempt đã đạt QA hoặc được duyệt.

Giới hạn: chưa chạy đánh giá hành vi EV-UF-006/007; chưa chứng minh độ mới/chất lượng media hoặc hiệu quả nền tảng. Không cài tự động pull, render, publish hoặc sao lưu theo lịch. Việc có VERSION không tự tạo Git tag hay GitHub Release.

### Bổ sung vào v1.0 — 2026-10-16

- Đưa cấu trúc hướng dẫn sáng tạo chung vào 00-Standards/creativity.md, dẫn từ README, START-HERE, AGENTS và skill chayvideo v1.4.
- Giữ hướng dẫn cụ thể của Underwater trong creative-direction.md; không nhân bản thành một danh mục tình huống đóng. Giữ nguyên quy tắc revision và hợp đồng đầu ra.
- VERSION tiếp tục là 1.0 theo yêu cầu người dùng; commit và manifest bổ sung phân biệt nội dung với bản v1.0 trước đó. Giữ nguyên manifest/gói cũ, không coi các bản cùng VERSION là byte-identical.

## Quy tắc ghi lần cập nhật tiếp theo

Trong quá trình phát triển, ghi mục `Chưa phát hành` ở đầu lịch sử. Khi chốt bản mới, cập nhật VERSION và mục tương ứng, nêu thay đổi/di chuyển dữ liệu, điều người dùng cần làm và giới hạn đã kiểm. Không sửa mô tả bản đã đóng để che lịch sử. Chỉnh dữ liệu sản xuất có thể chỉ cần commit mới, không tự tăng phiên bản toàn hệ thống sau mỗi clip.

### Quyết định giữ URL repository — 2026-10-16

- Giữ tên repo Nature-Studio, đưa tên thử Nature-Studio-v1.0 trở lại tên ổn định; vẫn là cùng repository ID 1421542100 và giữ toàn bộ lịch sử.
- Phiên bản chỉ ghi trong README/VERSION/CHANGELOG/manifest/gói và tag/release khi được tạo. Không đổi tên repo theo mỗi phiên bản. Quyết định này thay chính sách đổi tên thử trước đó; VERSION hiện vẫn 1.0.
