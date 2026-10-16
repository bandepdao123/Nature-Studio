# Underfishing — nghiên cứu 40 caption trên Reel triệu lượt xem

ID: K-BM-UF-CAP-20261016 | Version: 1.1 | Accessed: 2026-10-16 (Asia/Saigon)
Project áp dụng nghiên cứu: Underwater (under-fishing-us). Đây là benchmark mô tả và đề xuất thử, không là quy chuẩn được xác nhận hiệu quả.
Nguồn: [trang Reels Underfishing](https://www.facebook.com/Underfishing.life/reels/).

## Cách chọn và giới hạn

- Truy cập trang nguồn bằng trình duyệt đăng nhập. Công cụ web fetch bị throttled; kết quả tìm kiếm không cung cấp được mẫu nên không dùng làm dữ liệu caption/view.
- Rà 130 ô Reel theo thứ tự trang hiển thị trong phiên; 46 ô hiển thị từ 1 triệu trở lên. Chọn lần lượt các ô có số hiển thị >1 triệu, bỏ mốc đúng “1 triệu” vì làm tròn.
- Mở 42 Reel: 2 mục không thấy caption cả khi truy cập lại (1614261063381636, 1010127058492958) được loại khỏi thống kê chữ; lấy 2 mục tiếp theo cùng tiêu chí để có 40 caption đọc được. Caption chỉ “??” vẫn là caption có hiển thị và được tính.
- Đối chiếu tác giả Underfishing/ID trang 100063897016400 ở từng player. Khi có bản dịch tự động, dùng “Ẩn bản dịch” trước khi lấy tiếng Anh gốc; giữ nguyên cả lỗi ngữ pháp/chính tả trong corpus, không âm thầm sửa nguồn.
- Lượt xem là nhãn làm tròn trên lưới trang tại thời điểm truy cập, không phải số exact, reach, unique viewers hoặc dữ liệu lịch sử lúc đăng. Không có ngày đăng/retention/impressions hoặc nhóm video thấp view để kiểm nguyên nhân.
- Đọc caption 40 mục, chụp player 42 mục và xem contact sheet; đây không phải xem trọn 40 video hoặc nghe âm thanh. Ảnh là một khung tại lúc chụp, chỉ đủ đối chiếu bối cảnh sơ bộ, không xác nhận toàn bộ diễn biến/loài/rig.
- Không phải top 40 nhiều view nhất, mẫu ngẫu nhiên, hay mẫu đại diện toàn kênh. Có thiên lệch chỉ chọn video nhiều view và chỉ đọc được caption. Không kết luận dạng caption/độ dài/hashtag đã tạo ra lượng view đó.
- Không nhận Underfishing dùng giọng Anh Mỹ chuẩn: nhiều từ riêng của câu carp (boilies, chod, hookbait, tigers, lead) và câu không chuẩn. Không chuyển nguyên thuật ngữ đó sang Redfish/Muskie/Walleye.

Dữ liệu: [corpus JSON](corpus.json), [CSV](corpus.csv), [130 ô đã rà](screened-reels.json), ảnh tổng hợp chỉ lưu local (không kèm bản GitHub). Screenshots lưu local cho kiểm tra nguồn, có giao diện tài khoản; không tự đưa lên public/GitHub. Không tải MP4, không tương tác like/comment/follow.

## Những gì đếm được

| Chỉ số | Quan sát trong mẫu |
|---|---|
| Caption gốc đọc được | 40 |
| Lượt xem hiển thị | 1,1–6 triệu, làm tròn |
| Trung vị / trung bình số từ | 5 / 4,725 |
| 1–8 từ | 37/40 (92,5%) |
| Trên 8 từ | 2/40 (11 và 12 từ) |
| Không có từ, chỉ dấu câu | 1/40 (“??”) |
| Có dấu hỏi | 21/40 (52,5%), gồm mục chỉ dấu hỏi |
| Có hashtag trong caption player đọc được | 0/40 |

Đếm từ bằng biểu thức tách token chữ/số, giữ từ có dấu nháy là một từ; không đếm dấu câu. Phần UI/âm thanh gốc/tên tác giả/bản dịch bị loại. Không suy 0/40 thành “kênh chưa từng dùng hashtag”.

## Bài học biên tập rút ra

### Caption chọn một việc để người xem chú ý

Điểm lặp là câu ngắn chọn một điểm quan sát hoặc phán đoán, thay vì kể lại toàn bộ clip: xác định vật/rig/mồi, soi dấu hiệu, đặt câu hỏi vì sao hụt, so hai lựa chọn hoặc phản ứng như bạn câu cùng xem. Caption có thể tiết lộ đã mất cá rồi vẫn để mở câu hỏi tại sao; “không spoiler kết cục” không phải quy tắc chung rút được từ mẫu.

Câu cụ thể gắn vật/chi tiết nhìn thấy tạo một nhiệm vụ quan sát rõ hơn câu tò mò chung. Đây là giải thích biên tập có cơ sở ở câu chữ, chưa là thử nghiệm retention. Không được bịa chi tiết bí ẩn chỉ để đặt câu hỏi.

### Không bắt mọi caption thành câu hỏi

Có 19/40 không có dấu hỏi; nhiều câu là nhận xét, phản ứng hoặc chỉ dẫn xem một chi tiết. Ngay trong nhóm hỏi cũng có nhận diện, nguyên nhân, hành vi, thời điểm và lựa chọn kỹ thuật. Cần chọn theo footage, không xoay vòng một danh mục bắt buộc hoặc dùng một mẫu câu cho mọi video.

### Ngắn vì ngữ cảnh nằm trong hình

37/40 có 1–8 từ, nhưng hai câu dài hơn vẫn nằm trong mẫu triệu view. “Ngắn” là ưu tiên tiết kiệm lời, không phải cắt mọi caption về một độ dài hay đảm bảo viral. Caption một từ/dấu câu dựa nặng vào hình, không mặc định phù hợp video mới chưa có ngữ cảnh rõ.

### Dùng tri thức cộng đồng đúng chỗ

Một số câu mời người câu đánh giá rig, bait, hookpull, tight lines. Học cách chọn một vấn đề người xem có kinh nghiệm có thể bàn, không học bằng cách chép biệt ngữ. Với Underwater thị trường Mỹ, thay bằng chi tiết thực về retrieve, follow, lure, hookset… chỉ khi có hình hỗ trợ; cảnh săn mồi tự nhiên không cần ép thành câu chuyện đồ câu.

### Không học cả lỗi câu chữ

Corpus có cách diễn đạt không chuẩn, viết tắt, dấu chấm lửng và cường điệu. Có thể học tính gần gũi/ít chữ, nhưng đầu ra của Underwater vẫn dùng tiếng Anh Mỹ tự nhiên, đúng thuật ngữ. Nhân hóa chỉ là giọng kể khi thích hợp, không biến thành khẳng định tập tính/suy nghĩ cá đã được chứng minh.

### Hashtag là chỗ cần tách quan sát khỏi quyết định

Mẫu 40 caption không hiển thị hashtag. Quy định Underwater hiện vẫn yêu cầu 3–5 hashtag đúng cảnh. Nghiên cứu này không tự bỏ quy định và không chứng minh thêm/bớt hashtag tăng reach. Đề xuất khi người dùng cho phép: so các đợt đăng tương đương với 0 tag và 3–5 tag; ghi tuổi bài, nội dung, phân phối, chỉ số thực, các biến không kiểm soát. Không đăng lặp cùng clip chỉ để giả một A/B có kiểm soát.

## Cách áp dụng ngay trong quy chuẩn đang có

1. Xác định chi tiết/hành động thật đáng xem; tách điều nhìn thấy khỏi điều chưa biết.
2. Chọn một ý định giao tiếp phù hợp: nhận xét, hỏi nguyên nhân/nhận diện/lựa chọn, hoặc chỉ chỗ nhìn. Các ví dụ không là danh sách đóng.
3. Viết một câu Anh Mỹ tự nhiên, ưu tiên từ cụ thể và bỏ lời đệm. Không mặc định luôn hỏi, luôn giấu kết cục, luôn phải có jargon.
4. Đối chiếu ảnh/video hoặc concept nếu mới prompt-only; không khẳng định đã catch/hook/swallow khi chưa có bằng chứng. Không dùng chi tiết chỉ có ở video đối thủ.
5. Theo yêu cầu hiện hành vẫn một đoạn, hook khoảng 3–8 từ và 3–5 hashtag phù hợp; thay đổi biên này cần quyết định của người dùng, không lấy benchmark làm quyền sửa policy.
6. So với caption gần đây của chính Project để tránh lặp câu mở đầu/cơ chế tò mò. Ghi hiệu quả thực sau đăng, không biến nghiên cứu đối thủ thành active lesson về performance.

Ví dụ tự viết, không lấy nguyên caption đối thủ; chỉ dùng khi footage tương ứng:

- Cá theo lure nhưng quay đi: “That follow deserved another cast.”
- Cảnh fish bám theo rõ: “Would you slow that retrieve?”
- Cảnh nhiều mồi nhưng một mồi được chọn: “Why that bait over the others?”
- Cảnh kết quả hụt đã nhìn rõ: “Close enough to make you flinch.”
- Cảnh có khe thoát rõ: “That gap changed everything.”

Các câu là minh họa ý định, chưa phải caption hoàn chỉnh của production và không có bằng chứng hiệu quả. Không tự tạo production/attempt từ nghiên cứu này.

## Đề xuất người dùng có thể quyết định sau

- Giữ mặc định khoảng 3–8 từ nhưng cho phép ngắn/dài hơn khi chi tiết cần; chưa thay trong lần nghiên cứu.
- Có thể thử 0 hashtag như đối thủ, hoặc giữ 3–5 tag hiện tại; chưa có dữ liệu để chọn cách tốt hơn.
- Giữ đa dạng hình thức câu, không biến 52,5% dấu hỏi thành tỷ lệ phải đạt.
- Đánh giá caption bằng độ khớp nội dung và mức cụ thể trước; hiệu quả nền tảng chỉ kết luận sau dữ liệu production thực.

## Corpus 40 mục

Caption dưới đây là đoạn ngắn nguyên gốc từng Reel, giữ chữ sai nếu có. Mỗi URL là nguồn riêng; số view lấy từ lưới profile, không thay bằng likes trong player.

| # | View hiển thị | Caption gốc | Từ | Cơ chế chính (mã hóa mô tả) | Nguồn |
|---|---|---|---:|---|---|
| 1 | 1,5 triệu | Love the snowman!! | 3 | phản ứng/ngắn | [Reel 1766609001232039](https://www.facebook.com/reel/1766609001232039/) |
| 2 | 1,4 triệu | Cleann! | 1 | phản ứng/ngắn | [Reel 3185936764945635](https://www.facebook.com/reel/3185936764945635/) |
| 3 | 1,4 triệu | How to lose a fish.. | 5 | lỗi/thất bại/hiệu quả | [Reel 1135811299007293](https://www.facebook.com/reel/1135811299007293/) |
| 4 | 1,3 triệu | What are the odds? | 4 | điều bất ngờ/lần đầu | [Reel 1491564896282973](https://www.facebook.com/reel/1491564896282973/) |
| 5 | 1,3 triệu | ?? | 0 | phản ứng/ngắn | [Reel 2924576621214886](https://www.facebook.com/reel/2924576621214886/) |
| 6 | 1,2 triệu | Wrong set up! | 3 | lỗi/thất bại/hiệu quả | [Reel 917407867803862](https://www.facebook.com/reel/917407867803862/) |
| 7 | 1,3 triệu | Lost it.. | 2 | lỗi/thất bại/hiệu quả | [Reel 2263594507733535](https://www.facebook.com/reel/2263594507733535/) |
| 8 | 2,2 triệu | which species? | 2 | nhận diện/ước lượng | [Reel 27770037856008456](https://www.facebook.com/reel/27770037856008456/) |
| 9 | 1,7 triệu | Gained trust and took it! | 5 | hành vi/quyết định của cá | [Reel 1734984214462191](https://www.facebook.com/reel/1734984214462191/) |
| 10 | 1,1 triệu | Tell me what this is? | 5 | nhận diện/ước lượng | [Reel 4070974076538960](https://www.facebook.com/reel/4070974076538960/) |
| 11 | 1,5 triệu | Almost 2 hookbaits in 1 go! | 6 | hành vi/quyết định của cá | [Reel 942242742269280](https://www.facebook.com/reel/942242742269280/) |
| 12 | 1,2 triệu | Do you think the pike intended to strike on the boilies? | 11 | hành vi/quyết định của cá | [Reel 2266809550760335](https://www.facebook.com/reel/2266809550760335/) |
| 13 | 1,1 triệu | Trying really hard.. | 3 | phản ứng/ngắn | [Reel 1431731452158829](https://www.facebook.com/reel/1431731452158829/) |
| 14 | 1,4 triệu | So many options and still grabs the hookbait | 8 | hành vi/quyết định của cá | [Reel 2008800996425095](https://www.facebook.com/reel/2008800996425095/) |
| 15 | 3,2 triệu | Why did we lose it? | 5 | lỗi/thất bại/hiệu quả | [Reel 2660382767709230](https://www.facebook.com/reel/2660382767709230/) |
| 16 | 1,6 triệu | What are these strings on the bottom? | 7 | nhận diện/ước lượng | [Reel 1054086407368423](https://www.facebook.com/reel/1054086407368423/) |
| 17 | 3,4 triệu | Do you fish tigers? | 4 | lựa chọn/thảo luận kỹ thuật | [Reel 1388103036613085](https://www.facebook.com/reel/1388103036613085/) |
| 18 | 4,7 triệu | Guess the name of the rig | 6 | nhận diện/ước lượng | [Reel 2426590164498757](https://www.facebook.com/reel/2426590164498757/) |
| 19 | 1,5 triệu | How to no pre bait.. | 5 | lỗi/thất bại/hiệu quả | [Reel 1423438146553483](https://www.facebook.com/reel/1423438146553483/) |
| 20 | 1,6 triệu | How cautious is this pike? | 5 | hành vi/quyết định của cá | [Reel 1437761371545234](https://www.facebook.com/reel/1437761371545234/) |
| 21 | 3,5 triệu | First even chod take! | 4 | điều bất ngờ/lần đầu | [Reel 1336992098521390](https://www.facebook.com/reel/1336992098521390/) |
| 22 | 1,4 triệu | Why we lost it? | 4 | lỗi/thất bại/hiệu quả | [Reel 1662821224779771](https://www.facebook.com/reel/1662821224779771/) |
| 23 | 1,1 triệu | Too much bait? | 3 | lựa chọn/thảo luận kỹ thuật | [Reel 1373884291601096](https://www.facebook.com/reel/1373884291601096/) |
| 24 | 1,3 triệu | When it isn't your day... | 5 | phản ứng/ngắn | [Reel 1022041354148399](https://www.facebook.com/reel/1022041354148399/) |
| 25 | 1,8 triệu | Watch lead drop off! | 4 | chỉ dẫn quan sát | [Reel 2162948884649039](https://www.facebook.com/reel/2162948884649039/) |
| 26 | 1,4 triệu | How big? | 2 | nhận diện/ước lượng | [Reel 1006304398889739](https://www.facebook.com/reel/1006304398889739/) |
| 27 | 1,6 triệu | How your hookpull looks underwater! | 5 | lỗi/thất bại/hiệu quả | [Reel 1744445353417549](https://www.facebook.com/reel/1744445353417549/) |
| 28 | 1,3 triệu | So attractive but ineffective too | 5 | lỗi/thất bại/hiệu quả | [Reel 2060713144532687](https://www.facebook.com/reel/2060713144532687/) |
| 29 | 1,6 triệu | At what point does the carp notice? | 7 | hành vi/quyết định của cá | [Reel 2123694768213226](https://www.facebook.com/reel/2123694768213226/) |
| 30 | 2,8 triệu | Which bait is it? | 4 | nhận diện/ước lượng | [Reel 1896009014692271](https://www.facebook.com/reel/1896009014692271/) |
| 31 | 1,5 triệu | Cheat code in fishing! | 4 | phản ứng/ngắn | [Reel 1785274112641394](https://www.facebook.com/reel/1785274112641394/) |
| 32 | 2,6 triệu | Match the hatch or something bright? | 6 | lựa chọn/thảo luận kỹ thuật | [Reel 2482087992203923](https://www.facebook.com/reel/2482087992203923/) |
| 33 | 6 triệu | Can you spot the jaw on the bottom? | 8 | chỉ dẫn quan sát | [Reel 1339627390996560](https://www.facebook.com/reel/1339627390996560/) |
| 34 | 2,7 triệu | Where is the carp feeding on? | 6 | chỉ dẫn quan sát | [Reel 1649832629433289](https://www.facebook.com/reel/1649832629433289/) |
| 35 | 1,1 triệu | What is the pike doing?? | 5 | hành vi/quyết định của cá | [Reel 3504702036345530](https://www.facebook.com/reel/3504702036345530/) |
| 36 | 1,7 triệu | Would you dare to place a rig so close to a catfish? | 12 | lựa chọn/thảo luận kỹ thuật | [Reel 1014710797727548](https://www.facebook.com/reel/1014710797727548/) |
| 37 | 1,2 triệu | Too heavy? | 2 | lỗi/thất bại/hiệu quả | [Reel 1560847245655274](https://www.facebook.com/reel/1560847245655274/) |
| 38 | 1,4 triệu | How a catfish feeds! | 4 | hành vi/quyết định của cá | [Reel 1028452793245110](https://www.facebook.com/reel/1028452793245110/) |
| 39 | 1,2 triệu | Do you fish tight lines? | 5 | lựa chọn/thảo luận kỹ thuật | [Reel 2125839318342324](https://www.facebook.com/reel/2125839318342324/) |
| 40 | 1,4 triệu | Coots in the alps! | 4 | phản ứng/ngắn | [Reel 1365548942104872](https://www.facebook.com/reel/1365548942104872/) |

## Kiểm tra và kết luận được phép

- 40 ID khác nhau, đều có nhãn view >1 triệu trong 130 ô nguồn đã ghi.
- 40 caption có nội dung hiển thị, bao gồm 1 chỉ dấu câu; 2 Reel không hiện caption được lưu riêng trong corpus và không tính vào mẫu chữ.
- Có 42 screenshot nguồn. Thống kê tính lại từ corpus, không gán 40 lượt xem trọn video.
- Không có đủ cơ sở chứng minh nguyên nhân viral, hiệu quả caption của Underwater hoặc quy tắc cho toàn hệ thống. Không tự publish nghiên cứu/ảnh lên GitHub hoặc đổi VERSION.

## Quyết định sau nghiên cứu

2026-10-16: người dùng chọn áp dụng phong cách qua UF-D015 và giữ hashtag; UF-D016 loại #Underwater. Phần quan sát/thống kê và các đề xuất trước đó ở trên được giữ để truy vết, không ghi đè quy chuẩn hiện hành tại audience-and-caption.md. Bản GitHub chỉ gồm nghiên cứu/corpus văn bản; ảnh giao diện, captions-raw và evidence-manifest được giữ local. Không kết luận hiệu quả của Underwater đã được chứng minh.
