# Plan 01 — triển khai local và kiểm cơ chế

Date: 2026-10-17 | Skill: chayvideo v2.0 | Workspace VERSION: 1.5 (chưa phát hành)

## Phạm vi đã làm

- Dispatcher mỏng, ba đường new/revision/caption. Revision cục bộ không bắt tạo bốn trường; caption-only không cấp ID hoặc tái phát triển chuyện.
- PROJECT/format/output-contract Underwater là nguồn hiện hành duy nhất theo phạm vi; quyết định và baseline giữ lịch sử. Gỡ hợp đồng ba mục cũ khỏi runtime. Khôi phục đầy đủ phần chuyển động của baseline v1.9 vào format: bản tách trước chỉ có đoạn bùn nhưng tham chiếu mục 4. Đây là khôi phục yêu cầu đã có, không đổi chính sách key/nhịp.
- Context-map chọn file nguyên văn theo nhiệm vụ/interaction/loài; chưa rõ interaction giữ gate dụng cụ. Loài khác được yêu cầu nghiên cứu, không thay bằng Muskie hay giới hạn ở ba loài.
- Hash nguồn, map, entry docs/skill/workflow và inventory active giúp phát hiện packet cũ. Thiếu nguồn hoặc công cụ có fallback đọc gốc, không cắt token hoặc bỏ yêu cầu.
- History quét văn bản thực, kể cả attempt/feedback, trả toàn bộ fingerprint còn khớp nguồn và danh sách cần đọc. Lexical query chỉ hỗ trợ; không có giới hạn top-k và không được coi là kiểm mới ngữ nghĩa. Ledger/chat/ví dụ và dữ liệu Project khác liên quan vẫn phải xét. Capsule phải phản ánh cả cơ chế cũ đã giao trong các revision; không phải kết luận máy rằng chuyện độc nhất.
- Helper kiểm cấu trúc đầu ra và lưu attempt mới; AI vẫn chịu trách nhiệm nghiên cứu, story card, hồ sơ, ledger và QA nội dung. Không tự tạo/render/publish, không làm clonevideo, không thay model hoặc memory policy.

## QA bảo toàn yêu cầu

| Nhóm yêu cầu | Nguồn hiện hành / phép kiểm |
|---|---|
| Chọn dự án động, aliases, không kích hoạt từ câu hỏi kiến thức | SKILL + catalog đọc PROJECT thật; thiếu metadata phải mở gốc |
| Mọi loài phù hợp tại Mỹ, thiếu loài hỏi/chờ, đã có không hỏi lại | PROJECT; test unknown/multiple species, không tự gán Muskie |
| Sáng tạo mở, story-development, nhân quả và độ mới xuyên loài | new workflow + creativity/story-development chung và Project giữ nguyên; index không thay review |
| Revision giữ ý định, chỉ sửa phần được giao | revision/caption workflow; test partial revision và caption-only |
| First frame t=0, màu nước riêng độ trong, hạt/ánh sáng/nền/góc máy thật | output-contract + habitat Knowledge giữ nguyên; không gọi QA ảnh từ prompt |
| Đúng loài/sinh vật tương tác/dụng cụ/phương pháp/vùng và lực | format + Knowledge + research; natural không tự thêm tackle, unknown interaction không bỏ gate |
| 10s9:16, một shot, 5–8 beat liên tục, key onset >5s, setup/hậu quả | format + output-contract; test timecode và metadata onset, ngữ nghĩa cần AI/media thật |
| Môi trường+hành động lớn/rõ xuyên suốt, không nhạc/voice mặc định | format, output-contract; không tuyên bố đã nghe/đo audio |
| Bốn mục/ngôn ngữ, từng prompt một đoạn, caption Mỹ + 3–5 tag cùng đoạn, không AI/#Underwater | output-contract/audience; test cấu trúc, giọng tự nhiên vẫn cần review |
| Lesson active đúng điều kiện, candidate không tự active | memory-policy giữ nguyên; test tìm active thực ngoài INDEX, không lấy candidate vào active inventory |
| ID/attempt/legacy/quota/handoff giữ nguyên, runtime local | save không reserve, không ghi đè; test đồng thời lưu attempt và giữ quota; hash trước–sau |

