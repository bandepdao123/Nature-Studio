# Khán giả và giọng — v1.7

Updated: 2026-10-17 | Origin: approved guide v1.9 + /chayvideo

**Chế độ skill /chayvideo (kể cả nhận diện theo đặc trưng):** theo [output-contract.md](output-contract.md), giữ caption tiếng Anh Mỹ tự nhiên, phù hợp người câu cá Mỹ, một đoạn gồm hook ngắn và 3–5 hashtag đúng cảnh; ý tưởng tiếng Việt, FIRST FRAME PROMPT và VIDEO PROMPT tiếng Anh, mỗi prompt một đoạn. Yêu cầu mới này thay ngoại lệ caption tiếng Việt ở v1.1. Các tiêu chí giọng/cấu trúc bên dưới tiếp tục áp dụng. Lý do: điều chỉnh người dùng 2026-10-16.

Khán giả Mỹ thích câu cá; ngôn ngữ đầu ra tiếng Anh Mỹ, gợi tò mò bằng chi tiết thật trong clip. Không tự nhận giọng native bảo đảm performance.

### Caption đăng tải: một caption hoàn chỉnh có 3–5 hashtag

**Phong cách đã chốt — UF-D015:** học cách viết Underfishing qua benchmark 40 caption: ít chữ, trực tiếp, như một người câu cá phản ứng hoặc trao đổi ngay khi nhìn footage. Caption chọn **một chi tiết/hành động/phán đoán đáng chú ý**, không tóm tắt toàn bộ kịch bản hoặc viết lời quảng cáo. Dùng câu chữ nguyên bản và tiếng Anh Mỹ tự nhiên; học cơ chế giao tiếp, không chép caption, lỗi ngữ pháp hay jargon không đúng cảnh.

**Độ dài:** ưu tiên một câu hoặc cụm ngắn, thường 1–8 từ trước hashtag; 1–2 từ được phép khi hình đủ ngữ cảnh, dài hơn khi câu hỏi/chi tiết cần để tự nhiên và rõ nghĩa. Đây là ưu tiên biên tập, không quota hoặc giới hạn cứng. Không cố kéo câu ngắn thành 3 từ, không rút câu dài làm mất ý, không bắt chước caption chỉ có dấu hỏi vì thiếu ý tưởng.

**Kiểu viết:** linh hoạt câu hỏi, nhận xét, phản ứng ngắn, lời chỉ dẫn quan sát hoặc mời đánh giá một lựa chọn cụ thể. Chọn theo footage, không ép mọi caption là câu hỏi, không đặt tỷ lệ và không quay vòng các nhóm như danh mục đóng. Tò mò có thể đến từ vì sao, lúc nào, vật gì, quyết định nào hoặc điều bất ngờ; có thể nhắc kết quả đã thấy để người xem xem xét nguyên nhân, không bắt buộc giấu kết cục. Giọng gần gũi, ít lời, không hô hào “watch till the end”, không câu tương tác rỗng bằng “Comment YES”/tag bạn bè.

**Đúng cảnh và đúng khán giả:** không ép mọi video vào cú hụt/thoát móc/tranh mồi. Cá săn mồi tự nhiên không cần rig/lure; chỉ dùng *follow, short strike, commit, spit the bait, hookset, rig, lure, jig* khi hình hỗ trợ và đúng cách nói người câu cá Mỹ. Phân biệt bait/lure, tiếp cận/ăn/mắc câu; không tuyên bố hooked/caught/swallowed khi chưa thấy. Không nhập thuật ngữ carp như chod/boilies/tigers chỉ để giống đối thủ. Ở giai đoạn prompt, bám concept dự kiến và kiểm lại theo video thật; không coi concept là bằng chứng đã diễn ra.

