# Underwater

ID: under-fishing-us | Version: 1.3 | Status: configured | Updated: 2026-10-16
Slug: underwater
Production prefix: UF
Legacy names: Under Fish US; Under Fishing US; Under Fishing

Tên hiện hành: **Underwater**. ID nội bộ `under-fishing-us` và prefix `UF` được giữ để bảo toàn liên kết/ID cũ; thư mục hiện hành dùng slug `underwater`. Đây là cùng một dự án được đổi tên, không phải dự án mới.


## Mục tiêu

Reel dưới nước hướng khán giả Mỹ thích câu cá; footage mô phỏng camera thật, đúng loài/vùng/vật lý, câu chuyện nguyên bản. Người dùng chỉ định model video Omni Flash. Mặc định một bộ prompt, không tự sinh media khi chỉ được yêu cầu viết.

## Đọc theo thứ tự

Khi chạy `/chayvideo`, áp dụng hợp đồng riêng tại đầu output-contract.md và [skill](../../.agents/skills/chayvideo/SKILL.md): Ý TƯỞNG tiếng Việt, FIRST FRAME PROMPT và VIDEO PROMPT tiếng Anh, CAPTION tiếng Anh Mỹ kèm hashtag; mỗi prompt một đoạn, tra lịch sử trước khi sáng tạo. Phần ngôn ngữ/ba mục tiếng Anh kế thừa chỉ áp dụng ngoài chế độ này, trừ yêu cầu mới của người dùng. Thị trường mục tiêu là Mỹ; caption dùng cách nói tự nhiên của người câu cá Mỹ. Chế độ skill cũng áp dụng khi nhận diện yêu cầu tạo nội dung qua đặc trưng dự án, không cần gọi đúng tên.

1. [Format hiện hành](format.md)
2. [Khán giả và caption](audience-and-caption.md)
3. [Hợp đồng đầu ra](output-contract.md)
4. [Quyết định](decisions.md), [Lịch sử ý tưởng](idea-ledger.md)
5. Theo cảnh: Knowledge về loài, môi trường, tackle; model profile; Memory active phù hợp.

Các file này là nguồn hiện hành trong hệ thống, kế thừa đầy đủ phần liên quan từ v1.9. Các tham chiếu đánh số cũ trong đoạn trích trỏ về bản v1.9 tại ../../07-Releases/standalone-guides/; không phải tên file mới. Khi phát hiện chưa phân tách đủ, tra baseline thay vì tự bỏ ràng buộc; ghi vấn đề để sửa nguồn.

## Chọn loài

Nếu người dùng đã chọn/giao quyền thì không hỏi lại. Nếu thiếu, hỏi một câu có bốn lựa chọn: Redfish / Muskie / Walleye / Loài cá được câu bất kỳ ở Mỹ, cho nhập loài khác. Dùng lựa chọn tương tác khi có công cụ, không giả nút Markdown. Chờ câu trả lời thật; đáp án chọn sẵn không phải xác nhận. Với cá bất kỳ, tự nghiên cứu/chọn loài và vùng thích hợp rồi làm. Không hỏi chọn cá khi chỉ sửa hướng dẫn.

## Nguồn hiện hành và phiên bản

Nền người dùng chốt: v1.9 chỉnh từ v1.7, không v1.8. Bản phát hành nhập nguyên trạng chỉ dùng tham chiếu/đóng gói, không chỉnh song song. Khi sửa nội dung dự án, cập nhật file nguồn, decisions và manifest phát hành mới trong cùng công việc được giao.

2026-10-16: bổ sung chế độ /chayvideo theo yêu cầu trực tiếp; xem UF-D008–UF-D012; UF-D011 thay UF-D009 về ngôn ngữ đầu ra. Baseline v1.9 được giữ nguyên.

## Đặc trưng nhận diện cho skill

- Tên hiện hành/slug: Underwater / underwater; ID ổn định under-fishing-us. Tên cũ Under Fish US, Under Fishing US, Under Fishing chỉ là alias để nhận diện yêu cầu cũ. Underfishing là nguồn benchmark, không phải tên hiện hành của dự án; chỉ nhắc tên nguồn chưa đủ để chọn dự án.
- Chủ đề: Reel quan sát tương tác cá–mồi dưới nước cho người câu cá Mỹ; săn mồi tự nhiên, bait hoặc lure, rig/jig.
- Loài khởi đầu: Redfish/red drum/Sciaenops ocellatus; Muskie/muskellunge/Esox masquinongy; Walleye/Sander vitreus. Cũng có thể làm loài cá được câu khác ở Mỹ theo brief.
- Dấu hiệu kết hợp: camera chìm cố định, một shot dọc 10s, key sau 5s, lạch triều Texas/Louisiana/Florida hoặc hồ/sông phía bắc Mỹ. Đây là dấu hiệu định tuyến, không phải mọi yêu cầu đều phải nêu đủ.
- Chỉ suy ra dự án khi có ý định tạo bộ nội dung/video/prompt trong ngữ cảnh. “Làm bộ Walleye theo jig” khớp; “Walleye ăn gì?” là câu hỏi kiến thức. Từ đơn “cá”, “Mỹ”, “Omni Flash” chưa đủ phân biệt khi có nhiều dự án. Đọc metadata các dự án khác trước khi kết luận độc nhất.

2026-10-16: v1.2 điều chỉnh ngôn ngữ và nhận diện theo đặc trưng; giữ rà lịch sử và format kỹ thuật.

2026-10-16: v1.3 chuyển cấu trúc Channel sang Project và đổi tên dự án thành Underwater; xem UF-D013. Mục tiêu, format, lựa chọn loài, model và hợp đồng đầu ra giữ nguyên.
