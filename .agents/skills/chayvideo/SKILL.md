---
name: chayvideo
description: Tạo bộ ý tưởng và prompt video Nature Studio khi gọi /chayvideo hoặc yêu cầu làm video qua đặc trưng dự án như Redfish, Muskie, Walleye, câu cá Mỹ hay camera dưới nước. Tự tra dự án phù hợp, rà lịch sử tránh trùng; ý tưởng tiếng Việt, FIRST FRAME PROMPT và VIDEO PROMPT tiếng Anh, CAPTION tiếng Anh Mỹ tự nhiên kèm hashtag. Không tự render/đăng; không kích hoạt cho câu hỏi kiến thức hoặc sửa skill.
---

# /chayvideo

Version: 1.5 | Updated: 2026-10-16

Nhận `/chayvideo` trong tin nhắn như lời gọi quy trình. Có thể kèm tên dự án, số bộ, loài, brief hoặc yêu cầu sửa. Dùng workspace chứa file này làm gốc (đi lên ba cấp từ thư mục skill); không phụ thuộc ổ E: hoặc thư mục shell hiện tại. Các đường dẫn dưới đây tính từ gốc workspace.

## Xác định phạm vi và đọc nguồn

1. Đọc `START-HERE.md`, `SYSTEM.md` và `00-Standards/INDEX.md`; đọc tiêu chuẩn research, production, quality-review, memory-policy liên quan. Khi tạo concept mới, bắt buộc đọc `00-Standards/creativity.md`, kết hợp hướng dẫn riêng của dự án. Tôn trọng yêu cầu hiện hành của người dùng.
2. Xác định dự án từ ý định tạo bộ nội dung và các đặc trưng, không bắt buộc người dùng nhớ tên dự án hoặc gõ /chayvideo. Liệt kê và đọc mô tả/nhận diện trong mọi `03-Projects/*/PROJECT.md`; nếu thiếu metadata, tra format, đối tượng và output-contract tương ứng. Ưu tiên tên/ID người dùng nêu rõ, sau đó tổ hợp chủ đề, loài, môi trường, thị trường, format và ngữ cảnh hiện hành. Không chọn chỉ bằng một từ chung như “cá”, “Mỹ” hoặc “Omni”. Khi một dự án khớp rõ, tự chọn và ghi tên dự án vào brief/nhãn Ý TƯỞNG, không hỏi xác nhận lại. Khi nhiều dự án cùng khớp mà chưa phân biệt được, hỏi một câu ngắn; khi không dự án nào phù hợp thì hỏi dự án cần dùng, không ép vào dự án duy nhất. Nếu thiếu mọi dấu hiệu và chỉ có một dự án configured, có thể dùng dự án đó. Câu hỏi kiến thức về loài hoặc thảo luận/sửa skill không phải lệnh sản xuất.

   Dùng Slug/thư mục hiện hành trong PROJECT.md cho đường dẫn sản xuất; ID ổn định có thể khác slug sau đổi tên. Underwater dùng `03-Projects/underwater/PROJECT.md` và `04-Productions/underwater/`, giữ ID `under-fishing-us`/prefix UF để nối lịch sử. Tên cũ chỉ là alias của cùng dự án, không tạo dự án mới.

   Ví dụ với kho hiện tại: “Làm một bộ Walleye theo jig rồi quay đi” hoặc “/chayvideo red drum ở lạch triều Texas” → Underwater, không hỏi tên dự án. “Muskie sống ở đâu?” → trả lời kiến thức, không tạo production. Khi thêm dự án mới, đọc lại metadata hiện hành thay vì coi các ví dụ này là bảng định tuyến cố định.
3. Đọc toàn bộ `PROJECT.md`, `format.md`, `audience-and-caption.md`, `output-contract.md`, `decisions.md` và `idea-ledger.md` của đúng dự án. Đọc tài liệu tham chiếu bắt buộc được các file đó dẫn, bao gồm creative-direction nếu dự án có chỉ định; dùng baseline khi cần tìm ràng buộc còn thiếu. Tài liệu phát hành cũ là lịch sử, không ghi đè quyết định mới.
4. Tra `01-Knowledge/INDEX.md` và các hồ sơ loài, môi trường, tương tác, dụng cụ thực sự liên quan; tra `02-Models/INDEX.md` và model profile đúng dự án. Mở nguồn bên ngoài khi cần kiểm dữ kiện mới/hiện hành, ghi đúng việc đã truy cập. Thiếu nguồn bắt buộc để chốt chi tiết thì xử lý giới hạn trước khi giao, không bịa nguồn hoặc thông số.
5. Đọc `05-Memory/INDEX.md`, `05-Memory/projects/<slug>/INDEX.md` và `05-Memory/shared/INDEX.md`; tìm file thực nếu chỉ mục thiếu/cũ. Mở lesson gốc, chỉ áp active khớp Project ID ổn định và điều kiện nhiệm vụ/model/giao diện/format; shared không áp mặc định mọi nơi. Không tự áp bộ nhớ Project khác. Candidates chỉ gợi ý thử, retired là lịch sử; đọc lỗi/feedback production liên quan dù chưa active, không nâng lỗi cục bộ thành quy chuẩn chung. Gặp mâu thuẫn với brief/quy chuẩn thì nêu vấn đề, không dùng lesson ghi đè.

