# Phát hành độc lập

## Bổ sung skill workspace ngày 2026-10-16

Skill `/chayvideo` v1.0 và hợp đồng Under Fishing v1.1 được ghi tại [manifest](manifests/chayvideo-1.0-2026-10-16.json). Đây là phát hành tích hợp trong workspace, cần các nguồn hiện hành mà skill dẫn tới; không phải bản hướng dẫn độc lập mới thay thế baseline v1.9. Kiểm đã chạy và giới hạn kiểm được ghi trong manifest. Baseline nhập ban đầu giữ nguyên.

- Bản hướng dẫn Under Fishing v1.9 được nhập nguyên trạng theo yêu cầu đã chốt; loại imported-baseline, không tuyên bố là bản được tự động tổng hợp từ các module mới.
- Lần phát hành tiếp theo: chỉnh nguồn hiện hành → kiểm mâu thuẫn → tổng hợp gói tự đủ → kiểm ca liên quan → tạo manifest có file/version/hash nguồn và giới hạn kiểm.
- Không ghi đè release cũ. Không có công cụ build tự động được cài trong lần khởi tạo; manifest ghi đúng việc đã thực hiện.
- Dùng bản độc lập khi AI không truy cập kho. Trong kho, nguồn hiện hành là các file kênh/standards/knowledge, không tự sửa release để tạo một nguồn song song.

Skill `/chayvideo` v1.1 và hợp đồng Under Fishing v1.2: [manifest cập nhật](manifests/chayvideo-1.1-2026-10-16.json). Thay ngôn ngữ hai prompt/caption sang tiếng Anh và nhận diện dự án qua đặc trưng; giữ một đoạn mỗi prompt và rà trùng. Bản v1.0 là lịch sử.

## Chuyển cấu trúc Project ngày 2026-10-16

Tên hiện hành **Underwater**, nguồn tại [PROJECT.md](../03-Projects/underwater/PROJECT.md), skill chayvideo v1.2. Chi tiết đổi đường dẫn và kiểm toàn vẹn: [manifest migration](manifests/project-migration-2026-10-16.json). [Snapshot trước migration](snapshots/before-project-migration-2026-10-16/START-HERE.md) giữ nguyên nguồn cũ để truy vết. Bản phát hành cũ có thể chứa tên và đường dẫn Channel; đó là lịch sử, không phải cấu trúc hiện hành.

## Đóng gói GitHub ngày 2026-10-16

Thêm README, quy tắc Git, script đóng gói và [manifest](manifests/github-package-2026-10-16.json). Gói ZIP sinh trong packages/ (không commit) chứa cả skill ẩn và media. Trạng thái upload phải kiểm riêng; đóng gói/commit local chưa đồng nghĩa đã có repository trên GitHub.
