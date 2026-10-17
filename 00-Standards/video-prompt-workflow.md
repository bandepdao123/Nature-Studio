# Lõi viết prompt và lưu hồ sơ video — v1.4

Updated: 2026-10-17 | Một lõi cho chayvideo/clonevideo; nguồn nguyên văn theo giai đoạn.

## Context đúng nhiệm vụ

Chọn Project từ metadata hiện hành. Nguồn do context-map và routing Project chọn; giữ toàn văn, không tóm tắt/cắt theo quota. Lệnh dùng dữ liệu thật, đường dẫn local tương đối:

```text
python -X utf8 scripts/chayvideo_context.py packet <slug> --mode new|revision|caption|reference --stage all --species <tên> --interaction natural|angling|unspecified --out .nature-studio/context/task.json
python -X utf8 scripts/chayvideo_context.py view .nature-studio/context/task.json --context-id task-epoch-1 --receipt .nature-studio/context/read.json
```

Thay placeholder thật; `--species` lặp cho nhiều loài. Loài chưa có profile phải nghiên cứu đúng đối tượng; chưa rõ interaction giữ unspecified. Pending trống không chứng nhận brief đầy đủ. Output gate loài/tag/key riêng Project không áp sang mọi Project.

New/reference có thể chia `orient → concept → write → review → save`: orient làm rõ brief; concept đọc creativity/story, format và Knowledge trước chọn chuyện; write đọc contract/model/giọng và nguồn liên quan; review tự kiểm; save đọc production/IDs trước cấp mã/lưu. Giữ nguồn theo chuẩn reference, không ép mới so mẫu. Revision dùng write/review/save, caption dùng write; `--stage all` đọc đầy đủ một lần khi chưa chắc. Source mới chưa phân stage vẫn được nạp. Nguồn đang ảnh hưởng quyết định phải mở ngay, không chờ stage sau.

Thêm `--effect camera|rig|species|environment|story|audio-level|audio-source` cho ảnh hưởng thật; effects chỉ thêm phụ thuộc. Khi có nhiệm vụ review render/âm, dùng effect video-review/audio-review hoặc lặp `--task` đúng nhiệm vụ. Không giả review chỉ từ prompt.

View verify trước đọc và chia batch nguyên nguồn, mục tiêu 18.000 ký tự body; không cần đọc JSON/hash. Còn NEXT SOURCES.count thì gọi lại cùng packet với receipt trước làm seen, ghi receipt mới đến khi hết. `--max-chars` chỉnh theo budget tool, không cắt nguồn. Truncated thì không dùng receipt đó; đọc đủ từng nguồn bằng `--source`/file tools hoặc fallback đọc gốc, ghi chưa được helper kiểm. Chỉ thêm `--seen <receipt> --retained --context-id <cùng-epoch>` khi mọi nguồn của receipt đã đọc đủ và nguyên văn còn trong context. Receipt không chứng minh AI đã hiểu. Sau compaction/đổi chat/không chắc: bỏ seen/retained, đổi epoch và đọc lại. Packet stale phải dựng lại; không tự coi cache là trí nhớ.

Trước lưu/giao, `python -X utf8 scripts/chayvideo_context.py coverage <các-packet-đã-đọc> --receipt <receipt-còn-giữ> --context-id <epoch> --retained`; lặp receipt khi cần. Complete=false phải đọc nguồn thiếu/dựng lại nguồn stale. Coverage chỉ kiểm khai báo đủ nguồn, không thay QA ngữ nghĩa/history/media. Lưu manifest paths/version/hash vào INPUTS, không in vào bốn mục. [Cấu hình/tuỳ chọn chi tiết](context-routing.md) đọc khi bảo trì hoặc chưa rõ lệnh, không nạp mỗi lượt.

Memory theo [truy xuất chọn lọc](memory-retrieval.md): descriptor Project/shared theo task, xét hết trang/unknown/legacy và mở bài gốc phù hợp. Candidate không là luật. Nguồn tham chiếu/hồ sơ thực vẫn cần đọc riêng; quyết định/baseline/benchmark chỉ mở khi cần, không mặc định nạp lại. Thiếu Python/map/nguồn hoặc cấu hình sai: đọc Project/format/contract/giọng và Knowledge/model/creativity/story cần cho mode, bổ sung nguồn gốc; không đoán cấu hình hoặc nhận helper đã kiểm.

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

## Bộ nhớ schema2 — v1.8

Task/hint từ nhiệm vụ thật, cùng lõi memory_retrieval.py cho new/revision/caption/reference và skill ảnh/đóng phiên. Đọc memory-retrieval.md lần đầu dùng; packet chưa chọn lesson không chứng minh đã áp bộ nhớ. Lưu selection/query local, mở nguyên văn bài có thể dùng; tiếp tục next_cursor hoặc --broad khi cần. Verify xét cả inventory namespace để phát hiện bài mới/đổi status ngoài selection, không chỉ hash bài đã dùng. Khối sources và memory.errors/pending cần kiểm trước giao.