Với Underwater, giữ bước chọn loài tại PROJECT.md: nếu chưa có loài hoặc quyền chọn, hỏi Redfish / Muskie / Walleye / loài cá được câu bất kỳ ở Mỹ và chờ. Đã có lựa chọn hoặc quyền chọn thì không hỏi lại. Chưa đủ đầu vào không tạo hồ sơ/ý tưởng giả để lấp chỗ trống.

## Rà dữ liệu cũ trước khi chọn ý tưởng — bắt buộc

- Kiểm cả lịch sử chat đang truy cập, dữ liệu người dùng đưa, `idea-ledger.md` và file thực dưới `04-Productions/<slug>/`. Liệt kê file trước bằng `rg --files` (hoặc công cụ tương đương); không kết luận không có lịch sử chỉ vì ledger trống.
- Đọc mọi SUMMARY và concept hiện có của dự án để lập danh sách cơ chế cũ. Tìm thêm trong brief, feedback, review và prompt của các trường hợp gần giống; hồ sơ thiếu SUMMARY/concept phải tra nội dung thực còn lại. Dùng tìm kiếm từ khóa/đồng nghĩa theo loài, prey/bait/lure, rig, hành động, key, kết cục; không chỉ so tiêu đề hoặc chuỗi chữ giống hệt.
- Tính cả ý tưởng nháp đã giao, bị loại, retired và ví dụ tham chiếu vào danh sách đối chiếu, nhưng ghi đúng trạng thái: ví dụ không phải sản phẩm đã làm. Tra dự án khác khi chung chủ đề/cơ chế để phát hiện việc tái dùng; đánh giá trong phạm vi dự án, không cấm một cơ chế ở mọi thể loại.
- So sánh theo: câu hỏi mở đầu, kiểu tương tác, mồi/con mồi hoặc dụng cụ, vai trò địa hình, nguyên nhân và hành động key, hậu quả/kết cục. Đổi tên loài, màu, địa danh, thời tiết, caption hoặc thời điểm đơn thuần không tạo ý tưởng mới.
- Khi tạo mới, cân nhắc vài hướng rồi loại hướng trùng. Với Underwater, so với cảnh gần nhất phải có ít nhất hai khác biệt có ý nghĩa, trong đó ít nhất một thuộc key, kiểu tương tác hoặc kết cục; đổi loài đơn thuần không tính. Dự án khác theo tiêu chí riêng, tối thiểu khác cơ chế kể chuyện thực chất. Nếu ràng buộc đã khóa khiến không thể tạo khác biệt, nói rõ và hỏi lựa chọn cần thay đổi.
- Khi sửa/tiếp tục một production hoặc người dùng yêu cầu lặp lại, giữ ý tưởng/loài đã chọn, ghi là revision/tái dùng có chủ đích; không đổi chuyện để đạt chỉ tiêu mới.
- Ghi vào concept: đường dẫn/ID đã đối chiếu, trường hợp gần nhất, khác biệt cụ thể và phần lịch sử chưa truy cập. Nếu kho chưa có production, ghi đúng điều đó và vẫn tránh lặp nguyên ví dụ. Không tuyên bố độc nhất hoặc chưa từng làm ngoài dữ liệu đã kiểm. Nếu lịch sử có nhưng không đọc đủ, thông báo giới hạn; không đánh dấu đã rà toàn bộ.
- Với nhiều bộ trong cùng yêu cầu, đối chiếu chéo các ý tưởng vừa chọn trước khi giao để chúng không trùng nhau.

## Phát triển câu chuyện độc lập với cảnh mẫu

