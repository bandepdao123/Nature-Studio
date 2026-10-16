# Phát hành độc lập

## Bổ sung cấu trúc sáng tạo vào v1.0 — 2026-10-16

[Hướng dẫn chung](../00-Standards/creativity.md) liên kết với hướng dẫn riêng Underwater, được chỉ định từ README/START-HERE/AGENTS và skill. VERSION giữ 1.0 theo yêu cầu; [manifest bổ sung](manifests/nature-studio-v1.0-creativity-2026-10-16.json) cùng commit phân biệt với gói v1.0 trước. Các manifest/gói cũ giữ nguyên.

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

## Sáng tạo mở ngày 2026-10-16

Skill chayvideo v1.3 và quy chuẩn Underwater v1.4 bổ sung [creative-direction](../03-Projects/underwater/creative-direction.md). [Manifest](manifests/creative-direction-2026-10-16.json) ghi nguồn, kiểm cấu trúc và giới hạn; snapshot trước thay đổi được giữ trong snapshots/before-creative-direction-2026-10-16/. Hai ca EV-UF-006/007 mới ở trạng thái not run; chưa chứng minh chất lượng sáng tạo qua thử nghiệm.

## Nature Studio v1.0 — 2026-10-16

Phiên bản toàn hệ thống đầu tiên: [VERSION](../VERSION), [CHANGELOG](../CHANGELOG.md), [UPDATE](../UPDATE.md). [Manifest v1.0](manifests/nature-studio-v1.0-2026-10-16.json) ghi nội dung thực của workspace và phạm vi kiểm. Script đóng gói tạo ZIP có phiên bản cùng commit nguồn/trạng thái local; Git tag/GitHub Release là bước riêng, không tự có từ VERSION.

## Giữ URL nguồn ổn định — 2026-10-16

Repository hiện hành: [Nature-Studio](https://github.com/bandepdao123/Nature-Studio). Quyết định giữ tên repo, quản lý phiên bản trong nội dung thay chính sách đổi tên thử; xem [manifest khôi phục](manifests/stable-repository-name-2026-10-16.json). [Manifest đổi tên thử](manifests/repository-version-name-2026-10-16.json) giữ như lịch sử, không áp dụng làm quy tắc hiện hành.

## Nature Studio v1.1 — 2026-10-16

Thêm /dongvideo, bộ nhớ Project/shared, quyền kích hoạt có gate và validator. [Hướng dẫn migration](../UPDATE.md#nâng-từ-v10-lên-v11). [Manifest v1.1](manifests/nature-studio-v1.1-2026-10-16.json) ghi nguồn/hash và [kết quả kiểm](../06-Evaluation/results/v1.1-implementation-2026-10-16.md), không sửa snapshot/manifest cũ. Dữ liệu production đang thay đổi ở local được giữ riêng, không tự đưa vào commit framework.

## Nature Studio v1.2 — 2026-10-16

Mã video mới XXX-yyyyy từ 00001, prefix local từng Project. [Quy tắc](../00-Standards/video-identifiers.md), [migration](../UPDATE.md), [kết quả kiểm](../06-Evaluation/results/v1.2-identifiers-2026-10-16.md) và [manifest](manifests/nature-studio-v1.2-2026-10-16.json). Giữ mã legacy và production đang làm. Registry không vào Git/ZIP mẫu; backup cá nhân phải kèm registry riêng.
