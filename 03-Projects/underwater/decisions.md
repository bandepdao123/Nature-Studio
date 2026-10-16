# Quyết định hiện hành

Các quyết định dưới kế thừa yêu cầu người dùng và hướng dẫn v1.9; không phải kết quả đo hiệu quả.

| ID | Ngày | Quyết định | Phạm vi / nguồn hiện hành |
|---|---|---|---|
| UF-D001 | 2026-10-15 | Video 10s, 9:16; camera đời thực; một shot | format.md |
| UF-D002 | 2026-10-15 | Mỗi lần tạo mới có ý tưởng mới; sửa cũ giữ trọng tâm | format.md |
| UF-D003 | 2026-10-15 | Hỏi loài nếu thiếu, bốn lựa chọn và đường nhập khác | PROJECT.md |
| UF-D004 | 2026-10-15 | Môi trường + hành động lớn/rõ xuyên suốt, không nhạc/voice mặc định | format.md |
| UF-D005 | 2026-10-15 | Caption native US angler, tò mò, một đoạn với 3–5 hashtag, không nhắc AI | audience-and-caption.md |
| UF-D006 | 2026-10-15 | Tackle và tương tác phù hợp loài/vùng; không tự thêm đồ câu vào wild prey | Knowledge/equipment và output-contract.md |
| UF-D007 | 2026-10-15 | Key bắt đầu sau 5.0s, không dời riêng đỉnh; có setup và hậu quả | format.md, kế thừa v1.9 trực tiếp từ v1.7 |
| UF-D008 | 2026-10-16 | Dùng /chayvideo làm quy ước gọi skill trong chat; tạo văn bản và hồ sơ local, không tự render | ../../.agents/skills/chayvideo/SKILL.md; AGENTS.md |
| UF-D009 (đã thay bởi UF-D011) | 2026-10-16 | /chayvideo trả bốn mục tiếng Việt: ý tưởng, prompt first frame, prompt video, caption; mỗi prompt một đoạn. Trong chế độ này thay yêu cầu ba mục tiếng Anh và ngôn ngữ ở UF-D005; thị trường Mỹ và tiêu chí caption còn lại giữ nguyên | output-contract.md; audience-and-caption.md |
| UF-D010 | 2026-10-16 | Rà ledger, SUMMARY/concept, hồ sơ thực và lịch sử truy cập trước khi chọn ý tưởng; so cơ chế/key/kết cục, lưu đối chiếu và ghi drafted vào ledger; revision giữ trọng tâm | skill chayvideo; format.md |
| UF-D011 | 2026-10-16 | Thay UF-D009: Ý TƯỞNG tiếng Việt; FIRST FRAME PROMPT và VIDEO PROMPT tiếng Anh, mỗi prompt một đoạn, theo model profile Google Omni Flash; CAPTION tiếng Anh Mỹ tự nhiên kèm 3–5 hashtag hợp người câu cá Mỹ | output-contract.md; audience-and-caption.md; model profile |
| UF-D012 | 2026-10-16 | Skill nhận yêu cầu tạo nội dung qua đặc trưng dự án, tự tra metadata mọi dự án; không bắt buộc tên dự án hoặc /chayvideo; chỉ hỏi khi chưa có khớp rõ; không tự sản xuất từ câu hỏi kiến thức | PROJECT.md; skill chayvideo; AGENTS.md |

| UF-D013 | 2026-10-16 | Đổi cấu trúc quản lý Channel thành Project: 03-Projects/<slug>/PROJECT.md; đổi tên Under Fish US / Under Fishing US thành Underwater, slug underwater; giữ ID under-fishing-us, prefix UF và các quyết định cũ để truy vết. Hồ sơ sản xuất chuyển sang 04-Productions/underwater | PROJECT.md; SYSTEM.md; manifest project-migration-2026-10-16 |

| UF-D014 | 2026-10-16 | Bổ sung sáng tạo mở: ví dụ không là danh mục đóng; phát triển tiền đề độc lập từ brief/dữ kiện, chọn chuyện rồi xây timeline; kiểm độ mới bằng hành vi/nhân quả, không chỉ đếm hai thuộc tính khác; revision giữ chuyện đã chốt | creative-direction.md; format.md; skill chayvideo v1.3 |

Khi đổi, thêm dòng quyết định thay thế và cập nhật chính file nguồn. Không để hai quyết định xung đột cùng mang trạng thái hiện hành.

| UF-D015 | 2026-10-16 | Người dùng chọn Underwater học phong cách caption Underfishing sau benchmark 40 Reel: ít chữ, trực tiếp, một điểm đáng xem, linh hoạt hỏi/nhận xét/phản ứng/chỉ dẫn; thường 1–8 từ không cứng, giữ Anh Mỹ tự nhiên và 3–5 hashtag cùng đoạn. Thay ưu tiên độ dài/kiểu câu trước đó; giữ các yêu cầu còn lại. Không coi thành công đối thủ là bằng chứng nhân quả hoặc hiệu quả đã kiểm của Underwater | audience-and-caption.md v1.5; output-contract.md v1.5; chayvideo v1.7; yêu cầu trực tiếp người dùng trong phiên này |

| UF-D016 | 2026-10-16 | Người dùng yêu cầu không dùng #Underwater trong caption mới/revision, không phân biệt hoa/thường; giữ 3–5 hashtag khác phù hợp loài/phương pháp/môi trường. Thay ví dụ tag cũ, không đổi caption/attempt lịch sử | audience-and-caption.md v1.6; output-contract.md v1.6; chayvideo v1.8 |

| UF-D017 | 2026-10-16 | Triển khai Story Development có nguồn: liên quan khán giả, câu hỏi/khám phá thị giác, tiến triển nhân quả, key/hậu quả và kiểm giả thuyết; giữ sáng tạo mở và format/caption hiện hành. Không cam kết viral hoặc tự active lesson hiệu quả | story-development.md; ../../00-Standards/story-development.md; yêu cầu trực tiếp người dùng |

| UF-D018 | 2026-10-16 | Người dùng yêu cầu xây /taoanh và keyword tạo ảnh/tạo first frame, image_gen với ưu tiên Sunburst, không tìm được thì dùng model mặc định không hỏi lại; QA ảnh thật sau từng lượt, tối đa 5 call rồi xin thêm. Actual model chỉ ghi khi có căn cứ; danh tính model không là tiêu chí QA hoặc cổng chặn sinh ảnh, không tự chuyển API/CLI. Không tạo ảnh từ yêu cầu xây skill | skill taoanh v1.0; first-frame.md; first-frame-qa.md; model profile sunburst-imagegen |