**Trước khi giao:** xem caption có chọn đúng một điểm đáng xem, nghe như câu nói tự nhiên và có lặp cách mở/cấu trúc trong lịch sử Project không; sửa câu gượng hoặc chung chung. Ví dụ tự viết: `Not buying that lure.` khi cá thể hiện từ chối lure; `Watch that last-second turn.` khi có cú quay cuối rõ; `Would you change the retrieve?` khi footage có retrieve phù hợp. Đây là ví dụ có điều kiện, không phải khuôn phải lặp hoặc kết luận hiệu quả.

**Cấu trúc một caption:** câu hook ngắn + một dấu cách + **3–5 hashtag khác nhau**, tất cả **viết liền thành một đoạn văn duy nhất, không xuống dòng trước hashtag, không tách hashtag thành dòng/đoạn riêng**. Ví dụ định dạng: `What made him turn off? #Muskie #MuskyFishing #FreshwaterFishing`. Đây là **một trường caption** có thể sao chép đăng ngay; giao diện tự ngắt dòng theo chiều rộng màn hình không phải ký tự xuống dòng do AI chèn. **Không nhắc AI, việc tạo/sinh/mô phỏng video hoặc bất kỳ công nghệ tạo nội dung nào trong caption; không thêm dòng giải thích nguồn tạo. Không dùng hashtag về AI.** Tập trung hoàn toàn vào loài vật, hành động, câu hỏi và cảm giác tò mò như phong cách kênh tham chiếu. Không cần nhét địa danh vào câu hook nếu làm nó dài và gượng.

**Chọn hashtag — UF-D016:** không dùng `#Underwater` (không phân biệt hoa/thường); không biến tên Project thành tag mặc định. Giữ 3–5 tag khác đúng cảnh, không dùng biến thể chữ hoa/thường của tag đã loại để lách quy tắc.  ưu tiên một tag loài chính, một tag ngữ cảnh câu cá hợp loài, rồi tag phương pháp hoặc môi trường phù hợp; có thể thêm tag vùng khi đúng brief. Không gắn cả ba loài nếu chỉ có một loài; không dùng một chuỗi tag cố định sai nội dung; không nhồi `#viral #fyp #trending`; loại mọi hashtag về AI hoặc công nghệ tạo video. Ví dụ nhóm hợp ngữ cảnh: Redfish — `#Redfish #InshoreFishing #SaltwaterFishing`; Muskie — `#Muskie #MuskyFishing #FreshwaterFishing`; Walleye — `#Walleye #WalleyeFishing #FreshwaterFishing`.

**Quy tắc đầu ra:** gọi mục này là **CAPTION**, không phải TITLE. Không tách tiêu đề và hashtag thành hai sản phẩm; nếu dùng JSON theo yêu cầu người dùng, lưu toàn bộ trong **một chuỗi `caption` không có ký tự xuống dòng**, không tạo trường `hashtags` riêng. Caption không phải lời thoại hoặc chữ phải vẽ vào video. Các con số 3–5 hashtag là yêu cầu biên tập của dự án mới, không phải nhận định rằng đối thủ dùng hashtag hoặc quy tắc bảo đảm reach.

## Nghiên cứu tham chiếu — 2026-10-16

Phong cách đã duyệt ở trên là nguồn chạy mặc định. Mở báo cáo gốc khi nghiên cứu lại phong cách, cần ví dụ/đối chứng hoặc nguồn thay đổi; không bắt đọc lại mọi caption mỗi lần sửa một câu. Tham chiếu [benchmark 40 caption Underfishing](../../01-Knowledge/benchmarks/underfishing-captions-2026-10-16/REPORT.md). Nghiên cứu là quan sát, không chứng minh caption gây viral; phong cách được áp dụng theo **quyết định trực tiếp của người dùng UF-D015**, không phải tự nâng hypothesis thành active. Giữ **3–5 hashtag** dù mẫu đối thủ không thấy hashtag. Quyết định này cập nhật ưu tiên độ ngắn/kiểu câu; mọi giới hạn kỹ thuật video và ngôn ngữ vẫn giữ. Báo cáo nghiên cứu gốc giữ nguyên để truy vết các đề xuất trước quyết định.
