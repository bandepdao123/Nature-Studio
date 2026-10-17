# Underwater

ID: under-fishing-us
Slug: underwater
Version: 2.2 | Updated: 2026-10-17 | UF-D021 — camera cầm tay nhẹ
Aliases: Under Fish US; Under Fishing US; Under Fishing
Routing: Video/prompt tương tác cá–mồi dưới nước, khán giả câu cá Mỹ; săn mồi tự nhiên hoặc bait/lure/rig/jig; mọi loài cá được câu phù hợp tại Mỹ, không giới hạn Redfish/red drum/Sciaenops ocellatus, Muskie/muskellunge/Esox masquinongy, Walleye/Sander vitreus. Camera chìm cầm tay chuyển động nhẹ tự nhiên, dọc 10s và key sau 5s là dấu hiệu kết hợp. Một từ cá/Mỹ/Omni hoặc nhắc benchmark Underfishing riêng không đủ phân biệt dự án.
Model: omni-flash

UF-D020 — 2026-10-17: /clonevideo dùng [chuẩn chuyển thể](../../00-Standards/reference-video-adaptation.md) và lõi prompt chung. Reference giữ cơ chế mẫu có chủ đích, ánh xạ đúng loài/bối cảnh mới; ngưỡng độ mới dành cho concept độc lập không ép thay câu chuyện của bản chuyển thể. Quy chuẩn kỹ thuật/QA/âm/caption hiện hành vẫn áp dụng, khác biệt camera/nhịp so với mẫu phải ghi rõ.

UF-D021 — 2026-10-17: người dùng thay mặc định camera cố định bằng camera chuyển động nhẹ, tự nhiên như người cầm điện thoại quay. Áp dụng [camera cầm tay](format.md#camera-cầm-tay-tự-nhiên--uf-d021) cho bộ mới và revision được giao; tham chiếu học quan hệ máy–chủ thể, không đổi thành cá tự quay. Không sửa media/attempt lịch sử hoặc tự render.

## Nguồn hiện hành

- [Format](format.md), [hợp đồng đầu ra](output-contract.md), [khán giả/caption](audience-and-caption.md).
- Tạo concept mới phải đọc [Sáng tạo mở](creative-direction.md), [Story Development](story-development.md) cùng hai hướng dẫn chung tương ứng ở 00-Standards. Revision giữ ý định.
- [context-map.json](context-map.json) chọn nguồn theo nhiệm vụ; workflow skill quy định cách đọc và fallback, không coi packet là nguồn quyền mới. [decisions.md](decisions.md) giữ lịch sử; đọc khi truy nguyên/mâu thuẫn, không nạp mọi quyết định mỗi lượt. Baseline v1.9 chỉnh từ v1.7, không dùng v1.8; bản nhập giữ nguyên ở 07-Releases/standalone-guides.
- Knowledge: môi trường/quang học, đúng loài/tương tác và dụng cụ khi có câu cá. Thiếu loài trong kho thì tự nghiên cứu hồ sơ đúng loài, không thay tên trong hồ sơ Muskie. Research 20 Reel được khuyến nghị để hiểu/phát triển chứ không giới hạn sáng tạo.

## Chọn loài

Đã có loài/quyền chọn thì không hỏi lại. Thiếu thì hỏi một câu: **Redfish / Muskie / Walleye / Loài cá được câu bất kỳ ở Mỹ**, cho nhập loài khác. Dùng lựa chọn click nếu công cụ hỗ trợ (có thể gộp trong giới hạn số lựa chọn của công cụ), nếu không thì lựa chọn chữ; không giả nút Markdown. Chờ đáp án thật, lựa chọn sẵn không là xác nhận. “Bất kỳ” cho phép tự nghiên cứu/chọn loài và vùng phù hợp. Không hỏi chọn cá khi chỉ sửa skill.

## Runtime và bộ nhớ

Production: `04-Productions/underwater/`; idea-ledger.md local tại thư mục Project. Thiếu ledger không có nghĩa không có lịch sử. Mã mới qua scripts/video_ids.py reserve underwater theo video-identifiers.md; prefix riêng local, không ghi cứng. Giữ UF legacy khi revision.

Theo [truy xuất chọn lọc](../../00-Standards/memory-retrieval.md), query Memory Project/shared theo nhiệm vụ/hint, mở active gốc phù hợp; xét unknown/legacy và các trang còn lại, không nạp toàn bộ INDEX theo memory-policy. Ghi ID/version/đường dẫn/cách dùng vào INPUTS; candidates chỉ thử riêng, không tự active. /dongvideo đóng phiên theo skill riêng; không tự đóng từ /chayvideo.

Tạo ảnh thật qua /taoanh theo [first-frame-qa.md](first-frame-qa.md) và gate chung; tối đa 5 call/cycle, quota/handoff/hash local được bảo toàn. Không tự sinh media từ việc viết prompt. Danh tính model ảnh không chặn QA, không giả chọn Sunburst. Production/ledger/registry/media riêng không publish; lesson đi theo publication policy.
