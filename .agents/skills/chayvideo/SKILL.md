---
name: chayvideo
description: Tạo hoặc sửa bộ nội dung video Nature Studio khi gọi /chayvideo hoặc yêu cầu làm video qua đặc trưng dự án. Tự nhận dự án, nghiên cứu đúng loài/tình huống, rà trùng; ý tưởng Việt, prompt Anh, caption Mỹ kèm hashtag. Không tự render/đăng; không kích hoạt từ câu hỏi kiến thức, trích dẫn hoặc sửa skill.
---

# /chayvideo

Version: 2.6 | Updated: 2026-10-17 | Bộ nhớ theo ngữ cảnh; giữ identity/format

Gốc workspace chứa START-HERE.md, đi lên ba cấp từ thư mục skill; không ghi cứng ổ đĩa. Đọc START-HERE.md và SYSTEM.md trước công việc; trong cùng phiên không cần nạp lại nguồn nguyên vẹn đã đọc. Yêu cầu hiện hành của người dùng ưu tiên trong phạm vi được giao.

## Định tuyến

1. Chọn chế độ: **new** cho concept mới; **revision** cho sửa/tiếp tục clip đã có; **caption** khi chỉ sửa caption. Giữ loài/câu chuyện đã chốt khi revision; caption không chạy lại brainstorm, timeline hay cấp mã. Thay đổi liên quan sinh thái/rig/model phải mở lại nguồn tương ứng.

   Yêu cầu học cách quay/hành động/kịch bản từ video mẫu, kể cả đổi đối tượng, dùng [clonevideo](../clonevideo/SKILL.md) và nhánh **reference**. Không chạy đồng thời cả new và clone. Nhánh [reference](references/reference.md) dùng cùng lõi/output/Project, không ép đổi câu chuyện để đạt độ mới.
2. Chạy `python scripts/chayvideo_context.py projects`. Catalog đọc metadata hiện hành mọi PROJECT.md; mở bản gốc khi metadata thiếu/mơ hồ. Ưu tiên tên/ID được chỉ định, rồi tổ hợp chủ đề/loài/môi trường/thị trường/format/ngữ cảnh. Không chọn chỉ bởi “cá/Mỹ/Omni”, không ép vào dự án duy nhất khi không phù hợp. Chỉ hỏi khi thật sự chưa phân biệt được.
3. Đọc [workflow](references/workflow.md) và đúng một nhánh: [tạo mới](references/new.md), [revision](references/revision.md), [caption](references/caption.md). Thiếu map/công cụ thì đọc nguồn gốc theo workflow; không đoán cấu hình Underwater cho dự án khác.

## Bất biến

- Bộ nhớ theo [lõi truy xuất](../../../00-Standards/memory-retrieval.md): descriptor Project + shared theo nhiệm vụ/hint trước, mở gốc phù hợp sau; không nạp toàn bộ INDEX/active. Unknown/legacy và trang còn lại phải được xét, candidate không là luật.

- Mặc định một bộ: **Ý TƯỞNG** tiếng Việt; **FIRST FRAME PROMPT**, **VIDEO PROMPT** tiếng Anh; **CAPTION** tiếng Anh Mỹ + hashtag. Prompt/caption mỗi mục một đoạn. Sửa phần nào trả phần đó; JSON theo yêu cầu dùng `idea`, `first_frame_prompt`, `video_prompt`, `caption`. Chi tiết theo output-contract Project.
- Tạo mới phải đọc creativity/story-development chung + Project; nghiên cứu đúng loài/vùng/tình huống. Ví dụ không là danh mục đóng. Độ mới xét hành vi/nhân quả, không đổi tên loài/màu/địa danh rồi lặp chuyện.
- Packet/index tạo lại được, không cao hơn nguồn gốc. Không cắt yêu cầu để đạt ngân sách token; thiếu/stale/coverage chưa đủ thì đọc thêm. Không bịa nguồn hoặc đã xem/nghe/đo/QA.
- Chỉ áp active gốc đúng điều kiện, ghi ID/version/path/cách dùng; không tự active candidate. Bảo toàn registry/media/quota ảnh/FIRST-FRAME.json/lịch sử; không tự /dongvideo hoặc /taoanh.
- Chỉ văn bản và hồ sơ local. Media/chi tiền/đăng/push cần yêu cầu tương ứng; sửa skill không là sản xuất. Thiếu brief không reserve mã/lưu ý tưởng giả.