## Kiểm thử và giới hạn

Các test chạy trên workspace tạm, không cấp mã hoặc ghi production thật. Bộ test gồm nguồn đổi cùng độ dài, thiếu nguồn, dispatcher đổi, active mới, lịch sử mới/xóa/thiếu concept, capsule cũ/sai kiểu, query khác tên loài, ledger-only, path escape, save đồng thời, tag/timecode sai, partial revision và quota ảnh.

Kết quả cuối: **76/76 test đạt**, gồm 24 test mới Plan 01 và 52 test sẵn có. Skill quick_validate đạt, memory validator đạt (1 lesson, không đổi trạng thái), git diff --check sạch. Smoke trên kho thật: packet caption không stale, history tìm đủ ba production và báo cả ba chưa có capsule; không giả đã nén/đọc hết lịch sử. Không backfill production thật trong công việc sửa skill.

Đây là kiểm cơ chế phần mềm và đối chiếu yêu cầu; chưa phải A/B output của model, chưa chạy 6.1 Sol/API, chưa render hoặc đo thời gian/retention/view. Không từ kết quả này suy ra chất lượng sáng tạo luôn không đổi.

## Đo context

Phương pháp: tokenizer o200k_base làm proxy, không được xác nhận là tokenizer GPT-6.1 hoặc usage thực tế. Baseline là luồng đọc đầy đủ của skill cũ trên cùng kho: entry docs, skill, bảy file Project, standards, Knowledge cho Muskie angling, memory indexes và SUMMARY/concept hiện có. Không tính suy luận, web, output hoặc nội dung media. Luồng mới đo nguồn văn bản theo nhánh cộng skill/workflow và entry docs; new vẫn cộng SUMMARY/concept cho hồ sơ legacy chưa có capsule. Manifest JSON, tool overhead và nguồn bổ sung không tính vào cột source-text; vì vậy đây không là tiết kiệm hóa đơn hay thời gian đã đo. So revision/caption với baseline full-read chỉ thể hiện khác biệt đường đọc, không là thử nghiệm đối chứng cùng prompt.

Ưu tiên giữ phần đọc sâu ở concept mới. Lần đầu chưa có fingerprint không tự nhận đã có lợi ích lịch sử nén; chỉ có lợi ích đó sau khi đọc/ghi capsule hợp lệ, và luôn phải mở trường hợp gần nhất. Cùng phiên đã có nguồn nguyên vẹn không cần nạp lại nếu hash còn khớp. Mọi phần tài liệu bị tool cắt phải đọc tiếp, không tính là coverage đủ.

| Đường đọc | Source-text proxy tokens | Giảm so baseline full-read 48.660 |
|---|---:|---:|
| Tạo mới Muskie + angling, còn đọc legacy | 44.632 | 8,3% |
| Revision, chưa cộng hồ sơ clip được chọn | 34.408 | 29,3% |
| Caption-only, chưa cộng nội dung clip được chọn | 12.484 | 74,3% |

Riêng SKILL.md giảm từ 3.893 xuống 741 proxy tokens (**81,0%**); workflow/nhánh được đọc thêm khi chạy, đã tính vào bảng. Các tệp nguồn JSON packet nếu nạp nguyên manifest và escaping cũng có overhead riêng; bảng không che điều đó bằng việc gọi source-text là usage thực. Concept mới giảm ít hơn vì giữ nghiên cứu sâu và phục hồi đầy đủ mục chuyển động. Không đánh đổi chất lượng yêu cầu để đạt một tỷ lệ tiết kiệm đặt trước.

## Dữ liệu và phát hành

Đối chiếu **360 file runtime có trước công việc: 0 đổi hash, 0 mất**; không chỉnh production/media/quota/lesson/registry cũ. Chỉ tạo cache/packet/audit local mới. Backup nguồn và hash baseline nằm ngoài repo; không đưa đường dẫn máy hoặc runtime vào báo cáo công khai này. File nguồn cũ có trong backup và lịch sử Git, baseline phát hành giữ nguyên. Chưa commit/push; không gộp ba manifest local đã tồn tại vào lần cập nhật này.