Sau khi rà lịch sử và trước khi chốt concept, tách yêu cầu bắt buộc khỏi ví dụ. Dùng lịch sử làm dấu vân tay cơ chế để đối chiếu, không làm khuôn kịch bản. Phát triển vài tiền đề có tín hiệu kích hoạt, hành vi và quan hệ nhân quả khác nhau từ brief và dữ kiện; không chỉ sửa chi tiết của một tiền đề. Danh sách tình huống trong tài liệu không phải tập lựa chọn đóng; không bốc thăm thể loại hoặc buộc mỗi ý tưởng thuộc một nhóm định sẵn.

Đối chiếu các hướng ở cấp câu chuyện: bỏ tên loài/màu/địa danh mà chúng vẫn cùng một diễn biến thì cần phát triển thêm trước khi chọn. Ngưỡng hai khác biệt của Underwater là điều kiện tối thiểu, không đủ để gọi là mới nếu hành vi và nhân quả cốt lõi vẫn lặp. Không cấm vĩnh viễn một kết cục chỉ vì từng xuất hiện; sáng tạo không đồng nghĩa thêm cú sốc, thêm chủ thể hoặc sai sinh học.

Với Underwater, đọc và áp dụng `03-Projects/underwater/creative-direction.md`. Chọn điểm đáng quan sát trước rồi xây timeline theo format; nếu khó render, thử đơn giản hóa cách thể hiện mà giữ điểm mới thay vì tự quay lại cảnh quen. Chỉ lưu tiền đề đã chọn, cơ chế tò mò, căn cứ và kết quả đối chiếu ngắn trong concept; không xuất suy luận nội bộ hoặc thêm phương án vào bốn mục khi không được yêu cầu. Revision không kích hoạt yêu cầu thay câu chuyện.

## Soạn đầu ra và tự kiểm

Mặc định một bộ. Tự giải quyết chi tiết thông thường trong phạm vi brief. Khóa trạng thái t=0, chủ thể, môi trường, kết nối, đường đi, nguồn lực, key và hậu quả trước khi viết prompt.

Trả đúng bốn mục sau cho mỗi bộ: ý tưởng tiếng Việt; hai prompt và caption tiếng Anh. Không kèm bản dịch song ngữ trừ khi được yêu cầu:

1. **Ý TƯỞNG**: một đoạn ngắn mô tả câu chuyện, câu hỏi mở đầu, key/kết cục dự kiến và điểm khác thực chất so với dữ liệu cũ khi có.
2. **FIRST FRAME PROMPT**: một đoạn tiếng Anh duy nhất, tự đủ để sao chép, chỉ mô tả ảnh t=0: chủ thể, môi trường, bố cục, camera, ánh sáng, tỷ lệ và các vật thực sự nhìn thấy. Không có diễn biến tương lai hoặc âm thanh trong prompt ảnh. Ảnh sẽ dùng làm đầu vào mở đầu của Omni Flash, nhưng không tự đổi model tạo ảnh nếu chưa được chỉ định.
3. **VIDEO PROMPT**: một đoạn tiếng Anh duy nhất, tự đủ và tiếp nối đúng ảnh đầu. Với Google Omni Flash, đọc hướng dẫn tại `02-Models/model-profiles/omni-flash.md`; tổ chức lời prompt theo thứ tự ảnh mở đầu → thời lượng/tỷ lệ/camera → bối cảnh và tính nhất quán → chuyển động/beat/nhân quả → Sound design → loại trừ ngắn. Đây là cách soạn của studio theo hướng dẫn model, không phải schema API bắt buộc. Mốc thời gian/beat đặt ngay trong đoạn, ví dụ `[0.0–1.3s] ...; [1.3–2.6s] ...`; không trình bày timeline thành bảng, danh sách hoặc nhiều đoạn. Tích hợp âm thanh trong cùng đoạn theo quy chuẩn dự án. Chỉ dùng `<FIRST_FRAME>` khi giao diện hỗ trợ; tag không thay thao tác đính kèm ảnh.
4. **CAPTION**: một đoạn tiếng Anh Mỹ tự nhiên, như người bản xứ nói với nhóm khán giả Mỹ của dự án; không hiểu “American English” thành phong cách của người Mỹ bản địa (Native American). Hook cụ thể, tò mò từ sự kiện dự kiến/thực tế; không dịch sát tiếng Việt, nhồi slang hoặc dùng thuật ngữ sai. Với Underwater, giọng người câu cá Mỹ, hook thường 3–8 từ và 3–5 hashtag liên quan nối cùng đoạn, không nhắc AI; không tuyên bố mắc câu/bắt được khi hình chưa chứng minh.

