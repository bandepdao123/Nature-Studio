# Lõi viết prompt và lưu hồ sơ video — v1.2

Updated: 2026-10-17 | Dùng chung chayvideo/clonevideo; nguồn Project và helper là một nơi duy nhất.

v1.2: helper kiểm đúng phạm vi Project và thống nhất identity trước lưu; giữ cơ chế kế thừa/ảnh của v1.1, không đổi format hoặc quyền sinh media.

## Context đúng nhiệm vụ

`python scripts/chayvideo_context.py packet <slug> --mode new|revision|caption|reference --species <tên> --interaction natural|angling|unspecified --out .nature-studio/context/<tên>.json`

Thay placeholder trong lệnh bằng dữ liệu thật. `--species` lặp lại cho nhiều loài; dùng tên profile nếu có, loài khác vẫn hợp lệ và được báo cần nghiên cứu. Interaction chưa rõ giữ unspecified để không vô tình bỏ gate dụng cụ. Đọc nội dung packet một lần; ghi manifest đường dẫn/hash vào INPUTS. Không cần đọc lại từng file có toàn văn nguyên vẹn trong packet. Trước tái dùng packet ở lượt khác hoặc trước lưu: `python scripts/chayvideo_context.py verify <packet.json>`; nguồn thay đổi phải dựng/đọc lại. Không coi một packet cũ là trí nhớ vĩnh viễn. Catalog cũng phải tra lại khi định tuyến mới.

Chỉ truyền species khi có liên quan; Project quyết định đầu vào bắt buộc. Profile Underwater giữ gate chọn loài/quyền chọn; packet chung không ép Project cảnh quan chọn loài chỉ vì có hồ sơ loài tùy chọn. Pending trống không chứng nhận brief đầy đủ. Output helper giữ gate tag/AI/timing riêng cho Underwater; Project khác chỉ được kiểm cú pháp chung, AI vẫn phải đối chiếu contract thật (không tự coi số tag hoặc disclosure được phép cho mọi Project). Không thêm cấu hình máy mới hoặc thay hợp đồng bốn mục.

Map chỉ chọn tài liệu; AI vẫn đọc/áp đúng phạm vi, tra link nội bộ cần thiết. Tự bổ sung nguồn theo concept; map không biết mọi nhu cầu sáng tạo. Packet chứa nguyên văn nguồn, không tóm tắt bằng LLM/cắt theo token. Các active được tìm từ file thật cả Project/shared; đọc status/điều kiện gốc trước áp, chỉ ghi lesson thực sự dùng. Không lấy candidate trong INDEX làm luật.

Nếu công cụ đọc báo truncated, đọc tiếp theo từng source/phần cho đến hết; không coi file bị cắt là đã đọc đủ. Không cần đưa toàn bộ JSON/hash inventory vào context suy luận: manifest dùng để đối chiếu/lưu, nội dung nguồn mới là phần phải đọc.

Thiếu Python/map, lỗi hash hoặc nguồn: đọc PROJECT, format, output-contract, audience và các nguồn được Project chỉ định theo nhiệm vụ; tìm file thật bằng rg. Khi tạo mới vẫn đọc creativity/story-development, Knowledge/Models, memory policy và active liên quan. Decisions/baseline/benchmark chỉ mở khi cần truy nguyên, sửa phong cách, làm rõ mâu thuẫn hoặc kiểm ràng buộc thiếu; chúng không mặc định nạp mỗi lượt.

## Lưu và kiểm

### Fingerprint lịch sử

Sau khi đọc các nguồn thực, AI viết JSON gồm chuỗi `opening`, `interaction`, `objects`, `terrain_role`, `trigger`, `key_action`, `consequence` và object `source_hashes` đúng từ cache local `.nature-studio/history/<slug>.json` (bỏ chính HISTORY-FINGERPRINT.json); `history --full` cũng trả hash nhưng không cần nạp cả inventory mỗi lượt. Ghi cơ chế đủ cụ thể để so xuyên loài, không chỉ nhãn/tóm tắt tiêu đề. Chạy `python scripts/chayvideo_context.py fingerprint <slug> <ID> <json>`; công cụ từ chối nếu nguồn đã đổi/thiếu, nhưng không chứng minh AI đã đọc hoặc hiểu. Với hồ sơ mâu thuẫn/nhiều revision, phản ánh trạng thái và các cơ chế đã giao, không xóa nháp cũ khỏi đối chiếu. Bất kỳ thay đổi văn bản/attempt sau đó làm capsule hết hạn. Không backfill toàn kho ngoài nhu cầu nhiệm vụ; khi không có capsule thì đọc nguồn gốc như thường.

Đủ bộ nội dung thật mới reserve video mới qua `python scripts/video_ids.py reserve <slug>`; sửa clip dùng ID cũ. Đọc production.md và video-identifiers.md trước lần cấp mới trong phiên. Không cấp ID từ tra cứu/caption-only.

Lưu một JSON local với các trường đầu ra được giao; cho Underwater fullset thêm metadata nội bộ `checks.key_onset` là số giây dự định thật. Metadata không xuất thêm vào bốn mục cho người dùng. Chạy `python scripts/chayvideo_output.py check <json> --project <slug> --mode <mode>`. Script chỉ kiểm cú pháp/số tag/timecode, không xác nhận tiếng Anh, sinh học, key thật hay QA media; AI vẫn tự kiểm nội dung theo Project. Nếu kiểm lỗi thì sửa trước giao. Không lách validator bằng timecode/metadata khác lời prompt.

