# Revision và first-frame binding — triển khai mục 1–2

Date: 2026-10-17 | chayvideo v2.2 | taoanh v1.1 | VERSION 1.5, chưa phát hành

## Phạm vi

- Mở rộng scripts/chayvideo_output.py: resolve bộ nội dung từ một attempt rõ ràng và nguồn từng trường; revision/caption save yêu cầu base_attempt/base_sha256. Nguồn đổi, thiếu, không đầy đủ hoặc lưu dở không tự tái dùng. Không tự chọn mới nhất, selected hoặc approved.
- Frame_state khai báo trạng thái mở đầu. Revision chuyện/prompt thiếu đối chiếu thì unverified; caption-only kế thừa và không thay trạng thái ảnh. Cả chayvideo và clonevideo dùng lõi chung.
- Check-frame đối chiếu ảnh/review/hash, source attempt, snapshot t=0 và nguồn tiêu chí QA. Trả matched/needs_review/unverified/invalid; không chấm hình từ metadata, tự sinh ảnh hoặc đổi QA lịch sử. Phân biệt attempt sinh ảnh với source_attempt nội dung.
- Handoff schema 2 giữ metadata cũ và bổ sung binding. Hồ sơ legacy giữ nguyên; thiếu thông tin mở nguồn kiểm tay hoặc lưu snapshot đầy đủ đã đối chiếu vào attempt mới cùng ID. Không backfill hoặc bịa trường để đủ schema.
- Giữ cấu trúc thư mục, quota, registry, ID, memory policy và quyền người dùng. Không triển khai mục 3–4. Không tăng VERSION khi chưa phát hành.

## Kiểm thử

`python -m unittest discover -s scripts/tests`: **118/118 đạt**, gồm 99 ca trước và 19 ca mới. Ca mới dùng production tạm, không gọi model/cấp ID thật:

- Chuỗi sửa video → caption, nhánh không được chọn và layout attempts/; xác định đúng nguồn từng trường.
- Thiếu base/hash sai/ancestor đổi/nguồn thiếu/path escape/attempt lưu dở; kiểm identity modern và không tự cấp registry.
- Legacy fullset đọc được nhưng opening chưa xác minh; partial không có base bị từ chối.
- Caption không lén đổi chuyện/frame_state; caption và chuyển động mới có opening đã đối chiếu giữ binding ảnh.
- Revision thiếu đánh giá t=0 thành unverified; chủ thể/first-frame prompt hoặc tiêu chí đổi cần review.
- Ảnh/review/hash snapshot/source sai, ảnh attempt thiếu, binding tiêu chí thiếu và qa_incomplete không thể matched.
- CLI resolve/check-frame và exit codes; snapshot chi tiết chỉ in khi resolve có --frame-inputs; các lệnh không sửa file hoặc quota.

Hai skill chayvideo/taoanh qua quick_validate (Python UTF-8; PyYAML phục vụ kiểm đặt ngoài repo). Memory validator đạt, 1 lesson không đổi trạng thái. Các liên kết file mới/sửa hợp lệ. Git diff whitespace đạt khi công nhận CRLF bằng `git -c core.whitespace=cr-at-eol diff --check`; không chuẩn hóa hàng loạt file có trước.

## Bảo toàn và giới hạn

Snapshot nguồn chỉnh sửa, Git status/diff và hash runtime được lưu ngoài repo trước ghi. Đối chiếu **367 file runtime có trước: 0 thay đổi hoặc mất** (production, registry/cache local, Memory và ledger). Không sửa dữ liệu legacy thật, không tạo media, không commit/push.

Kiểm này xác nhận cơ chế phần mềm trên fixture. Hash/snapshot và qa_pass khai báo không chứng minh AI hiểu đúng hoặc ảnh thực đạt; frame_state vẫn cần đối chiếu brief/chat/ảnh. Không chạy QA ảnh thật, phân tích video, A/B model hoặc đo token/thời gian/chi phí. Không từ kết quả suy ra giảm token tổng thể hoặc chất lượng sáng tạo tăng.