Không chèn CR/LF trong nội dung của từng prompt (giao diện tự ngắt dòng theo chiều rộng vẫn được). Không placeholder, câu “như trên”, ghi chú nghiên cứu hoặc link trong prompt/caption. Nếu người dùng yêu cầu JSON, dùng bốn khóa `idea`, `first_frame_prompt`, `video_prompt`, `caption`; các giá trị là chuỗi, hai prompt và caption không chứa xuống dòng. Chỉ thêm thông báo ngắn ngoài bốn mục khi thiếu dữ liệu quan trọng hoặc cần chỉ rõ giới hạn; đường dẫn hồ sơ có thể gắn ngay nhãn Ý TƯỞNG.

Đây là hợp đồng v1.1 cho skill, áp dụng cả /chayvideo và lời gọi ngầm theo đặc trưng dự án: thay yêu cầu v1.0 xuất toàn bộ tiếng Việt. Tên mục giữ đúng Ý TƯỞNG, FIRST FRAME PROMPT, VIDEO PROMPT, CAPTION. Ngoài ý tưởng tiếng Việt, ba nội dung còn lại bằng tiếng Anh; yêu cầu trực tiếp mới của người dùng vẫn ưu tiên.

Kiểm trước khi giao:

- Đã xác định đúng dự án, đọc nguồn hiện hành và rà lịch sử thực; độ mới có căn cứ hoặc ghi giới hạn.
- Đã kiểm cơ chế câu chuyện sau khi bỏ tên loài/bối cảnh; ý tưởng không chỉ là cảnh mẫu đổi chi tiết, không bị giới hạn bởi danh mục ví dụ. Phản hồi chất lượng chỉ là bằng chứng trong phạm vi được quan sát, không bảo đảm mọi đầu ra tương lai sáng tạo.
- Ý tưởng, ảnh đầu, video và caption cùng loài, số lượng, vật thể, bố cục mở đầu và kết cục; đúng sinh học/môi trường, không bịa kết nối hay kết quả.
- Đủ bốn mục với đúng tên; ý tưởng tiếng Việt, hai prompt tiếng Anh, caption tiếng Anh Mỹ tự nhiên; mỗi prompt một đoạn, caption và hashtag cùng một đoạn, dễ sao chép.
- Underwater vẫn giữ 10s, 9:16, một shot camera cố định mặc định, 5–8 beat liên tục, onset key >5.0s, setup có tiến triển và có hậu quả; âm môi trường + hành động lớn/rõ suốt clip, có nguồn, mặc định không nhạc/voice; 3–5 hashtag đúng cảnh, không AI. Cấu trúc prompt cho Omni Flash không làm thay đổi các ràng buộc riêng của dự án.
- Phân biệt kiểm prompt với kiểm ảnh/video thật. Không hứa model tuân thủ timecode hoặc đã QA media khi chỉ có văn bản. Tìm lỗi rồi sửa bộ nội dung trước khi giao; không tự render để kiểm.

## Lưu để lần sau tra lại

Khi đã đủ đầu vào và có bộ nội dung thật, tạo production/attempt theo `00-Standards/production.md` và các template; tra ID trước khi cấp mới, không ghi đè lần cũ. Lưu brief, research, concept, SUMMARY, feedback/performance theo trạng thái thực; attempt có INPUTS, hai prompt, caption, settings, review. Settings ghi chưa thực thi/unknown đúng nghĩa, review ở mức prompt-only, performance chưa đăng. Không tạo file media giả.

Trong concept lưu kết quả rà trùng; trong INPUTS lưu phiên bản/đường dẫn nguồn và ID + version + đường dẫn + cách áp dụng của lesson active thực sự dùng; candidate được thử ghi riêng. Cập nhật `idea-ledger.md` với ID, cơ chế/key/kết cục và liên kết SUMMARY ngay khi đã giao bản drafted để lần sau tra được, không chờ render/đăng. Revision thêm attempt hoặc version trong hồ sơ hiện có. Không coi drafted là selected/approved/published.

Lỗi/phản hồi mới được ghi đúng hồ sơ, bài học mới theo memory-policy; không tự nâng candidate thành active. Lệnh `/chayvideo` chỉ tạo văn bản và hồ sơ local; tạo media, chi tiền hay đăng bài cần yêu cầu tương ứng của người dùng.

Sau phiên, người dùng có thể gọi `/dongvideo <production-id>` để tổng kết và xét đóng góp bộ nhớ Project/shared theo skill dongvideo. Không tự đóng phiên từ lệnh tạo nội dung; /chayvideo không tự kích hoạt lesson.