Có thể dùng `save <json> --project <slug> --production <ID> --mode <mode>` thay `check` để tạo attempt mới. Trong JSON thêm `files` gồm chuỗi `INPUTS.md`, `settings.md`, `review.md`, tùy chọn `revision.md`; ghi trung thực nguồn/hash/lesson/ảnh input và phần giữ nguyên, model/settings chưa thực thi/unknown, review prompt-only. Script chỉ tạo attempt, không tự viết nghiên cứu hoặc kết luận. Thiếu công cụ thì lưu theo template bằng file tools, không ghi đè attempt.

Sau lưu, hoàn tất brief/research/concept/SUMMARY/feedback/performance thực và ledger theo production.md; không để save attempt thay phần hồ sơ này. Concept ghi story card/so sánh/giới hạn; cập nhật ledger ngay drafted, không chờ render. Caption-only ghi revision/nguồn attempt trước, giữ prompt/chuyện cũ bằng tham chiếu, không chế bốn output mới hoặc đánh dấu selected/approved/published. Nếu có FIRST-FRAME.json, kiểm file/hash/review và ảnh thật khi cần tiếp nối; không sửa quota/handoff từ việc soạn prompt.

Rà cú pháp đạt khác với nội dung đạt, ảnh/video đạt hoặc khán giả thích. Báo giới hạn quan trọng, không tự render để kiểm. Không in suy luận nội bộ hay báo cáo dài vào bốn mục.

### Tiếp tục đúng bộ đầu vào

Khi tiếp tục/revision/caption, xác định attempt theo yêu cầu, SUMMARY và nguồn thực; không lấy Axx lớn nhất. `python scripts/chayvideo_output.py resolve A03 --project <slug> --production <ID>` trả bốn trường đã ghép và nguồn từng trường; nếu layout dùng attempts/ thì truyền `attempts/A03`. Lệnh chỉ đọc, không chọn/duyệt bản hoặc cập nhật SUMMARY. Chỉ resolve khi cần tiếp nối, không đọc toàn chuỗi thủ công nếu kết quả đủ và không mâu thuẫn brief/chat hiện hành.

JSON gửi `save` ở mode revision/caption bắt buộc có `base_attempt` (đường dẫn attempt tương đối production) và `base_sha256` lấy từ `attempt_sha256` của resolve bản gốc vừa kiểm. Chỉ ghi trường thật sự sửa. Helper giữ quan hệ/hash trong OUTPUT.json; từ chối nguồn thiếu/đổi, vòng tham chiếu hoặc SAVE-INCOMPLETE.txt. Nhánh khác không tự nhập vào bộ đang dùng. Resolve không xác minh ngữ nghĩa; AI kiểm tính liên đới giữa phần giữ và phần sửa. `check` vẫn chỉ kiểm cú pháp; `save` mới kiểm nguồn kế thừa.

`frame_state` là object nội bộ gồm bốn chuỗi không rỗng: `subjects` (chủ thể, số lượng, nhận dạng, vật/rig), `environment` (sinh cảnh/ánh sáng/chất liệu), `composition` (camera, vị trí/tỷ lệ, đường diễn biến cần chừa), `initial_state` (trạng thái/quan hệ tại t=0). Ghi đủ chi tiết khóa theo concept. Nên ghi từ fullset mới và bắt buộc đủ trước khi tạo handoff ảnh schema 2; không xuất thành mục thứ năm. Đây là khai báo AI cần đối chiếu, không phải máy chứng minh t=0 đúng.

Revision đổi idea/video/first-frame prompt phải đánh giá lại frame_state: nếu t=0 không đổi, truyền nguyên object đã đối chiếu; nếu đổi, ghi trạng thái mới. Không khai báo thì resolver đánh dấu unverified, không âm thầm kế thừa xác nhận cũ. Caption-only chỉ sửa caption, tự kế thừa frame_state và không làm mất hiệu lực ảnh. Thay câu chữ concept không tự bắt QA ảnh nếu opening đã được đối chiếu giữ nguyên. First-frame prompt đổi thì cần đối chiếu ảnh lại, không tự sinh lại.

Hồ sơ cũ fullset có OUTPUT.json vẫn resolve được; thiếu frame_state là unverified. Attempt chỉ có Markdown hoặc partial không rõ base phải mở nguồn để xác định, không suy theo số/thời gian. Nếu cần tiếp nối bằng helper, lưu một fullset snapshot mới sau khi đọc/đối chiếu bốn trường thật (`save --mode new` với **ID hiện có**, ghi nguồn legacy vào INPUTS); không cấp ID mới, không sửa attempt cũ và không giả đã tạo concept/media mới. Snapshot là cầu nối rõ ràng, không backfill toàn kho. Không có Python thì dùng tham chiếu từng trường trong INPUTS, ghi chưa được helper kiểm, không giả resolve đạt.

Nếu dùng ảnh đã QA, theo [kiểm liên kết first frame](first-frame.md#kiểm-liên-kết-ảnh-trước-tái-dùng); không chạy kiểm ảnh cho caption-only khi không có việc dùng ảnh.

## Khi tiếp nhận media thực — v1.7

Theo [kiểm media và finishing](media-review-and-finishing.md) khi nhận reference hoặc render; chỉ viết prompt không cần chạy đo. Tách khả năng trích xuất, ASR và hiểu hình/âm thực; giữ trạng thái text/render/QA/approval độc lập trong SUMMARY. Bộ đầu ra vẫn bốn mục.
