# Hướng dẫn tạo Reel câu cá dưới nước bằng AI: khung đầu, video 10 giây và caption

**Phiên bản hướng dẫn:** 1.9 — cập nhật ngày 15/10/2026 (Asia/Saigon). Đây là phiên bản của tài liệu giao việc, không phải chứng nhận format đã được kiểm chứng viral hoặc mọi bản render đã đạt.

**Dùng cho:** AI viết prompt phục vụ Gemini Omni Flash; video dọc **9:16, đúng 10 giây**, khán giả câu cá Mỹ; chọn **Redfish (red drum), Muskie (muskellunge), Walleye hoặc một loài cá được câu tại Mỹ khác phù hợp** làm cá chính theo lựa chọn của người dùng. Tài liệu này tự đủ để thực hiện công việc khi không có lịch sử chat hoặc các file nghiên cứu đi kèm.

**Đầu ra cho mỗi video:** đúng ba mục tiếng Anh, hoàn chỉnh và dùng được ngay: **FIRST FRAME PROMPT**, **OMNI FLASH VIDEO PROMPT**, **CAPTION**. Caption gồm câu mở đầu ngắn gây tò mò, tự nhiên với người Mỹ thích câu cá theo phong cách kênh tham chiếu **và 3–5 hashtag viết liền trong cùng một đoạn, không xuống dòng**. Prompt first frame dùng cho model tạo ảnh bất kỳ; prompt video dùng với chính ảnh đó làm khung mở đầu trong Omni Flash. Không tự tạo media hoặc khẳng định đã render khi yêu cầu chỉ là viết prompt.

## 0. Bắt đầu ở đây: mục tiêu, bằng chứng và cách làm việc

### 0.1. Nhiệm vụ khi nhận riêng file này

Đọc toàn bộ tài liệu, hiểu câu chuyện và lập trạng thái mở đầu trước khi viết. Mục tiêu là footage mô phỏng có cảm giác camera thật đang quan sát một tương tác hợp sinh thái ở Mỹ. Ưu tiên theo thứ tự: **đúng loài/địa điểm và quan hệ vật lý → nhất quán giữa ảnh đầu và video → sự kiện rõ trong 10s → hình ảnh hấp dẫn → caption**. “Siêu thực” ở đây nghĩa là photorealistic, không phải kỳ ảo.

Đừng chỉ nhắc lại nguyên tắc, đưa ra kế hoạch rồi dừng hoặc yêu cầu người dùng tự ghép prompt. Sau khi đã có lựa chọn loài hoặc được giao quyền chọn loài, đầu vào ngắn vẫn phải được phát triển thành một ý tưởng mới và một bộ ba hoàn chỉnh. Trường hợp chưa biết người dùng muốn loài nào phải hỏi theo quy tắc ngay dưới, chưa tự tạo bộ prompt. Không in suy luận nội bộ; dùng kết quả kiểm tra để sửa sản phẩm trước khi trả.

**Chọn loài trước khi sáng tạo:** đọc yêu cầu và ngữ cảnh hiện có. Nếu người dùng đã chọn loài, cung cấp ý tưởng xác định loài hoặc giao rõ quyền chọn một cá được câu ở Mỹ, dùng thông tin đó và không hỏi lại. Nếu chưa có thông tin này, sau khi đọc hướng dẫn **chỉ hỏi một câu rồi chờ trả lời**:

> Bạn muốn làm video về Redfish, Muskie, Walleye, hay để mình chọn một loài cá được câu bất kỳ ở Mỹ?

Bốn lựa chọn là **Redfish / Muskie / Walleye / Loài cá được câu bất kỳ ở Mỹ**. Người dùng cũng có thể nhập tên một loài cụ thể khác được câu ở Mỹ. Không mặc định Redfish; không tự chia ba video cho ba loài khi người dùng chưa chọn hoặc chưa giao quyền lựa chọn. Quy tắc hỏi này là bước lấy đầu vào, không phải sản phẩm cuối; chưa xuất ba mục prompt/caption khi còn chờ lựa chọn.

**Cách hiển thị câu chọn loài — ưu tiên đáp án bấm được khi có hỗ trợ:**

- Nếu giao diện AI có công cụ hỏi người dùng bằng lựa chọn tương tác, dùng **một câu hỏi, chọn một đáp án**, với bốn đáp án: **Redfish**, **Muskie**, **Walleye**, **Loài cá được câu bất kỳ ở Mỹ**; cho phép nhập tên loài khác hoặc thông tin bổ sung bằng ô văn bản nếu công cụ hỗ trợ. Ví dụ, công cụ `request_user_input_async` có thể nhận bốn suggested options; chỉ dùng khi thực sự có trong phiên. Nếu giao diện tự có ô nhập khác, không cần thêm một đáp án “Khác” trùng chức năng.
- Nội dung câu hỏi vẫn dùng câu tiếng Việt ở trên. Không đánh dấu một loài là “khuyến nghị” hoặc coi đáp án được chọn sẵn trên giao diện là ý kiến người dùng. **Chỉ tiếp tục sau khi người dùng gửi câu trả lời**; không tự chọn khi chưa có phản hồi. Nếu người dùng đã chọn loài/giao quyền trong ngữ cảnh thì bỏ qua bước hỏi, không mở bảng lựa chọn lần nữa.
- Nếu giao diện không có lựa chọn tương tác, hoặc giới hạn số đáp án không đủ bốn, hiển thị cùng một câu hỏi kèm danh sách `1. Redfish; 2. Muskie; 3. Walleye; 4. Loài cá được câu bất kỳ ở Mỹ`, rồi ghi: `Bạn có thể trả lời số, tên cá, hoặc nhập một loài cá khác được câu tại Mỹ.` Chờ trả lời như trên. Không cắt mất một lựa chọn để vừa công cụ, không giả làm nút bấm bằng link Markdown và không tạo trang web chỉ để hỏi loài.
- File Markdown là hướng dẫn dùng giao diện, **không tự tạo được nút chọn trên mọi AI**. Luôn có phương án nhập chữ. Quy tắc này áp dụng khi bắt đầu tạo một video mới thiếu loài; việc nghiên cứu, sửa chính tài liệu hướng dẫn hoặc sửa clip đã rõ loài không kích hoạt câu hỏi chọn cá.

Nếu chọn **“Loài cá được câu bất kỳ ở Mỹ”**, người dùng đã giao quyền chọn: AI tự chọn một loài và vùng/thủy vực Mỹ phù hợp, nêu rõ tên loài trong prompt, rồi triển khai luôn, không hỏi tiếp “cụ thể loài nào?”. Không xem Redfish là lựa chọn tự động cho phương án này. Ba loài trong bảng mục 2 là cơ sở tham khảo, không phải giới hạn danh sách; với loài khác, nghiên cứu đúng nhận dạng, phân bố, sinh cảnh, con mồi và tập tính của loài đó, không sao chép máy móc hồ sơ của ba loài cũ.

Nếu người dùng không nêu số lượng, mặc định làm **một bộ**. Sau khi đã biết loài/quyền chọn loài, thiếu địa điểm/mùa thì tự chọn bối cảnh phổ thông có cơ sở, không bịa tên điểm câu. Những kích thước, khoảng nhìn hoặc độ sâu tự chọn là thông số dàn cảnh hợp lý, không phải phép đo thực địa. Ngoài câu chọn loài bắt buộc khi thiếu, chỉ hỏi thêm khi có mâu thuẫn quan trọng không thể tự giải quyết mà vẫn giữ ý định người dùng; các lựa chọn thông thường tự xử lý.

### 0.1a. Mỗi lần yêu cầu tạo mới phải có một ý tưởng sáng tạo mới phù hợp

- Không coi việc nhận file là lệnh lặp một ví dụ. Khi loài đã rõ, **tự phát triển một câu chuyện nguyên bản cho lần yêu cầu này**, thay vì mặc định Redfish–cua, Muskie–perch hoặc một tình huống mẫu khác. Ví dụ nghiên cứu/thử nghiệm trong file là tài liệu học, không phải kịch bản mặc định.
- Trước khi chọn, cân nhắc vài hướng khác nhau về mồi/con mồi hoặc sinh vật tương tác, kiểu tương tác, địa hình vi mô, key/twist và kết cục; chọn một hướng mới mà vẫn đúng sinh thái/vật lý. Không xuất danh sách ý tưởng thay cho bộ ba cuối trừ khi người dùng yêu cầu brainstorm.
- Đối chiếu những ý tưởng có trong lịch sử chat hoặc danh sách người dùng cung cấp. Khi có cảnh cũ để so, thay đổi có ý nghĩa ít nhất **hai yếu tố**, trong đó có **key/twist, kiểu tương tác hoặc kết cục**; chỉ đổi màu mồi, tên địa điểm, thời tiết, caption hoặc timecode không đủ tạo ý tưởng mới. Nếu một yếu tố được người dùng khóa, giữ nó và sáng tạo ở phần còn lại.
- Khi không có lịch sử, tránh dùng lại nguyên các ví dụ trong file, tự dựng một cơ chế câu chuyện mới; không tự nhận nhớ hoặc bảo đảm chưa từng làm ý tưởng đó ở một phiên không truy cập được. Không bắt người dùng cung cấp lịch sử mới bắt đầu.
- Nếu làm nhiều video, mỗi bộ cần key/câu chuyện riêng, không đổi tên loài rồi giữ nguyên mọi hành động. Với lựa chọn cá bất kỳ, có thể thay loài giữa các lần/bộ theo ngữ cảnh có sẵn; không ép đa dạng bằng cách chọn loài hoặc tương tác sai vùng.
- Quy tắc ý tưởng mới áp dụng khi **tạo video/bộ prompt mới**. Nếu người dùng yêu cầu sửa, tối ưu hoặc tiếp tục một clip đã chọn, giữ câu chuyện/loài đã duyệt và chỉ sửa đúng phạm vi; không tự đổi sang ý tưởng khác. Redfish–cua vẫn được dùng khi người dùng yêu cầu rõ hoặc có diễn biến mới thực sự phù hợp, nhưng không phải lựa chọn mặc định.


### 0.2. Nghiên cứu nền: đã làm gì, biết được gì

**Nguồn nền được cung cấp:** [báo cáo 20 Reel Underfishing](https://drive.google.com/file/d/1gDUVVbi5IJ9GUxaQetKA30wkkWhhSPjs/view?usp=sharing), khảo sát ngày 14/10/2026. Báo cáo ghi nhận 20 Reel có nhãn view trên một triệu trong danh sách Facebook tải được, xem ở các mốc đầu/giữa/gần cuối. Các nhãn view được làm tròn, không phải unique viewers, không phải top 20 toàn kênh; tuổi bài, retention và nguồn traffic chưa biết. **Khuyến nghị AI đọc toàn bộ báo cáo qua link trước khi phát triển ý tưởng nếu có khả năng truy cập. Đọc để hiểu và phát triển sáng tạo, không bị giới hạn bởi các nghiên cứu này:** học cơ chế gây tò mò, cấu trúc hành động và dấu vết vật lý; có thể đề xuất tình huống, nhịp kể và twist mới ngoài các mẫu, miễn đúng loài, địa điểm và vật lý. Không biến báo cáo thành danh mục kịch bản duy nhất hoặc trần sáng tạo. Những kết luận cần dùng vẫn được tóm tắt trong file này; nếu link không truy cập được, dùng phần tóm tắt và không tự nhận đã đọc bản đầy đủ.

**Tóm tắt đủ dùng:** camera thấp và gần như cố định; cá/mồi cùng một không gian; đối tượng xa giảm tương phản; một sự kiện nhỏ đổi trạng thái của mồi/cá/dây; hậu quả nhìn thấy; caption ngắn mời người câu phán đoán. Báo cáo nền ghi trung vị khoảng 10,6 giây, 12/20 mẫu dưới 11 giây. Đây là lý do chọn thử 10s, không chứng minh độ dài tối ưu. Hành vi tiếp cận rồi bỏ qua hoặc kết cục bị che cũng hợp format; không buộc mọi video có cú ăn.

| Mẫu nguồn để hiểu cơ chế | View ghi trong hồ sơ nền | Điều học, không phải kết luận nhân quả |
|---|---:|---|
| [Rig và cá ở rất gần](https://www.facebook.com/reel/2426590164498757/) | 4,7 triệu | Cơ cấu nhỏ đủ rõ để đặt câu hỏi chuyên môn, có lý do quan sát lại. |
| [Cá chép và mồi tigers](https://www.facebook.com/reel/1388103036613085/) | 3,4 triệu | Mồi–miệng–dây có quan hệ thấy được; đổi thức ăn/hành vi khi chuyển loài. |
| [Vì sao mất cá](https://www.facebook.com/reel/2660382767709230/) | 3,2 triệu | Kết quả bất định và dấu vết có thể tạo câu hỏi; không tự chẩn đoán lỗi rig. |
| [Nhận diện cá da trơn](https://www.facebook.com/reel/27770037856008456/) | 2,2 triệu | Cá hiện dần rồi đến rất gần; nhận dạng và tỷ lệ tạo tò mò. |
| [Mồi/rig cạnh miệng cá](https://www.facebook.com/reel/1614261063381636/) | 1,7 triệu | Sự kiện thị giác có thể kể chuyện mà không cần caption giải thích dài. |
| [Râu cá ở cận cảnh](https://www.facebook.com/reel/1054086407368423/) | 1,6 triệu | Chi tiết sinh học nhìn được phù hợp một câu hỏi ngắn. |

**Âm thanh và thử nghiệm kế thừa:** hồ sơ ngày 15/10/2026 ghi nhận bốn MP4 do người dùng cung cấp: *Do you fish tigers?*, *Guess the name of the rig*, *Love the snowman!!*, *which species*. Hồ sơ mô tả trích frame, tách AAC, xem phổ và đo biên độ từng cửa sổ 0,5s; các số đo được giữ ở mục 5. Lần biên tập này không đo lại các MP4. AI nhận file sau không được tự nhận đã nghe/xem các tệp đó nếu chưa thực sự truy cập. Các nhận xét về hai clip AI Redfish–cua trong mục 1 cũng là kết quả thử nghiệm kế thừa, không phải bài kiểm tra do mọi AI nhận file tự thực hiện.

Phân biệt bốn loại thông tin: **quan sát trong hồ sơ nền**, **sự kiện sinh học có nguồn**, **giả thuyết hấp dẫn/viral**, **quyết định sáng tạo cho kênh mới**. Không biến giả thuyết thành số liệu thực nghiệm. Trích phổ/biên độ không đủ xác định âm sắc, vật phát tiếng hoặc sự có mặt/vắng mặt của nhạc. Nhãn Original audio cũng không chứng minh cách thu âm.

### 0.3. Quy trình nghiên cứu trước khi soạn mỗi bộ prompt

1. **Chốt loài và ý tưởng mới:** áp dụng bước chọn loài ở 0.1; thiếu lựa chọn loài/quyền chọn thì hỏi bốn phương án và chờ. Khi đã có, phát triển câu chuyện mới theo 0.1a, rồi chốt một loài chính, vùng Mỹ/kiểu thủy vực, một mồi/con mồi, một key moment và một kết cục. Không mặc định Redfish–cua.
2. **Đối chiếu sinh thái và điều kiện nước:** xác định vùng/kiểu thủy vực, loài, mùa/giờ/thời tiết, độ sâu, nền đáy, dòng chảy/thủy triều và con mồi. Nghiên cứu riêng **màu nước và nguyên nhân**, **độ trong/tầm nhìn ngang**, loại/phân bố vật chất trong nước, lớp vật liệu mịn ở đáy và khả năng bị tái huyền phù. Xét biến thiên theo mưa, gió, dòng chảy và triều, không lấy màu mặt nước hoặc một ảnh nước trong đẹp làm đại diện cho cả thủy vực. Ưu tiên tài liệu khoa học, cơ quan môi trường/FWC/TPWD/DNR/NOAA và media dưới nước có thông tin điều kiện quay. Phần “Nghiên cứu và tái hiện môi trường nước chân thực” ở mục 2 quy định chi tiết cách dùng dữ liệu/giả định.
2a. **Nếu có dụng cụ câu:** lập hồ sơ mồi–móc–dây–leader–rig–phương pháp theo mục 2A; đối chiếu loài, kích thước cá/mồi, nước ngọt/lợ/mặn, bang/thủy vực, mùa và quy định hiện hành. Chốt một bộ khả thi, không ghép đồ câu của các phương pháp khác nhau. Nếu là săn mồi tự nhiên thì ghi rõ không có dụng cụ câu. Đây là bước tự nghiên cứu, không bắt người dùng điền toàn bộ thông số.
3. **Đọc nghiên cứu để phát triển sáng tạo:** khuyến nghị mở báo cáo 20 Reel qua link ở 0.2 để hiểu cơ chế trước khi thiết kế. Chọn một hoặc hai ví dụ làm điểm xuất phát, tách quan sát khỏi giả thuyết viral, rồi phát triển twist/hành động mới phù hợp loài Mỹ. Không bị giới hạn trong các cảnh, kết cục, mồi hoặc nhịp của báo cáo. Không dùng lại footage, logo hoặc chép caption đối thủ. Nếu không mở được link, dựa vào phần tóm tắt và các nguyên tắc trong file, tiếp tục làm việc trong giới hạn đã biết.
4. **Kiểm giới hạn truy cập:** nếu có trình duyệt/media thì quan sát đầu–giữa–cuối, kiểm caption gốc và nghe audio khi có công cụ. Nếu không, dùng hồ sơ nền với tư cách thông tin đã được cung cấp; không bịa view mới, số đo mới, nguồn hoặc câu “tôi đã xem/nghe”. Thiếu công cụ nghiên cứu không ngăn soạn bộ prompt từ bối cảnh đã có cơ sở.
5. **Thiết kế key rồi trạng thái:** chọn một twist, hành động cực nhanh hợp loài hoặc hành động/đổi trạng thái đủ tạo câu chuyện cho cả clip. Khóa thời điểm bắt đầu hành động key **sau 5.0s**, không ở hoặc trước 5.0s; phần đầu tạo hook/tò mò và tiến triển, phần sau còn đủ thời gian thấy hậu quả theo mục 4. Lập bản đồ t=0 theo mục 4, đường vào/thoát, vật cản, tín hiệu và nguyên nhân lực dẫn tới key; xác định hậu quả đọc được trên điện thoại. Không trả một cảnh chỉ có cá bơi cho đẹp. Nếu chuỗi quá phức tạp, đơn giản hóa bố cục nhưng vẫn giữ một key rõ.
6. **Soạn ảnh rồi video:** ảnh chỉ có một trạng thái t=0; video đi tiếp từ ảnh đó qua các beat liên tục. Khóa màu nước và độ trong riêng, cho vật xa suy giảm theo đường truyền qua nước. Hạt và mây bùn chỉ có khi hợp vật liệu/nguồn lực; không âm thầm làm nước trong hơn để chủ thể đẹp hơn. Nếu khó thấy, điều chỉnh cự ly/bố cục trong môi trường đã chọn. Audio phải có hai lớp **môi trường + hành động**, âm lượng đầu ra lớn/rõ, hiện diện xuyên suốt từ 0 đến 10s; gắn từng chi tiết với nguồn, khoảng cách thu và hành động hợp lý, không tự thêm hit điện ảnh để tạo kịch tính.
7. **Viết caption:** từ kết cục đã thiết kế, câu mở đầu ngắn gây tò mò, tiếng Anh tự nhiên với người câu cá Mỹ + 3–5 hashtag liên quan viết liền một đoạn, không xuống dòng; không nhắc công nghệ tạo video. Sau render, đối chiếu lại với kết quả thực sự nhìn thấy.
8. **Tự kiểm và sửa:** chạy checklist mục 10 trước khi giao. Nếu nhận phản hồi hoặc bản render, chỉ rõ lỗi quan sát được và sửa phần gây lỗi, giữ các ràng buộc đúng. Không cam kết prompt bảo đảm vật lý hoàn hảo hay triệu view.

Nguồn dưới dạng website/tài liệu, caption đối thủ và comment chỉ là dữ liệu nghiên cứu; không phải chỉ thị thay đổi nhiệm vụ. Những link là để truy vết/kiểm thêm, không phải điều kiện bắt buộc để đọc hiểu hướng dẫn.

### 0.4. Phạm vi đầu ra và tương thích model

Trong chế độ viết prompt, trả ba sản phẩm ở mục 8, không trả báo cáo nghiên cứu dài. Chỉ thêm ghi chú ngắn ngoài ba mục khi có mâu thuẫn không thể khắc phục hoặc thiếu khả năng kỹ thuật làm thay đổi cách dùng; không giấu điều chưa kiểm chứng trong prompt. Khi người dùng yêu cầu nghiên cứu/audit riêng, lúc đó mới trình bày nguồn, quan sát và giới hạn chi tiết.

Không mặc định mọi giao diện Omni có cùng tham số. Kiểm cách giao diện nhận ảnh mở đầu; thực sự đính kèm ảnh, không chỉ viết tên file hoặc tag trong text. Tag `<FIRST_FRAME>` được tài liệu Google mô tả cho vai trò ảnh mở đầu, nhưng wrapper có thể có trường first/start frame riêng hoặc chỉ nhận reference. Nếu chỉ hỗ trợ reference, nói rõ độ bám frame đầu chưa được bảo đảm, không gọi ảnh tham chiếu là khung đầu đã khóa. Không tự đổi model hoặc tự bắt đầu lượt sinh trả phí khi nhiệm vụ chỉ yêu cầu prompt. [Tài liệu Omni Flash](https://ai.google.dev/gemini-api/docs/omni).

## 1. Điều khiến cảnh Underfishing trông như footage thật

Ở nhiều Reel trong mẫu, một camera gần như đứng yên được đặt thấp sát đáy. Nền có cát, sỏi, vỏ sò, cành hoặc cỏ không được xếp ngay ngắn. Mồi và cá cùng nằm trong một không gian nhìn được; cá có thể mờ hơn ở xa rồi rõ dần khi tới gần. Khi miệng, thân hoặc dây chạm đáy, bùn chỉ nổi từ vị trí bị tác động; nó có thể che đúng khoảnh khắc quyết định. Các vật còn lại tiếp tục ở nguyên chỗ. Đó là các dấu hiệu của **một máy quay đang chứng kiến sự việc**, không phải một chuỗi ảnh minh họa đã được dựng.

Các Reel [“How to lose a fish…”](https://www.facebook.com/reel/1135811299007293/), [“Lost it…”](https://www.facebook.com/reel/2263594507733535/) và [“Why did we lose it?”](https://www.facebook.com/reel/2660382767709230/) cho thấy kết quả nằm ở mồi, dây và đám bùn sau cú tiếp xúc. Các Reel [“??”](https://www.facebook.com/reel/2924576621214886/) và [“Do you think the pike will go for the boilies?”](https://www.facebook.com/reel/2266809550760335/) còn giữ sự tò mò khi cá tiến gần mà không cắn. Vì thế **không cần một cú tấn công phi lý trong mọi video**. Một cú bỏ qua mồi, hụt, nhả hoặc bị cỏ che vẫn có câu chuyện nếu khung đầu đặt ra được một câu hỏi rõ.

Chuyển công thức này sang ba loài Mỹ bằng cách giữ **góc máy, thời gian quan sát, một sự kiện và dấu vết vật lý**; thay toàn bộ cá, mồi, đáy, ánh sáng và hành vi theo sinh thái của loài. Không đem boilie/pop-up câu chép châu Âu đặt vào mọi cảnh của redfish, walleye hoặc muskie.

### Bài học từ clip AI thử nghiệm Redfish–cua dài 10 giây

Clip thử đã làm đúng ba việc: khung đầu có cả cá và cua, môi trường nông có hàu phù hợp, và bùn nổi gần vị trí cua lùi đi vào khoảng giây 7. Tuy vậy, cua gần như giữ nguyên tư thế trong nhiều giây khi cá đã áp sát; cú rút vào hốc hàu quá đột ngột để thấy chân tạo lực; cả cá và cua đều được trình bày quá rõ, quá đẹp như một cảnh được dàn trước. Đoạn kết chỉ cho thấy cua khuất khỏi khung, **không chứng minh cá đã bắt được cua**. Tệp xuất còn có một biểu tượng hình thoi dễ nhận ở góc phải dưới. Đây là **bài kiểm tra đầu ra**, không phải bằng chứng rằng mọi clip AI sẽ mắc cùng lỗi.

Rút thành bốn ràng buộc áp dụng cho mọi loài: **(1)** con mồi có phản ứng quan sát được trước biến cố, dù chỉ là dừng, đổi hướng hoặc thủ thế; **(2)** hành động mạnh có bước chuẩn bị tạo lực, đường đi liên tục và vật bị tác động đi tới một nơi xác định; **(3)** ảnh có lớp sâu, che khuất và chi tiết không đều theo môi trường, không phải hai “nhân vật” đều sáng nét hoàn hảo; **(4)** caption chỉ nói kết quả nhìn thấy. Nếu ảnh/video có biểu tượng hoặc chữ chèn ngoài cảnh, đánh dấu ở khâu kiểm đầu ra; prompt “no logo” đơn thuần không bảo đảm loại được dấu do nền tảng chèn.

### Bài học từ clip Redfish–cua thử nghiệm tiếp theo

Ở bản 10 giây tiếp theo, nước nâu lục, bùn/vỏ hàu không đều và độ rõ giữa gần–xa tự nhiên hơn; biểu tượng góc phải của bản trước không thấy trong các khung đã kiểm. Cá đi từ trái vào; cua giữ thế càng gần như nguyên vẹn suốt khoảng 0–6 giây, dù cá đã tiến gần. Khoảng 7–8,5 giây cua mới chạy ra phía phải, sau đó khuất khỏi khung; cá không bắt được cua trong phần hình nhìn thấy. Cảnh vẫn đọc được nhưng **phần đầu thiếu tiến triển ở con mồi** và **đích thoát bị lẫn giữa hốc hàu với mép khung**. Bài học: bố trí **5–8 beat linh hoạt** theo diễn biến, mỗi beat có một biến đổi nhỏ có thể chỉ ra, không ép beat bằng nhau hoặc buộc mọi động tác dài 1,5–2,5 giây; khóa rõ con mồi sẽ lùi vào hốc nào hay thoát qua mép nào, và cho nó phản ứng trước khi mõm cá sát thân. Đánh giá này dựa trên khung hình; luồng âm thanh của bản mới chưa được giải mã đủ để kết luận về âm sắc hoặc mức xung.

## 2. Môi trường phải khớp cả năm biến cùng lúc

Mỗi ý tưởng cần khóa một địa điểm có thật ở mức **vùng và kiểu thủy vực**, không cần bịa tên hồ/lạch cụ thể; rồi khóa năm biến: **độ sâu — nền đáy — độ trong — nguồn sáng — dòng chảy**. Nếu đổi một biến, kiểm lại bốn biến còn lại.

### Nghiên cứu và tái hiện môi trường nước chân thực

**Mục tiêu:** ảnh first frame phải giống hình ảnh một máy quay thực sự được đặt chìm tại địa điểm đã chọn có thể ghi lại. Ưu tiên tính đúng của môi trường, quang học và vật lý; không tự làm nước trong hơn, ánh sáng đẹp hơn hoặc chủ thể sắc nét hơn chỉ để tạo ảnh hấp dẫn.

#### 1. Nghiên cứu điều kiện thực tế trước khi viết prompt

AI phải xác định vùng địa lý, kiểu thủy vực, độ sâu, nền đáy, mùa, thời điểm, thời tiết và trạng thái dòng chảy hoặc thủy triều nếu có. Từ đó nghiên cứu:

- Nước thực tế thường có màu gì và vì sao: vật chất hữu cơ hòa tan, phù sa, tảo, vật liệu đáy hoặc các yếu tố khác.
- Độ trong biến thiên thế nào theo mưa, gió, dòng chảy, thủy triều và điều kiện tại thời điểm được chọn.
- Trong nước có những gì: hạt trầm tích lơ lửng, mảnh hữu cơ, tảo, vụn thực vật hoặc các thành phần phù hợp khác. Không mặc định nước tự nhiên luôn có rác, bong bóng hoặc nhiều hạt nhìn thấy.
- Nền đáy là bùn, sét, cát, sỏi, đá hay hỗn hợp; có lớp trầm tích mịn phủ trên bề mặt hay không.
- Chuyển động của con vật có thể tác động tới nền đáy, cây thủy sinh và nước xung quanh như thế nào.

Ưu tiên nguồn khoa học, cơ quan môi trường và hình ảnh/video dưới nước có thông tin địa điểm, điều kiện quay. Phân biệt hình ảnh quan sát được với diễn giải từ nguồn. Không lấy một ảnh nước trong đẹp làm đại diện cho toàn bộ thủy vực; không suy độ trong dưới nước chỉ từ màu mặt nước chụp trên bờ.

Nếu thiếu dữ liệu chính xác, chọn điều kiện có cơ sở phù hợp nhất và ghi rõ giả định trong ghi chú nghiên cứu. Không bịa số đo độ đục, tầm nhìn hoặc khẳng định đã kiểm chứng địa điểm. Các con số tự chọn để bố trí cảnh phải được xem là thông số dàn cảnh.

#### 2. Khóa màu nước và độ trong thành hai yêu cầu riêng

**Màu nước** là sắc nước trong điều kiện ánh sáng cụ thể. **Độ trong** là khả năng nhìn xuyên nước và nhận ra vật thể ở các khoảng cách khác nhau. Nước có màu không nhất thiết đục; phủ màu nâu hoặc xanh lên một cảnh rõ nét không tạo ra nước đục chân thực.

Prompt phải mô tả đồng thời:

- Sắc nước và nguyên nhân phù hợp.
- Mức độ, loại và phân bố của vật chất lơ lửng.
- Vật gần camera còn thấy những chi tiết nào.
- Vật xa mất chi tiết, tương phản và màu sắc đến mức nào.
- Hậu cảnh hòa dần vào nước như thế nào.

Sự suy giảm phải tăng theo đường truyền qua nước. Không cho chủ thể xa vẫn rõ từng chi tiết như ở sát ống kính. Không thay tán xạ trong nước bằng hiệu ứng xóa phông, làm mờ toàn ảnh hoặc một lớp sương phẳng.

Không chuyển trực tiếp số đo nhìn theo chiều sâu thành khoảng nhìn ngang của camera.

#### 3. Tạp chất và hạt lơ lửng phải có cơ sở

Chỉ thêm những thành phần hợp môi trường đã nghiên cứu. Hạt nhìn thấy cần có mật độ, kích thước, độ sáng và vị trí không đều; một số có thể nằm ngoài vùng nét hoặc quá nhỏ để phân biệt.

Không dùng lớp hạt trắng đồng đều như tuyết để biểu thị nước tự nhiên. Không tự thêm rác, bong bóng liên tục hoặc các mảnh vụn lớn để làm cảnh “thật hơn”. Nếu nước tương đối trong và ít hạt nhìn thấy, giữ đúng điều kiện đó.

#### 4. Bùn bị khuấy phải tuân theo nền đáy và nguồn lực

Không mặc định cứ con vật di chuyển mạnh là có mây bùn. AI phải xét:

- Đáy có vật liệu đủ mịn, rời và dễ tái huyền phù hay không.
- Con vật ở cách đáy bao xa.
- Vây, đuôi, thân, chân hoặc mõm có tiếp xúc nền hay tạo dòng nước đủ mạnh tới nền không.
- Hướng tác động và dòng chảy sẽ đưa vật liệu đi đâu.

Nếu điều kiện phù hợp, trầm tích phải bắt đầu nổi từ vùng thực sự bị tác động, sau tác động; sau đó lan, trôi và lắng theo vật liệu cùng dòng nước. Độ đục tăng cục bộ trước, không xuất hiện đồng loạt khắp khung. Đá và sỏi lớn không bay lơ lửng như bùn mịn.

Nếu con vật bơi cách xa đáy hoặc nền không có lớp vật liệu dễ bị khuấy, có thể không xuất hiện mây bùn. Không thêm bùn chỉ để tạo kịch tính.

**First frame chỉ thể hiện trạng thái tại t=0.** Không đặt sẵn mây bùn của một cú lao sẽ xảy ra trong video. Nếu đã có đám đục tại t=0, phải có nguyên nhân hợp lý và được xác định trong thiết kế cảnh.

#### 5. First frame phải tuân theo góc nhìn của máy quay thật

Xác định vị trí có thể đặt máy, độ cao so với đáy, hướng nhìn, góc ống kính và khoảng cách tới chủ thể. Những thông số này phải thống nhất với phối cảnh, tỷ lệ và mức nhìn thấy qua nước.

Ánh sáng phải đi qua mặt nước và môi trường đúng điều kiện đã chọn. Không tự thêm đèn rọi, vân nắng trong cảnh thiếu nắng trực tiếp hoặc ánh sáng làm mọi vật sáng rõ đồng đều.

Cho phép che khuất tự nhiên, bề mặt không đều và mất chi tiết theo khoảng cách. Không sắp chủ thể và con mồi như ảnh quảng cáo. Không dùng nhiễu, méo ống kính hoặc tối góc giả để che các sai lệch môi trường.

Nếu điều kiện nước khiến chủ thể khó nhìn, điều chỉnh khoảng cách hoặc bố cục hợp lý; không âm thầm làm nước trong hơn thực tế. Ảnh vẫn phải đọc được câu chuyện trong giới hạn mà máy quay tại vị trí đó có thể nhìn thấy.

#### 6. QA bằng ảnh thực tế, không bằng lời trong prompt

Sau khi sinh ảnh, đối chiếu lại với điều kiện đã nghiên cứu:

- Màu nước và độ trong có cùng hợp lý với địa điểm, ánh sáng và thời tiết không?
- Hạt lơ lửng, vật liệu đáy và lớp bùn có đúng loại, đúng mức không?
- Vật xa có mất chi tiết và tương phản theo khoảng cách không?
- Chủ thể có bị sắc nét, sáng hoặc bão hòa bất thường so với môi trường không?
- Có mây bùn, bong bóng hoặc tạp chất không có nguyên nhân không?
- Hình ảnh có giống góc nhìn từ một camera chìm thực sự, hay chỉ là cảnh rõ nét được phủ màu nước?

Nếu sai, sửa đúng thuộc tính gây lỗi rồi kiểm lại. **Không đánh dấu đạt chỉ vì ảnh đẹp, có màu nước phù hợp hoặc prompt đã ghi “photorealistic”.** Chỉ kết luận về những gì thực sự quan sát được; ghi rõ điểm chưa xác minh thay vì tuyên bố chính xác tuyệt đối.

**Cách ghi nhận nghiên cứu:** lưu nguồn/ngày truy cập và điều kiện nguồn nếu có; tách quan sát trực tiếp, diễn giải khoa học, giả định chọn cảnh và số dàn cảnh. Không bịa NTU, tầm nhìn hoặc việc kiểm chứng địa điểm. Ghi chú này là tóm tắt dữ kiện/giả định, không phải suy luận nội bộ phải xuất ra. Hợp đồng cuối vẫn có đúng ba sản phẩm; chỉ trình bày ghi chú nghiên cứu khi người dùng yêu cầu hoặc có giới hạn quan trọng cần thông báo ngắn. Khi không truy cập được nguồn mới, dùng cơ sở sẵn có đúng phạm vi, ghi rõ điều chưa xác minh và không tự nhận đã nghiên cứu hiện trường.

**Độ ưu tiên:** nếu một ví dụ hay mô tả thẩm mỹ khác trong file gợi ý thêm hạt, tăng độ rõ hoặc khuấy bùn nhưng điều kiện thực tế không hỗ trợ, áp dụng các quy tắc môi trường của mục này. Hạt không bắt buộc phải nhìn thấy; nước tự nhiên không bắt buộc đục. Nhịp key và độ hấp dẫn không được dùng để phủ nhận giới hạn nhìn thực của camera.

### Khóa môi trường tự nhiên và góc máy ngay trong first frame

First frame phải mô tả **đúng nơi con vật có thể sống**, không chỉ một phông nền dưới nước đẹp. Chọn và ghi rõ các chi tiết phù hợp cảnh:

- **Địa lý và không gian sống:** vùng Mỹ, hồ/sông/lạch triều/bãi cỏ biển/mép oyster, nước ngọt/lợ/mặn; độ sâu, độ dốc, khoảng mở giữa cá–mồi, vật che và đường di chuyển. Cây, vật liệu đáy, sinh vật phụ phải hợp cùng một hệ sinh thái và có tỷ lệ thật.
- **Mùa, giờ và thời tiết:** nêu một tổ hợp nhất quán, ví dụ đầu thu, chiều trời nhiều mây, gió nhẹ. Thời tiết phải được thể hiện bằng **hệ quả dưới nước** như ánh sáng tán xạ, dao động mặt nước, vân sáng hoặc độ đục có lý do; không bắt vẽ bầu trời hay hạt mưa rơi như trên cạn trong một khung hoàn toàn chìm. Không tự thêm bão, mưa, sóng hay bùn dày chỉ để tăng kịch tính.
- **Màu sắc đời thực:** màu thân/vây/đốm cá dưới nguồn sáng và đường đi ánh sáng trong nước; màu bùn, sỏi, cỏ, hàu và nước có độ biến thiên tự nhiên. Vật xa mất chi tiết/tương phản đúng môi trường; không dùng màu đỏ/cam bão hòa, teal–orange, HDR bóng bẩy hoặc nền xanh nhiệt đới cho mọi loài.
- **Camera ngoài đời:** mặc định một action-cam/camera quan sát dưới nước đặt cố định thấp ở vị trí có thể bố trí thật, với chiều cao, hướng nhìn và góc rộng vừa phải. Góc ngang/hơi chếch hợp khoảng cách và địa hình; phối cảnh tự nhiên, không canh cả cá và mồi như ảnh quảng cáo. Không mặc định góc máy điện ảnh, hero shot, góc bay, dolly, ánh sáng sân khấu, bokeh kịch tính hoặc camera đuổi theo cá. Chỉ dùng phong cách/góc điện ảnh khi người dùng yêu cầu rõ.

Giữ cùng tổ hợp môi trường/thời tiết/nguồn sáng từ ảnh t=0 sang video. Sự chân thực không có nghĩa phải làm ảnh tối hoặc bẩn quá mức: điểm key và mối quan hệ cá–mồi vẫn phải đọc được.


| Loài và cảnh hợp lý | Vật liệu thật trong khung | Nước và ánh sáng | Mồi/con mồi, kiểu tiếp cận | Dấu hiệu sai cần sửa |
|---|---|---|---|---|
| **Redfish:** rìa đầm mặn Louisiana/Texas; lạch thủy triều Florida; bãi cỏ biển, bùn hoặc mép oyster ở nước lợ/ven biển | Rễ/cọng cỏ mặn, bùn mịn, vỏ oyster không đều; cua/tôm/cá nhỏ; chỗ nước chảy quanh cỏ | Nông, hơi tannin hoặc phù sa; nắng tán qua mặt nước nếu ban ngày; cỏ đung đưa theo dòng | Cúi đầu dò đáy, có thể tailing; tiến tới cua/tôm hoặc jig thích hợp; đuôi khuấy bùn tại điểm đó | Hồ nước ngọt kiểu hồ núi; cá đỏ rực đồng nhất; ria cằm như black drum; spot đuôi chuyển chỗ giữa các frame |
| **Walleye:** hồ/sông ở Wisconsin, Minnesota hoặc vùng Great Lakes; điểm đá/sỏi, mép thảm cỏ | Sỏi đủ cỡ, tảng đá, ít cành/cỏ địa phương; minnow hoặc jig nhỏ ở độ cao hợp lý | Hoàng hôn/bình minh hoặc nước hơi đục; nếu giữa ngày và nước trong, cá thường ở sâu/tối hơn | Bơi dò tìm con mồi, áp sát và hút/đớp ngắn; đôi khi chỉ theo rồi bỏ | Bãi oyster nước mặn; chiếu sáng nhiệt đới giữa trưa trong veo; mắt phát sáng như đèn LED |
| **Muskie:** hồ mát/sông lớn miền Bắc; mép cỏ thủy sinh, gốc gỗ, gờ đá hoặc hố nước chậm | Bẹ cỏ “cabbage”, gỗ chìm/đá có kích thước thật; baitfish hoặc lure lớn phù hợp | Độ trong đủ để cá săn bằng thị giác; ánh sáng tự nhiên, vùng tối sau cỏ/gỗ | **Một** cá đơn độc núp/đi theo; tăng tốc một lần, đớp ngang con mồi hoặc hụt | Đàn nhiều muskie; hoa văn/vây biến thành northern pike; cá đứng bất động rồi dịch chuyển tức thời |

Đối chiếu nhận dạng và hành vi với [Texas Parks & Wildlife về red drum](https://tpwd.texas.gov/fishing/sea-center-texas/flora-fauna-guide/bays-and-estuaries/bay-animals/red-drum), [Florida FWC về red drum](https://myfwc.com/wildlifehabitats/profiles/saltwater/drums/red-drum/), [Wisconsin DNR về walleye](https://dnr.wisconsin.gov/sites/default/files/topic/Fishing/Species_walleye.pdf) và [Wisconsin DNR về muskie](https://dnr.wisconsin.gov/sites/default/files/topic/Fishing/Musky_MuskellungeFactSheet2012.pdf).

### Nước đục kiểu Underfishing: áp dụng khác nhau cho ba loài

**Nhận xét từ ảnh tham chiếu:** nhiều thumbnail có lớp nước xanh lục, xanh lam lẫn hạt, hoặc xám nâu; cá ở xa mờ và ít tương phản, trong khi miệng/mồi gần đáy còn đọc được. Có cảnh bụi đáy bùng **sau** khi cá quẫy. Đây là **độ đục cục bộ và có chiều sâu**, không phải phủ một lớp sương đồng nhất lên toàn màn hình. Thumbnail không đủ để suy ra độ đục đo bằng NTU hoặc độ sâu nhìn bằng đĩa Secchi.

| Loài | Độ đục có hợp sinh thái không? | Cấu hình cảnh nên dùng | Khi nào cần giảm độ đục |
|---|---|---|---|
| **Redfish** | **Có, rất hợp cho một số cảnh ven bờ.** Cửa sông pha nước ngọt–mặn có thể sẫm và đục; red drum thường kiếm ăn ở nước nông, nền bùn mềm, cỏ biển hoặc mép oyster. Nhưng không phải mọi bãi cỏ biển hay vùng redfish đều đục. | Lạch thủy triều/bãi bùn Louisiana hoặc Texas; nước lợ **nâu xanh/olive**, phù sa mịn lơ lửng, bùn chỉ bốc thêm khi đầu/đuôi chạm đáy. Ở gần camera thấy rõ mồi và đốm đuôi; cá xa là bóng đồng nâu nhạt, mép cỏ mờ dần. Nếu dùng mép oyster, giữ vỏ sắc nét trong tiền cảnh và mềm đi ở hậu cảnh. | Cảnh bãi cỏ biển Florida nắng đẹp hoặc nước nông rất trong; giảm lớp phù sa nền, vẫn giữ mất tương phản theo khoảng cách. |
| **Walleye** | **Có, ở mức vừa phải rất hợp.** Wisconsin DNR nói walleye ở nước trong thường trú sâu ban ngày và vào nông ban đêm; ở nước đục hơn có thể hoạt động cả ban ngày. Walleye cũng sống trong nhiều loại hồ, nên không bắt buộc nước đục ở mọi cảnh. | Hồ/sông phía bắc có nước **xanh rêu, nâu trà hoặc xám lục**; sỏi và jig rõ ở tiền cảnh, mép đá xa mềm và tối. Nước hơi đục hoặc ánh chiều tối tạo lợi thế thị giác cho cá, nhưng vẫn đủ để mắt, vây lưng và chóp trắng đuôi nhận ra khi cá tới gần. Có thể dùng bùn rất mịn ở khe sỏi; tránh đám bùn dày phủ cả bãi đá. | Hồ nước trong giữa ngày: đặt camera/cá sâu hơn hoặc dưới bóng cấu trúc; cảnh đêm/hoàng hôn có thể khá trong mà vẫn đúng loài. |
| **Muskie** | **Chỉ đục nhẹ đến vừa trong cảnh săn bằng mắt.** Wisconsin DNR mô tả muskie dựa nhiều vào thị giác và gặp khó hơn khi nước quá đục. Nó có thể ở hồ/sông với biến thiên độ trong; một lớp haze tự nhiên hợp lý, nhưng “súp bùn” kín tầm nhìn kém hợp cảnh nó phát hiện mồi từ xa và lao chính xác. | Hồ mát Wisconsin/Minnesota: nước **xanh lục dịu hoặc nâu trà trong vừa**, hậu cảnh mờ nhẹ, thảm cỏ và thân cá ở khoảng vài mét vẫn có bóng/hướng rõ. Đặt muskie núp sau cỏ/gỗ, mồi đi vào **tầm nhìn gần**, cú lao bắt đầu khi khoảng cách đã ngắn. Đám silt riêng chỉ nổi khi đuôi quét sát đáy hoặc vật va vào nền. | Nếu muốn mây đục dày như các Reel cá chép, đặt nó **sau cú lao** để che kết quả; không cho muskie khóa mồi ở xa qua nước đặc như sữa. |

Cơ sở: [Texas Parks & Wildlife về nước cửa sông thường sẫm/đục](https://tpwd.texas.gov/education/resources/aquatic-science/tas/chapters/chapter-6/) và [môi trường red drum](https://tpwd.texas.gov/huntwild/wild/species/reddrum/); [Wisconsin DNR về walleye trong nước trong/đục](https://dnr.wisconsin.gov/topic/Fishing/species/walleye.html); [Wisconsin DNR về muskie săn bằng thị giác và khó kiếm ăn hơn khi nước đục](https://dnr.wisconsin.gov/sites/default/files/topic/Fishing/Musky_MuskellungeFactSheet2012.pdf). [NOAA](https://repository.library.noaa.gov/view/noaa/44989/noaa_44989_DS1.pdf) giải thích hạt lơ lửng làm giảm tương phản và tầm nhìn ảnh dưới nước.

**Quy tắc dựng ảnh, không phải ngưỡng sinh học:** chọn khoảng nhìn *theo chiều ngang của camera* đủ cho câu chuyện. Ví dụ, với redfish cho mồi rõ trong ~0,3–0,7 m và cá chỉ thành bóng ở ~1,5–2 m; với walleye cho tiền cảnh rõ và cá mờ ở ~2–3 m; với muskie cho cá còn nhận được dáng ở ~2–4 m trước cú lao. Các khoảng này là **gợi ý bố cục để model sinh ảnh**, không phải số đo bắt buộc của hồ/sông, và **không được đổi thẳng từ độ sâu Secchi**. Nếu muốn nước đục hơn, kéo cá xuất hiện gần camera hơn; không giữ cá xa mà vẫn nhìn sắc như ảnh studio.

**Cách khóa môi trường trong prompt:** viết đủ sáu chi tiết theo thứ tự: `kiểu nước + nguồn đục + màu nền + mức nhìn xa + vật gần/vật xa + đám bùn phát sinh`. Ví dụ: “slightly tannic, sediment-bearing brackish creek water; olive-brown cast; shell and crab sharp within 50 cm, redfish silhouette soft at 1.5 m; a small local silt plume only after the tail brushes the mud.” Không dùng riêng từ “murky” vì model dễ phủ màn sương phẳng. Nếu có hạt lơ lửng nhìn thấy, chúng phải có phân bố phù hợp và không đều sáng như tuyết; màu nước, tán xạ và độ tương phản phải duy trì cùng trạng thái suốt shot trừ biến cố vật lý thấy được.

**Chống tiền cảnh quá sạch:** tiền cảnh đủ rõ để hiểu hành động, nhưng bùn có hạt mịn lẫn hạt thô, vỏ hàu/đá có mép mòn và mảng bám không đều, cỏ có lá gãy hoặc bị che một phần. Chỉ thêm hạt phù sa nhìn thấy khi hợp điều kiện nghiên cứu, ở các độ sâu khác nhau với kích cỡ/độ sáng khác nhau; một số hạt đi theo dòng rất chậm, không thành lớp hạt dày phủ đều. Tránh viền vật thể sắc như ảnh sản phẩm, bề mặt đồng nhất, sắp xếp vỏ/đá cân đối, ánh sáng rọi đều vào cả cá lẫn con mồi. Giữ chi tiết gần có chọn lọc; giảm độ rõ và tương phản của cá ở xa bằng tán xạ nước **ngay từ t=0**, không thêm màn sương toàn khung hoặc làm mờ giả toàn ảnh.

**Xếp ba lớp trong khung dọc 9:16:** (1) **tiền cảnh** 0–0,7 m: một mồi/con mồi, vài vật đáy đủ rõ để mắt người xem bám vào; hạt gần ống kính chỉ thêm nếu điều kiện nước hỗ trợ; (2) **trung cảnh** khoảng 0,7–2 m: đường cá đi vào hoặc chỗ cá núp, độ tương phản giảm nhẹ; (3) **hậu cảnh**: cỏ, đá, gốc gỗ hoặc bờ dần hòa vào màu nước, không dựng một “tường sương” phẳng. Số mét chỉ là gợi ý dàn cảnh. Với redfish thay hậu cảnh bằng rễ/cỏ mặn hay mép oyster; với walleye dùng bãi sỏi/gờ đá, bóng tối tăng ở xa; với muskie dùng mép thảm cỏ/gỗ chìm còn đủ hình dạng để cú phục kích đọc được. Nếu đã có mây bùn ở t=0, phải có nguyên nhân vừa xảy ra ngoài khung; mặc định bắt đầu bằng độ đục nền ổn định rồi mới thêm mây bùn từ hành động trong video.

### Chi tiết sinh học cần giữ ổn định

- **Redfish / red drum — *Sciaenops ocellatus*:** thân đồng ánh nâu đến bạc tùy nước, bụng nhạt, một hoặc nhiều đốm đen ở gốc đuôi; **không có râu cằm**. Đầu chúc xuống khi kiếm cua, tôm, giun biển hoặc cá nhỏ; đuôi có thể nhô trên mặt nước nông. Đừng vẽ răng nanh to ở miệng. Đốm đuôi là điểm nhận dạng cố định trên cùng một cá suốt video.
- **Walleye — *Sander vitreus*:** thân olive-vàng/đồng, bụng sáng, vây lưng trước có gai và đốm sẫm ở góc sau dưới; chóp trắng ở phần dưới vây đuôi. Mắt lớn phản sáng **khi có tia sáng tới đúng góc**, không tự phát quang. Cú đớp mồi của cá săn mồi phải diễn ra sau khi nó rút ngắn khoảng cách. Có thể có vài cá cùng khu vực, nhưng không cần dựng đội hình bơi đồng bộ.
- **Muskie — *Esox masquinongy*:** thân dài, mõm bẹt thuôn, hàm răng nhọn, vây lưng và vây hậu môn nằm lùi về gần đuôi; hoa văn vạch/đốm sẫm trên nền sáng biến thiên theo cá. Đừng trộn với pike có các đốm sáng trên nền sẫm. Muskie thường đơn độc, phục kích bên cỏ/gỗ/đá và lao ngắn có định hướng; không rỉa hạt mồi ở đáy kiểu cá chép.

## 2A. Mồi, móc, dây, rig, bẫy và phương pháp câu phải phù hợp loài tại Mỹ

### 2A.1. Chọn đúng loại tương tác trước, không tự thêm dụng cụ

Phân biệt **con mồi hoang dã**, **mồi tự nhiên dùng để câu** và **mồi giả**. Cua/tôm/cá nhỏ sống trong môi trường không mặc nhiên là mồi móc câu. Nếu câu chuyện chỉ là săn mồi tự nhiên, giữ nguyên lựa chọn đó: **không móc, không dây, không chì, không bẫy**. Nếu câu chuyện có câu cá, các vật dụng phải thuộc **một cấu hình có thật, phù hợp với loài, địa điểm, mùa và cách câu đã chọn**. Không buộc mọi clip phải có đủ tất cả đồ câu.

Trong tài liệu này, **rig** là bộ lắp dây–phụ kiện–móc/mồi; **lồng/bẫy thật** là thiết bị có cửa, khung/lưới và cơ chế giữ con vật. Không dịch mọi rig thành lồng bẫy. Cần câu/máy câu là nguồn lực ở ngoài khung nếu góc máy không thấy; không ép chúng xuất hiện dưới đáy để minh họa.

### 2A.2. Nghiên cứu bộ câu theo từng cảnh

AI tự hoàn thiện hồ sơ sau trước khi viết, không xuất thêm một mục thứ tư trong bộ ba đầu ra:

| Thông tin phải chốt | Yêu cầu |
|---|---|
| Loài, cỡ cá, vùng và cách câu | Tên loài chính xác; bang/thủy vực hoặc kiểu thủy vực có cơ sở; mùa; câu thả đáy, phao, jig, casting/retrieve, trolling, fly hoặc ice fishing khi hợp bối cảnh. Không đổi sang mùa băng chỉ để dùng tip-up. |
| Mồi | Chọn một loại cụ thể: tên con mồi tự nhiên và trạng thái sống/chết/cắt khúc; hoặc loại lure, kích thước, màu tự nhiên dưới nước và đặc tính chìm/nổi. Mồi sống phải được phép dùng tại đó; loài cùng xuất hiện trong tự nhiên chưa chắc được phép dùng làm bait. |
| Móc và điểm gắn | Single J-hook, circle hook, jig hook hay treble đúng cấu hình; số lượng, vị trí, hướng mũi/độ lộ mũi và tỷ lệ với mồi. Chốt cỡ móc theo đúng mẫu/nhà sản xuất khi cần; không dùng một cỡ cho cả ba loài. `#4` khác `4/0`; các hãng không có kích thước tuyệt đối hoàn toàn giống nhau. |
| Dây chính và leader | Mono/braid/fluorocarbon/wire theo vai trò; mức chịu lực phù hợp và chiều dài leader khi ảnh hưởng hình/chuyển động. **lb-test là sức chịu lực danh định, không phải đường kính, trọng lượng cá hoặc lực căng hiện tại**. Không suy ra đường kính chính xác nếu chưa tra sản phẩm. |
| Phụ kiện và sơ đồ nối | Sinker, swivel, snap, bead, float/bobber, split ring hoặc harness chỉ khi bộ câu cần; số lượng và đường nối cụ thể. Nêu phần nào nằm ngoài khung, chì nằm đáy hay treo, mồi cách đáy bao nhiêu, dây ra hướng nào. Không cho mọi phụ kiện vào cùng một rig. |
| Động tác và key | Tốc độ/hướng kéo, khoảng nghỉ, kiểu jig, trạng thái chùng/căng; cách cá cắn và hệ thống nhận lực. Kết cục không nhất thiết là mắc câu. Key có thể là theo rồi quay đi, hụt, nhả, đổi hướng hoặc mắc câu nếu hình chứng minh được. |
| Cơ sở kiểm chứng | Tài liệu loài/cách câu từ cơ quan thủy sản, quy định bang/thủy vực và sơ đồ/ảnh sản phẩm thực của nhà sản xuất khi cần cấu tạo. Phân biệt kinh nghiệm thông dụng, thông số sản phẩm, quyết định dàn cảnh và yêu cầu pháp lý. |

Các số trong bảng dưới là **ví dụ tham khảo có nguồn**, không là tiêu chuẩn bắt buộc cho mọi cá cùng loài. Khi có dụng cụ cần mô tả, AI phải chọn một bộ cụ thể đủ rõ để vẽ; không dán tất cả lựa chọn hoặc một dải thông số chưa chốt vào prompt. Không đổi cấu hình hợp lý đã được người dùng khóa chỉ để theo một ví dụ.

### 2A.3. Hồ sơ theo loài — lựa chọn khởi đầu, không phải kịch bản mặc định

| Cá chính | Mồi và cách trình bày phù hợp để nghiên cứu/chọn | Móc, dây và leader cần khớp | Lỗi cần tránh |
|---|---|---|---|
| **Redfish / red drum** | Mồi tự nhiên: tôm, finger mullet, blue crab; chọn một. Có thể dùng tôm dưới popping cork, mồi cá với slip-sinker đáy, hoặc mồi giả như spoon, soft-plastic/jig và shallow plug. Khớp cách trình bày với độ sâu, cỏ, đáy và dòng triều. [TPWD: Red drum](https://tpwd.texas.gov/huntwild/wild/species/reddrum/). | Mồi tự nhiên: chọn single hook phù hợp; nếu dùng circle thì giữ hình dạng/cách nhận lực đúng mục 2A.5. Soft-plastic jig có jig hook tương ứng; hard lure giữ đúng cấu tạo sản phẩm. Mono/braid và leader chống mài mòn được chọn theo vật cản, không tự dùng bộ muskie. TPWD nêu ví dụ dây 8–15 lb ở grass flats và 17–25 lb gần vật cản. | Không mặc định Redfish–cua. Không biến mồi cắt khúc thành cá tự bơi; không đặt cork chìm dưới đáy; không cho spoon hoạt động như cá sống. Không coi circle hook là bắt buộc cho mọi redfish trên toàn Mỹ. |
| **Muskie / muskellunge** | Bucktail/spinnerbait, jerkbait, crankbait hoặc spoon cỡ thích hợp; chọn casting/retrieve hay trolling và đường chạy đúng loại. Mồi sucker sống với quick-set/quick-strike rig là hướng cần nghiên cứu riêng, có đối chiếu quy định địa phương. [Wisconsin DNR: cách câu](https://dnr.wisconsin.gov/topic/Fishing/outreach/hookyourcatch.html). | Bộ lure thường cần dây braid chịu tải cao và **bite leader** chống răng; Wisconsin DNR nêu ví dụ braid 50–80 lb. Giữ số móc đơn/treble đúng mẫu lure/rig, không ép thành một móc duy nhất. [DNR: hồ sơ muskie](https://dnr.wisconsin.gov/sites/default/files/topic/Fishing/Musky_MuskellungeFactSheet2012.pdf). Wire/heavy fluorocarbon có lựa chọn theo kiểu lure; ví dụ của Jim Saric là fluoro 130 lb dài 14 inch cho nhiều cách casting, **không phải chuẩn duy nhất**. [Mercury Marine: leaders](https://www.mercurymarine.com/us/en/lifestyle/dockline/musky-leaders-101). | Không dùng leader mảnh kiểu walleye cho bộ muskie lớn. Không mặc định fluorocarbon chống cắn tuyệt đối. Không thêm quick-strike hooks vào lure vốn không có chúng; không viết figure-eight nếu quỹ đạo/nguồn kéo gần thuyền không hợp khung. |
| **Walleye** | Jig-and-minnow; slip-sinker/Lindy rig với minnow, nightcrawler hoặc leech; slip-bobber; hoặc hard lure casting/trolling. Chọn một phương pháp theo mùa, tầng nước và địa hình. [Minnesota DNR: cách câu walleye](https://www.dnr.state.mn.us/gofishing/how-catch-walleye.html). | DNR nêu ví dụ bộ spinning với dây 6–10 lb; mono hoặc braid kèm mono leader. Mồi tự nhiên nhỏ có thể dùng single hook; DNR nêu #4/#6 là ví dụ cỡ móc cho walleye, không áp nguyên cho jig hoặc crankbait. [DNR: dụng cụ](https://www.dnr.state.mn.us/fishing/fin/equipment.html). | Không sao chép bộ muskie nặng sang walleye. Không tự gắn wire leader hoặc nhiều treble vào minnow đơn. Không cho chì trượt cùng mọi vật như một khối; không biến slip-bobber thành lồng/bẫy. |
| **Loài cá được câu bất kỳ khác ở Mỹ** | Tự chọn/đọc loài cụ thể trước, rồi tra mồi–phương pháp–bang/thủy vực của chính loài đó. Cá hồi, bass, catfish… không dùng chung một hồ sơ. | Tạo hồ sơ theo 2A.2 với đồ phù hợp cỡ cá/mồi, môi trường và cách câu; không lấy bảng của redfish/muskie/walleye rồi chỉ thay tên. | Không khẳng định “đúng tại Mỹ” chỉ vì bộ câu được bán ở Mỹ. Không tự thêm trap/net/trotline cho một loài vì nó có thể ăn cùng loại mồi. |

**Mồi tự nhiên cũng cần kiểm địa phương:** một con cá mồi có thể là prey tự nhiên nhưng bị hạn chế làm bait, bị hạn chế vận chuyển hoặc có yêu cầu nguồn cung. Khi cần live bait, kiểm tên loài thật, nguồn được phép và cách gắn hợp sản phẩm; không viết chung chung “local baitfish” rồi vẽ ngẫu nhiên cá nhiệt đới. Không cần ép tên hãng/logo lên hình; dùng ảnh sản phẩm làm tư liệu cấu tạo, không yêu cầu chữ thương hiệu.

### 2A.4. Khóa sơ đồ nối — mỗi video chỉ chọn một cấu hình phù hợp

Các chuỗi sau là **khung mô tả kết nối để thiết kế cảnh**, không phải danh sách bắt buộc phải có trên mọi rig. Hoàn thiện theo bộ câu đã kiểm; nếu chi tiết ở ngoài khung, chỉ mô tả hướng dây và tác dụng, không kéo nó vào hình:

- **Jig đơn:** `dây chính → leader/nút nối nếu dùng → mắt jig → đầu jig và móc liền thân → soft plastic hoặc mồi tự nhiên đã chọn`. Mồi bám thân móc/đầu jig đúng cấu tạo, không có một hook khác nổi tự do cạnh đó. Nêu hướng mũi móc theo đúng rigging, không coi mọi jig là weedless.
- **Slip-sinker đáy:** `dây chính đi qua lỗ chì trượt → bead nếu có → swivel/chặn theo cấu hình → leader → single hook → bait`. Chỉ dùng đúng biến thể đã chọn. Chì có thể nằm đáy trong khi dây trượt qua; khoảng leader không tự co giãn hoặc biến mất. Không nhầm với sinker cố định ngay trên móc.
- **Slip-bobber:** `bobber stop → bead nếu cấu hình cần → float trượt trên dây → phần tải/leader/móc theo bộ đã chọn`. Phao ở mặt nước, mồi ở tầng đặt trước. Với camera đáy không thấy mặt nước, float thường ngoài khung; dây đi lên theo góc hợp lý, không vẽ bobber nằm trên sỏi.
- **Muskie lure casting:** `braid → bite leader với đầu nối phù hợp → eye/snap theo mẫu → một lure có số hook hangers/split rings/hooks cố định`. Không gắn thêm chì đáy hoặc phao chỉ vì chúng được nhắc ở bảng khác. Nếu chọn một mô hình lure cụ thể, kiểm hình sản phẩm trước khi chốt số treble và điểm treo.
- **Live sucker quick-strike/quick-set:** tra đúng sơ đồ thực và quy định về móc, rồi khóa dây/leader, bộ phận gắn mồi và vị trí từng hook. Không tự suy ra “hai treble là hợp lệ ở mọi bang”, không gộp các biến thể thành rig tưởng tượng. Nếu không xác minh được cấu tạo, chọn phương án khác đã có cơ sở hoặc nêu ngắn giới hạn nếu người dùng khóa rig này.

**Một mồi/cụm mồi chính không đồng nghĩa một móc cho mọi trường hợp.** Lure có thể có nhiều treble đúng thiết kế; rig có thể có nhánh đúng sơ đồ. Dùng cấu hình đơn giản khi phù hợp để giảm lỗi sinh hình, nhưng không bẻ cấu tạo thật chỉ cho dễ prompt. Ghi số lượng và vị trí cụ thể, rồi giữ nguyên từ first frame tới cuối video, kể cả khi tạm khuất sau cá/cỏ.

### 2A.5. Vật lý dụng cụ và hành vi nhận lực phải đúng

1. **Móc phải nối thật:** dây/leader vào mắt móc hoặc mắt lure đúng vị trí; jig hook nối liền đầu jig; treble treo qua hanger/split ring đúng mẫu. Móc không tự mọc từ má cá, không đi xuyên hàm hoặc xuyên lure. Dây không kết thúc ở giữa nước. Chỉ gọi mắc câu khi hình/chuỗi lực xác nhận, không từ một cú đớp đơn thuần.
2. **Circle khác J-hook:** circle có mũi cong vào trong; không thay bằng J-hook qua một frame. Khi kịch bản dùng circle, mô tả cá mang mồi và lực dây tăng dần, không cú giật mạnh kiểu J-hook để tạo drama. Với loại khác, chọn động tác phù hợp rig cụ thể. [FWC: Fishing Basics](https://myfwc.com/fishing/basics/). Không ép mọi cú cắn thành mắc ở cùng một vị trí miệng.
3. **Dây phản ứng với lực:** xác định đầu đi về cần/thuyền/bờ ngoài khung; dây chùng có đường cong hợp dòng và trọng lượng, khi kéo thì căng dần đúng hướng. Không dùng dây như que thép, dây thừng phát sáng hoặc đường đồ họa luôn rõ bất chấp độ đục. Không cho cá bị kéo lùi khi dây vẫn chùng và chưa có lực khác.
4. **Mồi giả có cơ chế cụ thể:** spinner cần dòng nước tương đối để cánh quay; spoon lắc/flutter hợp hướng kéo hoặc rơi; crankbait bơi theo thân/lip và lực kéo; soft-plastic tail phản ứng với dòng. Khi dừng kéo, nổi/chìm/lơ lửng theo loại lure đã chọn và tải leader/phụ kiện, không mặc định mọi lure đều nổi. Mồi chết không tự tạo lực bơi; mồi sống có thể tự cử động trong phạm vi dây/điểm gắn.
5. **Chì/phao đúng vai trò:** tải, độ nổi, lực cản và dòng quyết định vị trí, tốc độ chìm và góc dây. Không cho chì nặng lơ lửng vô lực, phao nổi nằm dưới đáy vô neo, hoặc chì cào đá tạo bùn trên nền không có hạt mịn. Không thêm tải vào lure rồi vẫn bắt giữ y nguyên độ nổi khi điều đó mâu thuẫn.
6. **Âm thanh đồ câu có nguồn:** kim loại chạm kim loại/đá hoặc lure có rattle chỉ phát tiếng khi đúng cấu tạo và chuyển động. Dây chịu lực không mặc nhiên phát tiếng rít lớn dưới nước; máy câu ngoài khung/ngoài mặt nước không được nghe như micro sát máy. Tiếng popping cork ở mặt nước cần hợp góc thu chìm. Giữ yêu cầu âm thanh môi trường + hành động, lớn/rõ, xuyên suốt mục 5; không lấp tiếng bằng click/hit giả.

### 2A.6. Bẫy/lồng, lưới và quy định địa phương

Mặc định khi có hoạt động câu là **hook-and-line phù hợp loài**. Lồng bắt cá, bait trap, crab pot, trotline, jugline, lưới hoặc tip-up không phải những tên thay thế cho nhau. Không mặc định bẫy dành cho cá mồi/cua được phép dùng để bắt Redfish/Muskie/Walleye.

Nếu câu chuyện thật sự dùng bẫy/lưới hoặc phương pháp khác, phải xác minh **loài được bắt, bang/thủy vực, nước ngọt/mặn, mùa, loại thiết bị, mục đích giải trí/thương mại và điều kiện áp dụng** bằng cơ quan quản lý hiện hành. Ví dụ Texas phân biệt các thiết bị và hạn chế loài được giữ trên trotline; không suy ra một quy tắc chung cho mọi phương pháp từ ví dụ này. [TPWD: Legal Devices, Methods & Restrictions](https://tpwd.texas.gov/regulations/outdoor-annual/fishing/general-rules-regulations/legal-devices-for-fish).

Không ghi “legal throughout the US” hoặc biến lựa chọn circle hook thành luật toàn quốc. Quy tắc có thể đổi theo bang, thủy vực và mùa. Nếu chưa xác minh được một cấu hình đặc biệt, không trình bày nó như hoạt động hợp lệ đã kiểm; ưu tiên phương án thông dụng có cơ sở trong phạm vi ý tưởng được giao. Nếu người dùng yêu cầu giữ chính thiết bị chưa kiểm được, nêu ngắn giới hạn đó ngoài ba đầu ra, không bịa kết luận và không tự đổi ý định chính.

### 2A.7. Đưa hồ sơ dụng cụ vào ba đầu ra và QA

- **FIRST FRAME PROMPT:** nếu có câu cá, mô tả mồi/loại móc/số móc, dây–leader và các phụ kiện **thật sự nhìn thấy**; vị trí/điểm nối, hướng dây ra khung, trạng thái t=0 và tỷ lệ. Nêu đủ đặc trưng để model vẽ đúng bộ, không nhồi nguyên bảng đồ câu. Nếu không có dụng cụ thì khóa rõ `No lure, hook, fishing line, sinker or trap` khi cần ngăn model tự thêm.
- **OMNI FLASH VIDEO PROMPT:** nhắc lại cùng bộ câu đã chốt, giữ số lượng/kết nối, chuyển động mồi đúng phương pháp, chùng/căng và nguồn kéo; key cùng hậu quả phải tuân theo cấu hình ấy. Không đổi móc/rig khi cá che mồi; không đổi từ săn mồi tự nhiên thành hooked fish.
- **CAPTION:** dùng đúng từ bait/lure/jig/rig và loài; không gọi mồi tự nhiên là lure, không gọi theo mồi là caught. Giữ hook ngắn gây tò mò, giọng tự nhiên với người câu cá Mỹ + 3–5 hashtag viết liền một đoạn, không xuống dòng; không nhắc AI hoặc hashtag AI như mục 5.
- **QA thực tế:** xem ảnh mở đầu và từng frame quanh key: số móc, vị trí treo/điểm móc bait, đường dây, mối nối, chì/phao, cách lure bơi và trình tự nhận lực có đúng hồ sơ không? Vật tạm khuất có hiện lại với cấu tạo cũ không? Phân biệt khó nhìn vì quang học với sai cấu tạo. Nếu render đổi rig, sửa ảnh/prompt và kiểm lại; không dùng caption để giải thích hộ lỗi vật lý.

**Nguồn bổ sung kiểm ngày 15/10/2026:** các link tại mục 2A là tư liệu sơ cấp từ cơ quan quản lý và bài hướng dẫn trực tiếp của chuyên gia trên Mercury Marine. Hồ sơ Wisconsin muskie 2012 là tư liệu nền về loài/đồ câu, **không dùng làm quy định năm hiện tại**. Kiểm lại nguồn quy định khi chọn cảnh cụ thể. Khi thiếu web, có thể dùng cấu hình phổ thông đã có cơ sở trong file nhưng không tự nhận vừa xác minh tính hợp lệ tại địa điểm; không bịa thông số sản phẩm/sơ đồ còn thiếu. Các bảng mở rộng khả năng sáng tạo, không khóa ý tưởng thành vài loại bait/rig cố định.

## 3. Quy luật hình ảnh dưới nước tạo cảm giác quay thật

**Khoảng cách và độ trong.** Xác định khoảng nhìn hữu ích, chẳng hạn một vài mét hoặc ít hơn trong lạch nhiều phù sa. Vật ở xa phải giảm tương phản và mất chi tiết trước khi đến gần. Không cho đáy xa sắc nét hơn mõm cá gần máy. Độ đục phải nhất quán trong cả cảnh, trừ một đám bùn mới phát sinh tại vị trí bị khuấy. Hạt lơ lửng có kích thước và mật độ không đều; chúng **không phải màn tuyết hạt trắng đồng đều**. Hấp thụ và tán xạ ánh sáng làm màu thay đổi theo đường đi trong nước, nên đừng tô cá đỏ/cam bão hòa như ảnh trên cạn. [Nghiên cứu lưu trữ tại NOAA về màu ảnh dưới nước](https://repository.library.noaa.gov/view/noaa/70095) và [NOAA về ánh sáng, màu ở độ sâu](https://oceanexplorer.noaa.gov/lesson/bioluminescence-light-and-color/) hỗ trợ nguyên tắc này.

**Ánh sáng.** Quyết định một thời điểm: trưa nắng nông, trời âm u, hoàng hôn, hoặc bóng mát dưới cỏ. Chỉ vẽ vân nắng dao động trên đáy khi có ánh mặt trời trực tiếp và nước đủ nông/trong. Với walleye ở chiều tối, cảnh nên tối vừa đủ để vẫn đọc được cá và mồi, không dùng đèn sân khấu chiếu riêng lên thân. Một nguồn sáng từ phía trên tạo bóng và độ tương phản phù hợp ở mọi vật, kể cả dây, mồi và cỏ.

**Máy quay và khung.** Camera đặt thấp, cố định trên đáy hoặc giá không thấy trong hình; góc nhìn ngang/hơi chếch lên, ống kính góc rộng vừa phải. Duy trì cùng tiêu cự, phối cảnh, độ cao và hướng nhìn suốt 10 giây. Mép khung có thể bị cỏ/vỏ sò chắn một phần; bụi đáy và thân cá có thể che máy thoáng chốc. Cho cá tiến **trong không gian**, lớn lên vì tới gần ống kính, không vì crop/zoom. Tránh dolly, drone underwater, chuyển nét kịch tính hoặc cut đúng lúc cá đớp. Không cố làm footage bẩn bằng quá nhiều noise, méo ống kính, vignetting hay bong bóng giả.

**Tránh cảm giác cảnh được dàn:** trước khi chốt first frame, nhìn xem cá và con mồi có đang cùng sáng, cùng nét, cùng phô toàn thân ở hai vị trí “đẹp” không. Nếu có, che bớt **một** mép bằng cỏ/hàu/đá đúng địa hình, cho vật xa mất tương phản, hoặc đặt con mồi lệch trục cá một chút. Giữ điểm quan sát chính đọc được trên điện thoại. Không phá bố cục bằng lỗi ống kính giả; sự bất toàn phải có nguyên nhân quang học/vật lý trong cảnh.

**Tỷ lệ.** Ghi chiều dài cá, mồi và khoảng cách ở mức tương đối hợp lý. Cua nhỏ bên cạnh redfish, jig nhỏ hơn mõm walleye, baitfish/lure đủ kích thước để muskie chú ý. Cỏ, sỏi, móc câu và dây phải có tỷ lệ thống nhất khi cá đi qua. Một cá lớn gần máy có thể lấp khung; nó không thể đột ngột tăng gấp đôi chiều dài ở cùng khoảng cách.

## 4. Quy luật chuyển động: một nguyên nhân tạo một hậu quả

Lập **bản đồ trạng thái ở t=0** trước khi viết diễn biến. Gọi các vật `F` (fish), `P` (prey/lure), `L` (line nếu có), `B` (bottom), `C` (camera). Ghi cho từng vật: vị trí trong khung (x,y), khoảng cách ước lượng tới camera, độ cao so với đáy, hướng đầu, trạng thái động/tĩnh và vật nào che vật nào. Tọa độ x/y là tỷ lệ 0–1 tính từ trái/trên; chỉ dùng để soạn prompt, không cần in lưới lên ảnh.

**Điều kiện t=0:** khung đầu đặt ra mục tiêu quan sát: mồi/con mồi và không gian cá sẽ đi vào, hoặc đã có một phần cá trong khung. **Không buộc cá phải hiện hoàn toàn ở t=0**. Trong *Guess the name of the rig*, mồi tím rõ từ đầu còn cá đi vào sau; trong *which species*, mồi hồng ở góc dưới và cá hiện rõ về sau. Điều quan trọng là video **không tạo vật mới vô cớ**: cá đi vào liên tục từ mép khung, từ sau cỏ hoặc từ vùng nước mờ, đúng vị trí đã dự liệu. Cá chưa được có mồi trong miệng nếu cú đớp diễn ra ở giây 6. Mồi chưa bị nhấc nếu dây chỉ căng ở giây 8. Đám bùn do cú lao cuối video chưa tồn tại từ đầu.

**Chuyển động:** các mô tả sau là tiêu chí kiểm duyệt cảnh, không phải mô phỏng động lực học đã chứng nhận. Cá có thể có đoạn lướt theo quán tính sau một cú quẫy; không ép mọi dịch chuyển phải kèm một cú quẫy lớn. Thân và đuôi tạo lực đẩy; vây ngực/vây bụng điều chỉnh thăng bằng; tăng tốc đi kèm ít nhất một cú quẫy rõ. Cá đổi hướng qua cung bơi có bán kính, không xoay tròn tại chỗ như mô hình 3D. Mang và miệng cử động ít nhưng hợp nhịp. Nếu con mồi chạy, nó phải phản ứng sau dấu hiệu săn mồi và rời theo một đường liên tục. Không cho hai vật xuyên nhau.

**Phản ứng của con mồi:** trước khi cá tới gần, chọn **một** chiến thuật hợp loài: đứng yên ngụy trang, giơ càng/phòng thủ, lùi từng bước, đổi hướng, hoặc bỏ chạy. Đứng yên **vẫn là một hành vi** nhưng cần dấu sống nhỏ như vây giữ vị trí, mắt/hướng thân, càng điều chỉnh; khi cá đã ở sát trong nhiều giây, phải có lý do rõ để tiếp tục bất động. Với cua: càng có thể mở/khép nhẹ, chân bám nền rồi đẩy thân sang bên vào hốc; bùn nổi từ chân/càng quệt đáy. Với cá mồi: thân uốn và đuôi quẫy trước khi đổi hướng. Không mô tả cua “teleport” vào vỏ hàu hoặc cá mồi biến mất sau một frame; đường thoát cần được che dần bởi vật cản hoặc đi liên tục qua mép khung.

**Chuỗi nhân quả cho một tương tác:** `phát hiện → phản ứng nhỏ của con mồi → cá điều chỉnh hướng → cú áp sát/đớp duy nhất → chân/vây/miệng tác động → bùn/cỏ/mồi đổi trạng thái → kết quả nhìn thấy hoặc che khuất có lý do`. Không bắt buộc clip có đủ mọi bước riêng rẽ, nhưng **thứ tự không được đảo**. Không để 4–6 giây giữa cá và con mồi gần nhau mà không có biến đổi nào, trừ khi chính sự chờ đợi là tình huống kể chuyện có dấu hiệu quan sát cụ thể.

**Cảnh key bắt buộc — một sự kiện tạo câu chuyện cho toàn bộ 10 giây:** trước khi chia beat, xác định `kỳ vọng người xem → tín hiệu/chuẩn bị → twist hoặc hành động then chốt → hậu quả xác nhận`. Key là thay đổi quan trọng trong một cú máy liên tục, **không phải một cảnh cắt**. Nó có thể là cú twist về kết quả, một cú đớp/lao/thoát cực nhanh, cú nhả đảo ngược tưởng đã ăn, động tác phòng thủ làm cá đổi hướng, hoặc một hành động khác đủ làm người xem hiểu clip đang kể chuyện gì. Không chấp nhận chỉ cá bơi qua, áp sát lặp lại hoặc hình đẹp không có đổi trạng thái đáng chú ý.

### Thời điểm key — bắt đầu sau giây thứ 5, không giải quyết câu chuyện ngay đầu clip

**Quy tắc bắt buộc của kênh mới:** trong video đúng 10s, hành động key chỉ được **bắt đầu khi `t_key_start > 5.0s`**, không phải đúng 5.0s và không chỉ là đạt đỉnh sau mốc đó. Mốc được chọn linh hoạt theo từng câu chuyện; không mặc định mọi video đều đớp ở 5.1s, 6s hay 7s. Key vẫn phải kết thúc đủ sớm để thấy hậu quả trước 10.0s. Đây là quyết định biên tập cần thử nghiệm trên video và dữ liệu người xem, không phải kết luận nghiên cứu rằng chỉ cần dời key là bảo đảm retention/viral.

- **Hook thị giác khác key:** ngay đầu clip cần có điều đáng quan sát như mồi đang hoạt động, bóng cá sau cỏ, ánh mắt/hướng đầu hoặc khoảng trống gợi một cuộc chạm trán. Không dùng lại cú đớp, cảnh đã mắc câu hay kết quả cuối làm teaser trước rồi quay về chuẩn bị. Một shot liên tục, không flash-forward hoặc preview key.
- **Từ 0.0 tới hết 5.0s:** xây kỳ vọng qua những thay đổi có ý nghĩa: cá phát hiện, ra khỏi chỗ che, theo/điều chỉnh hướng; con mồi có dấu sống và phản ứng phù hợp, mồi giả hoạt động đúng cơ chế. Không cho cú lao tấn công chính, cắn/ngậm/mắc câu, thoát quyết định hoặc twist giải quyết câu chuyện xảy ra trong khoảng này rồi chỉ đặt nhãn KEY vào một động tác muộn hơn. Với câu chuyện câu cá, không cho cá đã cắn ở giây 2 rồi gọi cú lắc đầu ở giây 7 là key để lách quy tắc.
- **Sau 5.0s:** thực hiện key ở tốc độ đời thực với tạo lực và đường đi liên tục, rồi cho thấy phản ứng/hậu quả đến hết clip. Có thể thử bắt đầu khoảng 5.5–8.0s khi hợp cảnh, **chỉ là gợi ý**, không thêm khung giờ bắt buộc. Không dồn key sát 10s đến mức mất kết quả, không kéo dài cú cắn hoặc dùng slow motion cho đủ thời gian.
- **Dàn cảnh để trì hoãn hợp tự nhiên:** điều chỉnh cự ly ban đầu, đường lure, đường cá đi vào, vật che hoặc thời điểm phát hiện. Không đặt cá sát mồi ngay t=0 rồi buộc nó chờ bất động năm giây. Không làm mồi treo đứng vô lực, kéo quá chậm khiến spinner không quay, hoặc cho prey phớt lờ nguy hiểm để chờ timecode. Nếu bối cảnh không đủ chỗ/nhịp, sửa đồng thời first frame và video prompt trong cùng ý tưởng; ưu tiên nhân quả thật.
- **Giữ phần đầu có cảm xúc:** mỗi beat chuẩn bị phải thêm thông tin hoặc đổi quan hệ cá–mồi, không kéo dài/lặp “cá tiến gần” để lấp 5s. Âm thanh môi trường + hành động vẫn lớn/rõ và liên tục từ 0s như mục 5; không làm phần đầu im lặng hoặc thêm hit giả. Không bắt buộc phải có cá lộ toàn thân ngay đầu.
- **Kiểm ở bản render:** tìm frame đầu tiên của hành động key thật, không chỉ đọc nhãn timecode trong prompt. Nếu cú lao/cắn hoặc biến cố quyết định bắt đầu ở hoặc trước 5.0s, bản render chưa đạt yêu cầu nhịp dù đỉnh/kết quả ở giây 6–8; sửa dàn cảnh/prompt và tạo lại khi được phép. Đồng thời kiểm phần đầu có tiến triển và phần cuối còn hậu quả đọc được. Không xác nhận đạt khi chưa xem video.

**Câu khóa để tích hợp vào video prompt:** `The key action must begin strictly after 5.0 seconds, with its onset explicitly timed. From 0.0 through 5.0 seconds, show only physically plausible setup, tracking and anticipation; no main attack, bite, hookup, decisive escape or outcome reveal. Do not show the key early and relabel a later reaction as the key. Vary the onset for this story and leave enough time for a visible aftermath before 10.0 seconds. Keep real-time motion, continuous meaningful progression and audible environmental and action sound throughout.` Viết lại cho đúng hành động cụ thể của từng clip, không dán danh sách biến cố không liên quan vào prompt.

**Sáng tạo không bị bó trong báo cáo:** có thể phát triển key mới ngoài các Reel tham khảo. Một cú bỏ qua vẫn có thể là key nếu có diễn biến chuẩn bị và một quyết định/hậu quả bất ngờ nhìn thấy rõ; không dùng nó như lý do để né xây câu chuyện. Tránh bịa hành vi trái loài, thêm sinh vật bất khả thi ở địa điểm hoặc dựng kết quả chỉ được caption kể hộ.

**Nhanh phải thật:** cú tấn công hoặc thoát có thể rất nhanh ở tốc độ đời thực, nằm trong một beat ngắn có mốc thập phân, nhưng phải có động tác tạo lực, đường đi liên tục và phản ứng hợp sinh học. Không làm chậm cú đớp cho vừa một beat dài; không dùng tua nhanh, slow motion mặc định, teleport, xuyên vật hoặc tiếng nổ để giả tốc độ. Beat kể chuyện và thời lượng động tác không phải một thứ; không gắn cùng tốc độ cho cả ba loài.

**Kiểm key trước khi viết:** key thay đổi điều gì trong câu chuyện? Vật nào phát hiện/tạo lực? Khoảng cách có thể khép lại trong thời gian dự kiến không? Con mồi có lối thoát? Vật cản đã có từ t=0? Người xem thấy dấu hiệu nào trước và hậu quả nào sau? Nếu key bị vùi hoàn toàn trong bùn hoặc không thể chỉ ra trên hình, đổi bố cục/diễn biến để nó đọc được. Kết quả cuối có thể chưa chắc chắn nhưng sự kiện key vẫn phải được cảm nhận từ chuyển động và dấu vết có lý do.

**Tương tác:** nếu cá đụng mồi, mồi đổi vị trí/hướng; nếu dây câu gắn mồi, dây phải đi tới mép khung đúng phía người câu và thay đổi chùng/căng theo lực. Dây có thể đã căng ở t=0 khi lure đang được kéo; không bắt mọi loại rig phải chùng ban đầu. Mồi giả chuyển động theo lực kéo/dòng nước; con mồi sống có lực đẩy riêng; chỉ thêm tác động từ cá khi đã có tiếp xúc hoặc dòng nước do cá gây ra. Nếu cá nhả mồi, mồi đi từ miệng ra theo hướng hợp vận tốc/dòng nước; không xuất hiện lại đúng vị trí ban đầu. Đám bùn bắt đầu tại nơi vây, mõm hoặc mồi chạm nền, lan và lắng dần; sỏi lớn không nổi như tro. Cỏ chỉ cong khi dòng nước hoặc vật va chạm, rồi hồi lại. Âm thanh xuất hiện **cùng thời điểm** với va chạm/đáy bị quét, không đến trước vài giây.

**Nhịp 10 giây linh hoạt — 5–8 beat:** tự chia khoảng `[0.0–10.0s]` thành **5 đến 8 beat**, ngắn/dài theo hành vi và câu chuyện. Cho phép mốc thập phân như `[1.3–2.3s]` và beat rất ngắn cho cú đớp/thoát nhanh. Không chia cố định mỗi 2 giây; không đặt thời lượng tối thiểu/tối đa chung cho mọi beat. Các khoảng phải liên tiếp, mốc kết beat trước bằng mốc đầu beat sau, không chồng/thiếu thời gian, và tổng đúng 10 giây. Mỗi beat có một thay đổi chính mới, đọc được; mọi beat nằm trong cùng shot.

**Một ví dụ nhịp, không phải khuôn:** `[0.0–1.3s]`, `[1.3–2.3s]`, `[2.3–3.8s]`, `[3.8–5.2s]`, `[5.2–5.5s]`, `[5.5–7.6s]`, `[7.6–10.0s]`. Beat thứ năm có thể chứa key nhanh, chẳng hạn chuẩn bị đã hoàn tất trước 5.2s, cú lao/né ở khoảng 5.3s, rồi phản ứng tiếp diễn ở beat sau. Đây chỉ là ví dụ dàn cảnh; chọn lại toàn bộ mốc theo key của video, không sao chép chuỗi này cho mọi loài. Key bắt đầu sau 5.0s theo quy tắc trên; ví dụ này dùng 5.2s, nhưng không bắt buộc mọi key ở 5.2s, trong khoảng 6–8s hoặc sát cuối clip.

**Kiểm nhịp trước khi sinh:** ở mỗi ranh beat, chỉ ra điều gì vừa thay đổi và nó giúp chuẩn bị/key/hậu quả thế nào. Nếu hai beat chỉ lặp “cá tiến gần hơn”, gộp hoặc thay bằng tín hiệu hay phản ứng có ý nghĩa. Không ép thêm hành động vô cớ cho đủ beat; có thể tách chuẩn bị, động tác và hậu quả của cùng một tương tác. Kiểm hành động key thật bắt đầu sau 5.0s, không có cú đớp/kết quả chính sớm bị đổi tên thành chuẩn bị; giữ đủ khoảng đọc kết quả trước 10.0s. Caption phải bám điều nhìn thấy. Timecode là chỉ đạo cho model, chưa phải kết quả render đã khớp khung hình.

## 5. Âm thanh và caption

### Bốn MP4: số liệu được ghi trong hồ sơ nền

| Clip, thời lượng file | Hình ở các mốc chính | Dữ liệu audio gốc và kết luận có thể rút ra |
|---|---|---|
| [*Do you fish tigers?*](https://www.facebook.com/reel/1388103036613085/) — 13,93s | Cá chép rất gần camera từ t=0; cúi xuống bãi mồi, ngậm rồi bơi sang phải; từ khoảng 8–10s rig/dây lộ ở miệng, cuối clip khung dần trống | Có luồng AAC stereo 48 kHz. Mức trung bình toàn clip khoảng **−22,9 dBFS**; các cụm âm nổi ở 0–2s, 5,5s, 7,5s, 9,5s và 12–13s, xen nhiều quãng thấp hơn khoảng −35 đến −40 dBFS. Phổ thiên về tần số thấp, có các vệt xung ngắn. Tiếng không đồng đều liên tục; **không thể gán chắc từng xung** là tiếng cá, dây hay va máy chỉ từ phổ. |
| [*Guess the name of the rig*](https://www.facebook.com/reel/2426590164498757/) — 10,26s | Mồi tím/rig đứng ở phần dưới từ t=0; cá vào rất gần khoảng 2–4s; nửa sau cá rời khung, mồi/đáy cỏ còn lại | AAC stereo 48 kHz; trung bình khoảng **−24,2 dBFS**. Đầu 0–2s rất nhỏ, khoảng −45 đến −47 dBFS theo cửa sổ 0,5s; tăng ngắn ở ~2,5s, ~5s, rồi mạnh hơn khoảng 8–10s. Vì cao trào audio muộn hơn thời điểm cá lấp khung, **đừng ép mọi đỉnh tiếng thành tiếng cú cắn**. Có thể có truyền rung/ma sát hoặc hoạt động ngoài khung; không xác nhận nguồn cụ thể. |
| [*Love the snowman!!*](https://www.facebook.com/reel/1766609001232039/) — 10,95s | Cá chép cúi sát mồi hai màu ở t=0; cá nhỏ lướt qua t≈2s; cá chép áp sát/tác động rig khoảng 4–8s; dây/rig dựng lên ở 8s, bùn và khung trống gần cuối | AAC stereo 48 kHz; trung bình khoảng **−26,4 dBFS**. Nền rất thấp ở nhiều đoạn đầu (~−50 dBFS theo 0,5s), những cụm tăng quanh 4,5s, 7,5–8s và **đỉnh mạnh nhất ở khoảng 10s**. Điều này ủng hộ cấu trúc “yên → những nhiễu động ngắn → hậu âm cuối”, nhưng không chứng minh tiếng 10s đến từ đúng vật nào. |
| [*which species*](https://www.facebook.com/reel/27770037856008456/) — 12,14s | Mồi hồng lộ ở t=0; cá da trơn từ cỏ tới đáy sau ~2s; ria, đầu và thân tiến sát máy 6–12s | AAC stereo 48 kHz; trung bình chỉ khoảng **−56,8 dBFS**, thấp hơn nhiều so với ba clip kia. Có dao động nhẹ khoảng 4,5–7,5s khi cá tới gần, nhưng không có đỉnh lớn tương ứng với cảnh cá lấp khung ở cuối. Bài học: **động tác lớn trên hình không bắt buộc có hit âm thanh lớn**. |

Theo hồ sơ nền được cung cấp, các mức dBFS là phép đo trên bản âm thanh mono giải mã từ MP4; chúng mô tả **mức tín hiệu trong file**, không phải độ ồn cảm nhận trên loa và không chứng minh cách thu âm. Bốn luồng đều có tín hiệu âm thanh; phổ cho thấy nền rộng và những xung ngắn, **không thấy bằng chứng đủ mạnh để xác nhận một bản nhạc chung**, nhưng phân tích số không thay thế việc nghe. Không khẳng định bốn clip tuyệt đối không có nhạc hoặc lời. Những xung nổi có thể là âm tại hiện trường, tiếng dây/camera hay hậu kỳ; nguồn cụ thể chưa được xác thực. [Bản phỏng vấn Underfishing](https://peche-poissons.com/carpe/carpe-underfishing-leurs-videos-subaquatiques-de-carpes-cumulent-des-millions-de-vues-882538-php/) nói máy quay đôi khi thu rung truyền dọc dây; thông tin đó hỗ trợ một **khả năng**, không chứng minh xung nào trong bốn MP4.

**Kiểm tra âm thanh của clip AI Redfish–cua:** tệp thử có nền khoảng −50 dBFS ở phần đầu và một cụm xung lên khoảng −19 dBFS trong cửa sổ 0,1 giây quanh 6,9s, gần lúc cua lùi và bùn nổi. Đây là **đồng bộ thời gian tốt**; phép đo không xác định được tiếng ấy có âm sắc tự nhiên hay giống “impact” điện ảnh. Bài học cho prompt và QA: đặt xung sau cú đẩy/chạm nhìn được, nhưng còn phải **nghe tệp xuất bằng loa điện thoại ở mức bình thường** để xem tiếng có quá đột ngột/lớn so với nền, có thêm nhạc hay tiếng không thuộc cảnh không. Không lấy mức −19 dBFS làm mục tiêu chung.

### Công thức âm thanh cho kênh mới — môi trường + hành động, lớn và xuyên suốt

**Yêu cầu hiện hành:** video phải có **âm thanh môi trường + âm thanh hành động**, volume **lớn, rõ, đầy đặn**, âm thanh xuất hiện **xuyên suốt toàn bộ 10 giây**. Đây là lựa chọn sản xuất của kênh mới theo yêu cầu người dùng, thay thế hướng dẫn nền rất nhỏ/gần như im lặng ở các bản trước; không diễn giải các số đo MP4 tham chiếu thành mục tiêu âm lượng của kênh mới. Omni Flash tạo audio cùng video và [cho phép mô tả riêng sound design](https://ai.google.dev/gemini-api/docs/omni).

1. **Lớp môi trường liên tục:** dựng sound bed đúng thủy vực và góc thu từ `0.0s` tới `10.0s`, nghe rõ cả khi chủ thể chậm lại: chuyển động nước/dòng chảy, nhiễu động môi trường hoặc cọ cây có nguồn hợp lý. Nền có biến thiên tự nhiên, không là tiếng drone phẳng. Không fade về im lặng giữa/cuối clip, không để nhiều giây đầu chỉ có hình mà thiếu tiếng. Không dùng bong bóng liên tục, tiếng chim trên bờ hoặc tiếng mặt nước rõ như thu trên cạn nếu góc thu không giải thích được.
2. **Lớp hành động bám toàn diễn biến:** bố trí chi tiết phù hợp trong từng beat từ chuẩn bị, tiếp cận, phản ứng đến key và hậu quả: nước bị vây/đuôi/thân đẩy, cây/vật liệu bị cọ, mồi/chân/mõm quệt nền hoặc dây/rig chịu lực khi thật sự có. Mức rõ và cường độ thay đổi theo động tác; không chỉ chờ một cú hit duy nhất ở key rồi để phần còn lại gần câm. Beat ít chuyển động dùng chi tiết nhỏ có cơ sở cùng sound bed liên tục, không bịa va chạm chỉ để lấp tiếng.
3. **Key nổi bật, đúng thời điểm:** nhấn hành động quyết định bằng âm thanh rõ, sắc nét theo vật liệu/góc thu nhưng đồng bộ với lực và tiếp xúc nhìn thấy. Sau key, tiếp tục âm phản ứng/nước chuyển động/cọ vật liệu nếu có và giữ môi trường nghe rõ tới hết. Không bắt mọi chuyển động tạo tiếng va mạnh hoặc lặp tiếng đớp suốt 10 giây.
4. **Volume lớn nhưng sạch:** yêu cầu *loud, clear, full-bodied environmental and action audio throughout*. Tăng mức cảm nhận của toàn bản mix, không chỉ làm một transient bật rất lớn trên nền nhỏ. Môi trường luôn hiện diện; hành động tách bạch, key có điểm nhấn, vẫn còn độ động hợp diễn biến. Kiểm và tránh clipping, rè, méo hoặc bass lấn hết chi tiết. Âm lớn không có nghĩa tự thêm tiếng nổ, monster growl hay phóng đại lực vật lý so với hình.
5. **Phối hai lớp xuyên suốt:** ghi âm nền và hành động ngay trong các beat của video prompt hoặc một đoạn sound design chỉ rõ cách chúng chạy từ đầu đến cuối. Không quy định tối đa chỉ một/hai tiếng trong toàn clip; số chi tiết tùy hành động thật, còn key vẫn là một sự kiện kể chuyện chính. Không nhạc và không voice trong bản chuẩn; không cinematic hit, whoosh, bass drop hoặc sonar vô nguồn.

**Biến thể theo bối cảnh:** Redfish ở lạch triều dùng môi trường dòng nước hợp cảnh, cộng các chi tiết nước/cỏ/nền theo chuyển động. Walleye ở hồ đá dùng môi trường hồ nghe rõ cùng nước chuyển động, lure/jig chạm sỏi khi có tiếp xúc thật. Muskie ở mép cỏ dùng nền hồ liên tục, chi tiết nước/cỏ theo tiếp cận và âm hành động rõ ở cú lao rồi phản ứng sau đó. Với loài cá được câu ở Mỹ khác, chọn lại nguồn âm theo đúng môi trường/hành vi, không sao chép máy móc ba mẫu. Đây là sound design cho sản phẩm mới, không phải nhận dạng âm từng loài từ các MP4 nguồn.

**Đoạn audio mẫu để tích hợp vào video prompt:** `Loud, clear, full-bodied underwater environmental and action audio throughout the entire 0.0–10.0 seconds. Keep a continuous, clearly audible habitat-appropriate water ambience bed from the first frame to the last, with natural variation and no silent gaps or fade to silence. Layer synchronized action details across all beats: water displacement, vegetation or substrate contact, and lure or line movement only where justified by the visible scene. Make the key action audibly prominent at its actual timing, then continue the audible environmental bed and physically justified aftermath. Maintain strong perceived volume for the whole mix, with distinct layers and controlled peaks; no clipping, distortion or isolated oversized hit over a barely audible bed. No music, voice, cinematic impacts, whooshes, bass drops, sonar or unmotivated persistent bubbles.` Khi viết bộ prompt cụ thể, thay các nhóm âm chung bằng nguồn/hành động có thật trong cảnh; không chép cả danh sách tiếng không xuất hiện.

### Caption đăng tải: một caption hoàn chỉnh có 3–5 hashtag

**Câu mở đầu:** tiếng Anh Mỹ tự nhiên, giống một người thích câu cá đang nói với người cùng sở thích; khoảng **3–8 từ cho câu hook**, không phải giới hạn của toàn caption. **Bắt buộc gợi tò mò bằng một chi tiết cụ thể trong clip**: cú theo mồi rồi quay đi, quyết định ăn/nhả, cú hụt hoặc dấu hiệu khó đoán; để người xem muốn quan sát và tự phán đoán. Học độ ngắn, tính trực diện của Underfishing, nhưng tự viết câu chữ theo đúng cảnh; không dịch sát từ tiếng Việt, dùng giọng quảng cáo, giật tít chung chung hoặc cố làm mọi bài cùng một câu. Ưu tiên cách nói/thuật ngữ người câu cá Mỹ dùng khi đúng ngữ cảnh, như *follow, short strike, commit, spit the bait, hookset, rig, lure, jig*; không nhồi tiếng lóng hoặc dùng thuật ngữ chỉ để nghe chuyên nghiệp. Phân biệt *bait* với *lure*, cá *follow* với cá đã ăn/mắc câu; *short strike* chỉ khi hình cho thấy cú đánh hụt/không lấy trọn mồi phù hợp, không dùng cho mọi cú quay đi. Ví dụ hướng giọng: `What made him turn off?`, `Would you change that retrieve?`, `Did he just spit the bait?` — chỉ dùng khi hành động và dụng cụ trong clip hỗ trợ, không phải mẫu phải lặp. Có thể dùng câu hỏi, lời mời quan sát hoặc phản ứng ngắn; tạo tò mò mà không kể hộ một kết quả chưa thấy. Không tuyên bố hooked/caught/swallowed nếu hình chỉ cho thấy tiếp cận, ngậm, nhả hoặc bị che. Không câu tương tác bằng “Comment YES” hay yêu cầu tag bạn bè.

**Cấu trúc một caption:** câu hook ngắn + một dấu cách + **3–5 hashtag khác nhau**, tất cả **viết liền thành một đoạn văn duy nhất, không xuống dòng trước hashtag, không tách hashtag thành dòng/đoạn riêng**. Ví dụ định dạng: `What made him turn off? #Muskie #MuskyFishing #Underwater #FreshwaterFishing`. Đây là **một trường caption** có thể sao chép đăng ngay; giao diện tự ngắt dòng theo chiều rộng màn hình không phải ký tự xuống dòng do AI chèn. **Không nhắc AI, việc tạo/sinh/mô phỏng video hoặc bất kỳ công nghệ tạo nội dung nào trong caption; không thêm dòng giải thích nguồn tạo. Không dùng hashtag về AI.** Tập trung hoàn toàn vào loài vật, hành động, câu hỏi và cảm giác tò mò như phong cách kênh tham chiếu. Không cần nhét địa danh vào câu hook nếu làm nó dài và gượng.

**Chọn hashtag:** ưu tiên một tag loài chính, một tag ngữ cảnh câu cá hợp loài, rồi tag dưới nước/môi trường; có thể thêm tag vùng khi đúng brief. Không gắn cả ba loài nếu chỉ có một loài; không dùng một chuỗi tag cố định sai nội dung; không nhồi `#viral #fyp #trending`; loại mọi hashtag về AI hoặc công nghệ tạo video. Ví dụ nhóm hợp ngữ cảnh: Redfish — `#Redfish #InshoreFishing #Underwater #SaltwaterFishing`; Muskie — `#Muskie #MuskyFishing #Underwater #FreshwaterFishing`; Walleye — `#Walleye #WalleyeFishing #Underwater #FreshwaterFishing`.

**Quy tắc đầu ra:** gọi mục này là **CAPTION**, không phải TITLE. Không tách tiêu đề và hashtag thành hai sản phẩm; nếu dùng JSON theo yêu cầu người dùng, lưu toàn bộ trong **một chuỗi `caption` không có ký tự xuống dòng**, không tạo trường `hashtags` riêng. Caption không phải lời thoại hoặc chữ phải vẽ vào video. Các con số 3–5 hashtag là yêu cầu biên tập của kênh mới, không phải nhận định rằng đối thủ dùng hashtag hoặc quy tắc bảo đảm reach.


## 6. Các lỗi làm lộ video AI và cách sửa đúng chỗ

| Lỗi nhìn thấy | Nguyên nhân thường gặp trong prompt | Sửa prompt cụ thể |
|---|---|---|
| Cá đổi số vây, spot/hoa văn trượt trên thân | Chỉ ghi “realistic fish” | Khóa loài, 3–4 dấu nhận dạng và yêu cầu chúng giữ nguyên trên **cùng một cá** suốt clip |
| Key xảy ra ngay đầu clip hoặc cá đứng chờ để kéo tới giây 5 | Thiếu khóa onset; bố cục đặt cá–mồi quá gần hoặc chỉ đổi nhãn KEY | Khóa hành động key bắt đầu sau 5.0s; dàn lại cự ly/đường vào và 5–8 beat có tiến triển, giữ tốc độ thật và hậu quả trước 10s; kiểm trên render |
| Cá lơ lửng, trượt ngang không quẫy, lao như dịch chuyển | Không có hướng, khoảng cách, nhịp tăng tốc | Ghi t=0, hướng đầu, quãng đường hợp lý, cú đập đuôi trước khi tăng tốc |
| Mồi/dây/móc đổi vị trí hoặc mọc thêm | Không lập quan hệ vật thể | Chỉ có **một** mồi và **một** dây nếu có; khóa điểm nối, hướng dây, lực chùng/căng theo diễn biến |
| Bùn phun đồng loạt từ toàn đáy; sỏi bay | Mô tả “dramatic sediment” | Chỉ một đám silt mịn nhỏ từ đúng điểm va, trôi theo dòng; đá/sỏi nằm lại |
| Nước trong như bể kính nhưng hạt dày như tuyết | Hai mô tả quang học mâu thuẫn | Chọn một mức độ đục và khoảng nhìn; vật xa ít tương phản, hạt không đều |
| Cá và con mồi cùng phô rõ, sáng đều, như ảnh quảng cáo | First frame chỉ tối ưu vẻ đẹp của chủ thể | Dùng khoảng cách và che khuất thật của môi trường: một mép cỏ/hàu/đá chắn một phần, vật xa giảm nét/tương phản, không làm mất điểm quan sát chính |
| Con mồi đứng bất động quá lâu dù cá đã sát bên | Không có chiến thuật phản ứng của con mồi | Chọn phản ứng hợp loài trước cú lao: thủ thế/đổi hướng/lùi; nếu đứng yên ngụy trang, vẫn có dấu sống nhỏ và một ngưỡng kích hoạt hợp lý |
| Con mồi biến mất hoặc lao sang bên không thấy lực | Video prompt chỉ ghi “escapes” | Mô tả thân/vây/chân tạo lực, đường thoát liên tục, vật cản che dần; bùn chỉ nổi ở điểm chân/vây tác động |
| Bóng/ánh sáng đổi hướng; caustics trong cảnh tối | Thay bối cảnh giữa các timecode | Khóa cùng giờ, độ sâu, nguồn sáng và góc máy ở t=0 đến t=10 |
| Tiếng hành động đến trước lực/tiếp xúc | Audio mô tả chung chung | Gắn chi tiết với đúng hành động/timecode; giữ sound bed môi trường lớn, rõ và liên tục trước/sau sự kiện |
| Một hit quá lớn trên nền gần câm, rè/méo hoặc không khớp lực nhìn thấy | Chỉ nhấn transient thay vì phối toàn bộ âm môi trường + hành động | Tăng độ rõ/âm lượng cả bản mix xuyên suốt, cân bằng hai lớp và khống chế peak; nhấn key đúng mức, không bịa impact để thay cho hành động |
| Caption hứa cú câu trúng nhưng hình mơ hồ | Không đối chiếu caption với kết cục | Viết lại caption theo hậu quả nhìn được; giữ câu hỏi nếu chưa chắc và giữ đủ 3–5 hashtag trong cùng caption |
| Biểu tượng/chữ của công cụ hiện trong khung | Lớp chèn của hệ thống hoặc bản xuất, prompt “no logo” không kiểm soát được | Kiểm tra tệp cuối; nếu là dấu bắt buộc của nền tảng, ghi nhận như giới hạn của bản xuất; không mô tả nó là footage không có dấu AI |

“Photorealistic, ultra realistic, 8K” không thay thế các ràng buộc trên. Nếu bản sinh sai, sửa **một lỗi có thể chỉ rõ**: “At 6s, the lure remains attached to the same single line and moves only after the walleye mouth contacts it; keep everything else the same.” [Hướng dẫn chính thức của Omni Flash](https://ai.google.dev/gemini-api/docs/omni) cũng khuyến nghị nêu rõ một cảnh liên tục và sửa cục bộ bằng chỉ dẫn đơn giản.

## 7. Cách dùng file này với bất kỳ AI nào

Gửi nguyên file, kèm loài/ý tưởng ngắn hoặc chỉ yêu cầu số bộ. Ví dụ: `Làm một bộ cho Walleye ở hồ Minnesota lúc chạng vạng: theo jig rồi quay đi.` Nếu chưa có loài hoặc quyền chọn cá bất kỳ ở Mỹ, AI hỏi câu bốn lựa chọn ở 0.1 trước. Khi đã có lựa chọn, tự phát triển ý tưởng mới theo 0.1a và chỉ xuất ba mục ở mục 8 cho mỗi video. Không đòi lịch sử chat hoặc file báo cáo khác mới bắt đầu.

Model tạo ảnh không bắt buộc là Omni Flash: **FIRST FRAME PROMPT** phải mô tả được một ảnh tĩnh khi sao chép riêng. **OMNI FLASH VIDEO PROMPT** phải có đủ thông tin cảnh và hành động, chỉ phụ thuộc vào ảnh first frame thực sự được đính kèm; không dùng “như ở trên”, “same as previous chat” hoặc một mô tả chỉ có “animate it”. Không ghi preset/tham số model tạo ảnh chưa biết.

Quy trình thực thi: tạo ảnh từ prompt ảnh → kiểm ảnh theo t=0 → đưa chính ảnh đạt yêu cầu vào input ảnh mở đầu của giao diện Omni → dùng prompt video → kiểm tệp 10s/9:16, hình và tiếng → đối chiếu/sửa caption. Nếu ảnh thực tế khác prompt, sửa ảnh hoặc điều chỉnh **đồng thời** prompt video và caption; không diễn tả một sinh vật/lối thoát không tồn tại trong ảnh như thể đã có.

Đặt 9:16 và 10s trong prompt và các trường giao diện/API tương ứng nếu được hỗ trợ. Dùng `<FIRST_FRAME>` khi giao diện hỗ trợ vai trò đó; nếu có ô Start/First frame riêng, gắn ảnh vào ô đó. Tag trong text không tự tải hoặc đính kèm ảnh. Đừng gắn giới hạn của connector cũ cho mọi bản Omni. Tài liệu chính thức mô tả ảnh mở đầu, video kèm audio và yêu cầu một shot liên tục; nguồn kỹ thuật cần kiểm lại khi giao diện/model thay đổi: [Google Omni Flash](https://ai.google.dev/gemini-api/docs/omni).

Độ dài gợi ý: prompt ảnh khoảng 150–230 từ, prompt video khoảng 230–360 từ; ưu tiên đầy đủ và nhất quán hơn đếm từ máy móc. Khi trường nhập có giới hạn ký tự, rút câu trùng trước, giữ nguyên loài/bối cảnh/t=0/nhân quả/audio. Nếu không có trường negative prompt, viết các loại trừ ngắn ngay trong prompt chính, không tự bịa một tham số API.

Nguồn đã kiểm trong lần biên tập 15/10/2026: tài liệu Google Omni, FWC red drum, Minnesota DNR walleye và Wisconsin DNR muskie. Việc kiểm nguồn không phải xem lại các MP4 hoặc đo lại audio. Phần ví dụ là prompt biên tập, chưa phải video đã sinh và đạt QA.

## 8. Chỉ thị giao việc và hợp đồng đầu ra

> **Vai trò và mục tiêu:** Bạn là AI viết prompt với cách làm việc kết hợp quan sát tư liệu dưới nước, kiểm tra sinh học cá và tính nhất quán hình–âm. Đọc hướng dẫn này như một brief độc lập. Khuyến nghị đọc báo cáo 20 Reel qua link mục 0.2 **để hiểu và phát triển sáng tạo, không bị giới hạn bởi các nghiên cứu này**. Tạo tình huống nguyên bản cho khán giả câu cá Mỹ, một cá chính thuộc lựa chọn Redfish/Muskie/Walleye hoặc loài cá được câu ở Mỹ khác đã chọn theo 0.1, một mồi hoặc con mồi chính, **một cảnh key bắt buộc bắt đầu sau 5.0s** tạo câu chuyện: twist, hành động cực nhanh hoặc thay đổi có ý nghĩa; phần đầu có hook và tiến triển hợp tự nhiên, phần cuối còn hậu quả; 10s, 9:16, camera dưới nước chân thực mặc định cố định, một shot liên tục. Thật về loài, môi trường và chuỗi lực quan trọng hơn việc cố gây sốc. Không tự nhận có chứng chỉ chuyên môn, đã đọc/nghe nguồn hoặc đã render khi chưa thực hiện.
>
> **Cách làm trước khi trả:** dùng nghiên cứu nền và quy trình mục 0; xác định loài, vùng, mùa/giờ/thời tiết, năm biến môi trường, màu sắc tự nhiên, góc camera có thể đặt ngoài đời, trạng thái t=0, đường đi và nơi kết thúc của từng vật, cảnh key, phản ứng phụ của nước/cỏ/dây và âm thanh. Nếu thiếu loài và chưa được giao quyền chọn, chỉ hỏi câu bốn lựa chọn ở 0.1 rồi chờ, chưa xuất prompt/caption. Khi đã có lựa chọn, tự phát triển một ý tưởng mới theo 0.1a, cân nhắc vài hướng rồi chọn hướng mới, rõ, đúng và ít lỗi; không lặp mặc định Redfish–cua hay chép cảnh mẫu. Không in suy luận nội bộ. Chỉ dùng mặc định cho các chi tiết phụ được phép ở 0.1; không hỏi lại loài đã có hoặc quyền chọn đã được giao. Khi ý tưởng sai rõ về sinh thái, chọn cách sửa gần ý định nhất; nếu phải đổi loài chính hoặc kết cục người dùng yêu cầu, nêu một câu thông báo ngoài ba mục, không âm thầm thay đổi trọng tâm.
>
> **Sau khi đã có loài hoặc quyền chọn cá bất kỳ ở Mỹ, chỉ xuất ba mục sau cho mỗi video**, bằng tiếng Anh, mỗi mục là một khối văn bản hoàn chỉnh dễ sao chép. Không thêm phương án thay thế hoặc báo cáo dài trừ khi được yêu cầu. Không để placeholder, câu “như trên”, ghi chú nghiên cứu hoặc link nguồn vào nội dung prompt/caption. Tên mục giữ đúng như sau:

### FIRST FRAME PROMPT

Áp dụng hồ sơ dụng cụ mục 2A khi cảnh có câu cá: khóa mồi, cấu tạo/số móc, các điểm nối và phần dây/leader/phụ kiện nhìn thấy tại t=0. Không thêm dụng cụ vào cảnh săn mồi tự nhiên.

Viết một prompt độc lập để tạo **một ảnh tĩnh dọc 9:16 tại t=0, trước sự kiện chính**. Ghi chi tiết vùng/kiểu thủy vực Mỹ đúng loài, nước ngọt/lợ/mặn, mùa/giờ và thời tiết, độ sâu/độ dốc, vật liệu đáy/cây địa phương, màu nước và màu cơ thể tự nhiên dưới ánh sáng đó. Mô tả camera quan sát dưới nước có thể đặt thật: chiều cao, hướng nhìn, phối cảnh/góc rộng vừa phải, bố cục và tỷ lệ. Mặc định cảm giác footage đời thực, không góc máy/ánh sáng điện ảnh trừ khi được yêu cầu. Thể hiện thời tiết qua hệ quả dưới nước hợp lý, không bắt vẽ bầu trời trong khung chìm. Ghi vị trí/hướng/khoảng cách tương đối của **vật thực sự nhìn thấy**, nhận dạng cá nếu nó hiện trong hình, số lượng chủ thể, vị trí mồi, dây/điểm nối nếu có và vật che/lối thoát sẽ cần trong video. Nếu cá chưa vào khung, mô tả ảnh t=0 không thấy cá; đường cá vào từ đâu được chốt ở video prompt, không yêu cầu ảnh vẽ một cá “ngoài khung” thành cá trong khung.

Áp dụng đầy đủ mục “Nghiên cứu và tái hiện môi trường nước chân thực”: khóa **màu nước + nguyên nhân** tách biệt với **độ trong + suy giảm theo khoảng cách**. Nêu loại/mức/phân bố vật chất lơ lửng nếu có, chi tiết gần còn thấy và chi tiết/độ tương phản/màu bị mất ở xa; hậu cảnh hòa dần theo đường truyền qua nước. Nêu loại nền và có/không lớp vật liệu mịn có thể bị khuấy. Khóa nguồn/hướng/độ tán xạ ánh sáng phù hợp thời tiết. Không coi nước có màu là nước đục; không dùng xóa phông, sương phẳng hay làm mờ toàn ảnh thay tán xạ. Không đổi Secchi/tầm nhìn theo chiều sâu thành tầm nhìn ngang. Không tự thêm hạt, rác, bong bóng hoặc bùn để tăng vẻ thật. Cùng một môi trường phải giải thích được màu sắc cá, nước và nền; không áp màu phim, đèn sân khấu hay vân nắng vào cảnh âm u thiếu nắng trực tiếp. Nếu chủ thể khó thấy, thay cự ly/bố cục hợp lý, không tự làm nước trong, sáng hoặc chủ thể nét hơn điều kiện cho phép. Không kể chuỗi hành động, đặt timecode tương lai, âm thanh hay biểu cảm người trong prompt ảnh. Không cho mồi đã vào miệng, dây đã chịu lực của sự kiện tương lai hoặc mây bùn của cú lao chưa xảy ra. Bố trí cự ly, hướng và vật che tại t=0 đủ cho phần chuẩn bị có tiến triển qua 5.0s trước khi key bắt đầu; không đặt cá sát mồi rồi buộc đứng chờ. Không thêm text, logo, UI, diver hay nhân vật ngoài brief.

### OMNI FLASH VIDEO PROMPT

Nếu có dụng cụ, giữ nguyên bộ đã chốt ở mục 2A và ảnh đầu: cùng bait/lure, hook count, kết nối, leader/phụ kiện; chuyển động và nhận lực theo đúng phương pháp câu. Không ghép rig mới hoặc làm dụng cụ biến hình trong key.

Viết một prompt độc lập bằng tiếng Anh, dùng **chính ảnh first frame được đính kèm làm t=0**, 10 seconds, vertical 9:16, one continuous unbroken locked underwater shot, no cuts/zoom/reframing. Dùng tag `<FIRST_FRAME>` nếu được hỗ trợ, đồng thời nêu bằng lời ảnh phải là opening frame. Giữ danh tính/hoa văn/giải phẫu/tỷ lệ và bố cục **ban đầu**, không khóa cá đứng yên ở vị trí đó suốt clip. Giữ đá/cỏ/đáy, hướng sáng, màu/độ đục nền và camera ổn định. Chỉ cho chủ thể đã định xuất hiện qua đường vào hợp lý.

**Chia thành 5–8 beat linh hoạt**, dùng mốc giây có thể là số thập phân, ví dụ `[1.3–2.3s]`. Beat dài/ngắn theo động tác, không cố định hai giây hoặc giới hạn trong 1,5–2,5s. Toàn timeline bắt đầu `0.0s`, kết thúc `10.0s`, các beat nối liên tục, không chồng/thiếu khoảng. Mỗi beat có một thay đổi chính mới đọc được trong cùng shot. **Bắt buộc có một key**: twist về kết quả, hành động cực nhanh hợp loài hoặc một hành động đủ tạo câu chuyện. Ghi rõ thời điểm bắt đầu hành động key và key interval: **bắt buộc `t_key_start > 5.0s`**, không ở hoặc trước 5.0s; không chỉ dời đỉnh sang nửa sau trong khi cú lao/cắn đã diễn ra sớm. Từ 0.0 tới hết 5.0s chỉ dựng hook thị giác, phát hiện/theo mồi và chuẩn bị có tiến triển, không cho biến cố quyết định/kết quả xuất hiện sớm. Áp dụng đầy đủ mục 4, giữ đủ hậu quả trước 10.0s và không ấn định key ở cùng một giây cho mọi video. Một cú lao có thể nằm trong beat vài phần mười giây và vẫn phải chuyển động liên tục ở tốc độ đời thực. Timecode là chỉ đạo kể chuyện cần kiểm trên render, không bảo đảm chính xác đến từng frame.

Mô tả **trước → trong → sau** biến cố: tín hiệu/chuẩn bị tạo lực; hành động và đường đi liên tục; vật nào đổi trạng thái và dấu vết/kết cục nào xác nhận. Con mồi sống có phản ứng hợp loài, có thể đứng ngụy trang nhưng phải có lý do và dấu sống khi cần; không giật máy móc theo đồng hồ. Khi thoát, chỉ chọn một hốc hoặc một mép khung đã chuẩn bị, cho thấy chân/vây/đuôi tạo lực và sự khuất dần hợp lý. Lure được kéo phải có nguồn lực/điểm nối; mồi tự nhiên sống có thể tự bơi; dây có thể chùng/căng từ t=0 theo cách câu đã chọn. Không teleport, xuyên vật, biến mồi hay thay số vây. Trước khi cho có bùn, xác định nền có vật liệu mịn/rời dễ bị khuấy không, con vật cách đáy bao xa, bộ phận nào tiếp xúc hoặc tạo dòng đủ mạnh đến nền và dòng chảy mang vật liệu đi đâu. Chỉ khi đủ điều kiện, trầm tích nổi cục bộ **sau** tác động rồi lan/trôi/lắng hợp vật liệu và dòng; đá/sỏi lớn không bay. Cá bơi xa đáy hoặc nền không có lớp dễ bị khuấy có thể không tạo mây bùn. Không tăng độ trong/mật độ hạt hoặc thêm mây bùn tùy tiện để làm key dễ thấy hoặc kịch tính hơn.

Tích hợp **sound design ngay trong video prompt**: **hai lớp môi trường + hành động**, volume **lớn, rõ, đầy đặn và xuyên suốt `0.0–10.0s`**. Môi trường đúng thủy vực/góc camera chạy liên tục, nghe rõ từ đầu đến cuối, không silent gaps hoặc fade về im lặng. Ghi chi tiết hành động có nguồn hợp lý trong từng beat, đồng bộ chuyển động/lực/tiếp xúc; không chỉ có một hit ở key. Key được nhấn rõ, sau đó vẫn nghe môi trường và hậu quả hành động tới hết clip. Tăng âm lượng toàn mix, giữ hai lớp phân biệt và peak sạch, không rè/clipping hoặc phóng đại lực bằng tiếng nổ. Không music, voice, cinematic hit, whoosh, bass drop, sonar hoặc bong bóng liên tục vô nguồn. Không biến lựa chọn âm thanh này thành tuyên bố đã nghe hoặc sao chép âm thanh của đối thủ. Không vẽ chữ, caption, hashtag hoặc logo lên video, không thêm kết quả ngoài câu chuyện.

### CAPTION

Trả **một caption tiếng Anh Mỹ duy nhất có thể đăng ngay, viết liền một đoạn, không chèn ký tự xuống dòng**. Hook ngắn, thường 3–8 từ, phải gây tò mò từ đúng sự kiện nhìn thấy và nghe như người Mỹ thích câu cá trò chuyện với nhau, theo cơ chế Underfishing nhưng câu chữ nguyên bản. Ưu tiên cách nói/thuật ngữ câu cá Mỹ khi đúng hành vi và dụng cụ, theo mục 5; không dịch máy, giọng quảng cáo, nhồi slang hoặc dùng jargon sai để gây tò mò. **Không nhắc AI/công nghệ tạo video, không có dòng giải thích nguồn tạo và không có hashtag AI.** Ngay sau hook và một dấu cách có **3–5 hashtag khác nhau, đúng loài/ngữ cảnh**, trong cùng đoạn caption; không xuống dòng trước hashtag. Không xuất một mục TITLE hoặc HASHTAGS riêng. Giới hạn 3–8 từ chỉ áp dụng hook, không tính hashtag.

Nếu output theo JSON do người dùng yêu cầu, chỉ dùng ba khóa `first_frame_prompt`, `video_prompt`, `caption`; giá trị `caption` chứa cả hook và 3–5 hashtag về loài/câu cá/môi trường trong một đoạn; không chứa ký tự xuống dòng CR/LF hoặc escape `\n`, `\r`. Không thêm mảng `hashtags`.

Caption ở giai đoạn prompt phản ánh kết cục dự kiến. Khi nhận video thực tế, sửa caption theo điều nhìn thấy; nếu kết quả bị che thì dùng câu hỏi hoặc sự không chắc chắn phù hợp. Không tuyên bố hooked/caught/swallowed chỉ từ một cú áp sát hoặc một đám bùn. Hashtag không được dùng để che việc thiếu câu hook hoặc sai nội dung.

### Mẫu nhập liệu tùy chọn

```text
Number of videos: 1 by default
Species choice: Redfish | Muskie | Walleye | Any fish caught by anglers in the US [if absent and not supplied in context, ask these four choices and wait]
Specific other US angling species: [optional; if specified, use it without asking again]
Creative direction: a new original story for this request; avoid repeating examples or available previous concepts
Existing concept to revise: [optional; when supplied for revision, preserve it rather than invent a replacement]
US region / habitat: [optional]
Season / time of day / weather: [optional]
Water clarity / sediment source / natural colors: [optional]
Story key: twist | very fast species-appropriate action | other meaningful visible change [optional; AI must develop one]
Key timing: action onset strictly AFTER 5.0s, not at 5.0s; AI chooses a variable onset and leaves visible aftermath before 10.0s
Opening: immediate visual curiosity with meaningful setup through 5.0s; no early main strike, hookup, decisive escape or outcome reveal
Prey or lure: [optional]
Interaction mode: wild predation without tackle | baited angling | artificial lure [optional; infer from the requested concept]
Fishing method / rig / hook / main line / leader / visible accessories: [optional user constraints; AI researches and completes a coherent species- and location-appropriate setup under section 2A]
Trap or non-hook method: [only if relevant; verify the specific species, state, waterbody and season before portraying it as permitted]
Ending: take | miss | spit | ignore | occluded/uncertain [optional]
Beat plan: 5–8 variable beats, decimal-second boundaries allowed, continuous from 0.0 to 10.0s
Camera style: real-life fixed underwater observation by default; cinematic only if explicitly requested
Image model / Omni interface: [optional; do not invent unsupported parameters]
Caption angle: species | lure/rig | what happened | why it missed [optional]
Caption voice: curiosity grounded in the visible event; natural US angler language, fishing terms only when accurate
Hashtags: 3–5, appended after the hook with spaces in ONE paragraph; no newline
```

## 9. Ví dụ đầy đủ: một bộ ba đầu ra theo hợp đồng

**Ý tưởng đầu vào:** Muskie; hồ miền bắc Wisconsin, mép cỏ thủy sinh; theo một cá perch nhỏ rồi lao hụt. Ví dụ này minh họa cách viết, chưa được render/kiểm hình–âm; không phải kịch bản bắt buộc cho mọi video. Kích thước, cự ly và timecode là dàn cảnh, không phải số đo của một hồ hay ngưỡng sinh học.

**FIRST FRAME PROMPT**

> Vertical 9:16 still image, the exact t=0 frame of a fixed underwater action camera positioned 15 cm above a gravel-and-silt bottom at the edge of a cabbage weed bed in a cool northern Wisconsin freshwater lake in early autumn, on a lightly overcast afternoon with a gentle surface breeze. One anatomically accurate adult muskellunge, about 90 cm long, waits 1.8 m from the lens behind the left-side weeds, facing diagonally toward the lower-right foreground; its long pointed head and one eye are visible, its rear body partly screened by uneven leaves. Natural dark vertical markings remain attached to the same light olive body, pointed fins set far back near the tail. One small yellow perch, about 12 cm long, is 0.9 m from the lens in the lower-right third, facing left, separated from the muskie by open water. No lure, hook, fishing line or second predator. Soft diffuse daylight from the clouded sky filters from above at about 2 m depth; no strong sunlight caustics. The breeze produces only slight natural variation in surface-transmitted light, without a staged spotlight. A restrained natural green cast consistent with the chosen lake conditions, kept distinct from moderate horizontal visibility limited by fine suspended matter: gravel, baitfish and weed edges sharp near the lens; the muskie at 1.8 m a softer but recognizable silhouette; background vegetation farther away loses contrast gradually. Enough visibility for this visual predator to track nearby prey, not opaque brown mud. A few irregular suspended particles, no artificial beam or excessive caustics. The gravel bottom has a thin patchy coating of loose fine silt in a few depressions, not a deep mud bed; it is undisturbed at this instant. Do not improve water clarity or selectively spotlight either fish to make the scene prettier. Ordinary field-camera framing, restrained natural colors and exposure, moderate wide-angle perspective from a physically placeable fixed camera, no cinematic hero angle, dramatic bokeh or teal-orange grading; no text, logo, diver or rendered look.

**OMNI FLASH VIDEO PROMPT**

> Use the attached `<FIRST_FRAME>` image as the opening frame at t=0. Generate exactly 10 seconds, vertical 9:16, one continuous unbroken locked underwater observation, no cuts, zoom or reframing. Begin with the same approximately 90 cm muskellunge partly screened by left weeds at 1.8 m from the lens and the same 12 cm yellow perch in the lower-right foreground at 0.9 m. Preserve both animals' anatomy, scale and markings, the gravel-and-silt bottom, plants, natural green lake-water color, visibility, 2 m depth and soft early-autumn overcast-afternoon light. This is an ordinary fixed field camera, not a cinematic viewpoint. [0.0–1.3s] The perch advances slowly left with small tail movements while the muskie watches. [1.3–2.3s] The muskie eases out of the left cover with restrained tail propulsion. [2.3–4.0s] The perch notices the approach, angles its head right and begins a smooth turn toward open water. [4.0–6.4s] The muskie adjusts its heading along the weed edge as the perch continues forward, keeping a visible gap; only near the end does its tail bend in preparation for one lunge. No attack, bite, decisive escape or outcome reveal from 0.0 through 5.0s. [6.4–6.7s] KEY ONSET at 6.4s, strictly after 5.0s: a strong tail stroke drives a fast natural lunge; at about 6.5s the perch bends sharply and darts right, and the jaws close just behind it in a visible miss. No teleporting or contact through another body. [6.7–8.1s] The perch continues through the right edge; the muskie brakes with fin adjustments. Only if the near-bottom tail stroke reaches a loose fine-silt patch does a small localized cloud begin there after the stroke; otherwise the gravel remains undisturbed. Rocks stay fixed. [8.1–10.0s] The muskie turns back in a continuous arc while the localized silt disperses, leaving the escape path visibly empty. Keep baseline water haze, weather-driven lighting and camera perspective unchanged. Sound design: loud, clear, full-bodied environmental and action audio continuously from 0.0 to 10.0s. Keep a clearly audible natural lake-water ambience bed throughout. Layer synchronized local water movement with the fish movements in each beat, vegetation contact only where it occurs, a prominent but physically proportionate water disturbance during the 6.5s lunge, and continued water movement during braking and turning. No silent gaps or fade to silence; maintain strong overall mix volume with distinct layers and controlled peaks, no clipping or distortion. No music, speech, cinematic hit, whoosh, surface splash, persistent bubbles, extra animals, text or logo.

**CAPTION**

```text
How did that muskie miss? #Muskie #MuskyFishing #Underwater #FreshwaterFishing
```

## 10. Kiểm tra chất lượng trước khi dùng prompt hoặc đăng video

1. **First frame:** chụp ảnh đầu ra, so với prompt. Có đúng **t=0** không? Mồi đã bị cắn sớm? Cá có đúng loài, số lượng, sinh cảnh/vùng Mỹ? Màu cơ thể/nước/đáy, cây, không gian, mùa/giờ/thời tiết và ánh sáng có cùng hợp lý không? Góc máy có thể đặt thật, phối cảnh và màu như footage ngoài đời thay vì ảnh điện ảnh không được yêu cầu? Điểm nhận dạng có nằm ở vị trí sinh học đúng?
2. **Timeline và cảnh key:** xác nhận có 5–8 beat linh hoạt nối liên tục từ 0.0 đến 10.0s; kiểm vật ở đúng các ranh beat đã viết, không dùng lịch lấy mẫu cố định mỗi hai giây. Cá, mồi, dây, cỏ, đá không tự sinh/biến mất; quãng đường/hướng bơi liên tục. Chỉ ra **key có twist/hành động nhanh hoặc đổi trạng thái tạo câu chuyện**, có tín hiệu trước và hậu quả sau. Đo thời điểm bắt đầu hành động key thật trên video: phải **sau 5.0s**, không ở hoặc trước 5.0s, kể cả khi đỉnh muộn hơn. Phần 0–5s có hook và tiến triển, chưa có cú đớp/kết quả chính; sau key còn đủ hậu quả thấy được trước 10s. Không chấm đạt bằng cách đổi tên cú cắn sớm thành chuẩn bị. Quanh key nhanh, xem từng frame hoặc bước nhỏ đủ phân giải động tác; lấy mẫu 0,25s có thể bỏ sót cú đớp vài phần mười giây. Không chấm đạt chỉ vì đã viết nhãn KEY trong prompt.
3. **Môi trường, vật lý và quang học — kiểm trên ảnh/video thật:** đối chiếu điều kiện đã nghiên cứu, không chỉ lời prompt. Màu nước và độ trong được kiểm riêng: có hợp vùng/ánh sáng/thời tiết không; vật xa có giảm chi tiết/tương phản/màu theo đường truyền qua nước không, hay chỉ là ảnh rõ phủ màu? Chủ thể có nét, sáng hoặc bão hòa bất thường so với cùng môi trường không? Hạt, mảnh hữu cơ, vật liệu đáy và lớp mịn có đúng loại/mức không; có rác/bong bóng/mây đục vô nguồn không? Nếu có bùn, nền/cự ly/lực/hướng dòng có giải thích được điểm phát sinh và lan/lắng sau tác động không; đá/sỏi lớn vẫn ở lại. Kiểm nguồn sáng, phối cảnh và góc camera chìm có thể đặt thật; không dùng nhiễu/méo/tối góc để che lỗi. Nếu khó thấy, sửa cự ly/bố cục chứ không tăng độ trong trái cơ sở. Sửa đúng thuộc tính sai rồi kiểm lại; không chấm đạt chỉ vì ảnh đẹp, màu nước hợp hoặc đã ghi “photorealistic”. Chỉ kết luận điều quan sát được và giữ rõ điểm chưa xác minh.
4. **Sinh học:** redfish tìm mồi ở nước lợ/ven biển, walleye hợp ánh sáng thấp hoặc nước đục, muskie là cá phục kích đơn độc; cấu trúc vây, mắt, miệng và hoa văn không đổi. Kiểm lại tư liệu loài khi dùng địa hình/season khác.
5. **Chuỗi hành vi:** kiểm từng beat trước key theo chính timecode đã chọn xem có tín hiệu/tiến triển quan sát được; con mồi sống không giữ cùng tư thế suốt nửa đầu khi cá tiến gần. Con mồi có phản ứng trước khi chạy trốn; chân/vây/đuôi tạo lực nhìn được; đường thoát đi về đúng hốc hoặc mép khung đã định ở t=0; cá có phản ứng tương ứng; sau sự kiện còn dấu vết vật lý đúng chỗ. Nếu kết cục bị che, caption giữ mức chưa chắc chắn.
6. **Âm thanh và caption:** nghe bằng loa điện thoại ở mức bình thường, đối chiếu hình ở từng beat và key. Xác nhận cả hai lớp môi trường + hành động có mặt trong bản mix, volume lớn/rõ xuyên suốt từ 0 tới 10s, không quãng câm hoặc fade về im lặng; môi trường không bị mất khi hành động chậm. Các tiếng hành động có nguồn/thời điểm đúng, key nổi bật và hậu quả còn nghe được; bản mix không chỉ có một hit to trên nền nhỏ, không rè/méo/clipping. Không nhạc/voice hoặc hit điện ảnh vô nguồn trong bản chuẩn. Caption chỉ nói điều video chứng minh hoặc đặt câu hỏi đúng mức; gồm hook ngắn gây tò mò từ đúng chi tiết hình, tiếng Anh Mỹ tự nhiên với người thích câu cá, thuật ngữ câu cá dùng đúng nghĩa; hook và 3–5 hashtag liên quan viết liền một đoạn, không ký tự xuống dòng, không tách TITLE/HASHTAGS; không nhắc AI/công nghệ tạo video hoặc dùng hashtag AI.
7. **Thông số và dấu chèn:** file cuối 9:16, đúng 10 giây; xem lại bằng kích thước điện thoại. Kiểm góc hình ở first frame, video vừa sinh và file xuất để biết chữ/biểu tượng xuất hiện ở bước nào. Nếu là thành phần AI tự vẽ, sửa prompt và tạo lại; nếu là dấu bắt buộc của công cụ/nền tảng, ghi nhận đó là giới hạn của bản xuất và chỉ dùng lựa chọn xuất không dấu khi công cụ cho phép. Đừng mô tả nó như chi tiết tự nhiên trong cảnh. Nếu một mục chất lượng hỏng, sửa lỗi đó và tạo lại khi công cụ cho phép. Không có prompt nào bảo đảm mọi lần sinh đều trông thật; chất lượng phải được kiểm bằng video đã tạo.

8. **Hợp đồng đầu ra:** có đúng FIRST FRAME PROMPT, OMNI FLASH VIDEO PROMPT và CAPTION cho mỗi video; prompt ảnh chỉ là t=0; prompt video dùng đúng ảnh đó, không lệch số lượng/hướng/cảnh; 5–8 beat linh hoạt nối liên tục đủ 10s, cho phép mốc thập phân; một cảnh key bắt đầu sau 5.0s tạo câu chuyện, phần đầu có tiến triển và phần cuối còn hậu quả; sound design tích hợp; caption có hook gợi tò mò, giọng người câu cá Mỹ tự nhiên và 3–5 tag khác nhau viết liền một đoạn, không xuống dòng. Các khối có thể sao chép riêng, không còn chỗ trống cần người dùng tự điền. Chỉ tag `<FIRST_FRAME>` là ký hiệu media hợp lệ, phải đi cùng ảnh input thực tế.
9. **Trung thực về kiểm chứng:** không ghi đã xem, nghe, đo, render, đạt QA hoặc viral nếu chỉ đọc hướng dẫn/viết prompt. Các dBFS kế thừa là số trong hồ sơ nguồn, không phải mục tiêu âm lượng hoặc kết quả đo mới. Bản prompt được kiểm về cấu trúc/nhất quán vẫn cần kiểm video thực tế.

10. **Chọn loài và độ mới:** thiếu loài/quyền chọn thì đã hỏi đúng bốn lựa chọn và chờ chưa? Nếu đã có thì không hỏi lại. Khi tạo mới, ý tưởng có khác thực chất với ví dụ/lịch sử hiện có về key, tương tác hoặc kết cục không, hay chỉ đổi tên/màu/thời tiết? Loài bất kỳ có đúng là cá được câu ở vùng Mỹ đã chọn và có hồ sơ sinh thái phù hợp không? Khi sửa clip cũ, có giữ câu chuyện đã chọn không?

11. **Dụng cụ và phương pháp câu:** nếu có, đã chốt một bộ đúng loài/vùng/mùa theo mục 2A chưa? Kiểm bait sống/chết/lure, loại/cỡ/số móc, leader, main line, điểm nối và phụ kiện thực sự cần; quỹ đạo, tải, chùng/căng, cách nhận lực đúng bộ. Nếu có bẫy/lưới/thiết bị đặc biệt, đã phân biệt với rig và kiểm quy định cụ thể chưa? Cảnh săn mồi tự nhiên không bị tự thêm hook/line. Tư liệu cũ/thông số sản phẩm không bị gọi là luật hiện hành.
12. **Giao diện chọn cá:** khi thiếu loài, dùng bốn lựa chọn tương tác nếu công cụ hỗ trợ, có đường nhập loài khác; nếu không, dùng bốn lựa chọn chữ. Chỉ tiếp tục khi nhận câu trả lời thật, không coi đáp án chọn sẵn là xác nhận.

## 11. Nhật ký cập nhật ngày 15/10/2026

- Giữ phần hướng dẫn sinh thái, quang học, nước đục, hành vi con mồi và dữ liệu audio đã có; làm rõ chúng thuộc hồ sơ nền chứ không phải lần nghe/đo mới.
- Thêm mục 0 để file tự đủ bối cảnh, nêu cơ chế nghiên cứu, chất lượng bằng chứng, mặc định khi thiếu đầu vào và cách làm khi không có web/media.
- Chuẩn hóa ba đầu ra; đổi TITLE thành CAPTION; áp dụng 3–5 hashtag như một phần của caption; chỉ tính giới hạn từ cho hook.
- Làm rõ ảnh t=0 → ảnh input thực tế → một video liền mạch; phân biệt ảnh mở đầu và ảnh reference theo giao diện Omni.
- Sửa ví dụ cho đủ key moment, trạng thái đầu, âm thanh và caption có hashtag; gắn nhãn chưa render.
- Thêm checklist đầu ra; làm rõ dây có thể căng sẵn khi đang kéo lure và cá có thể lướt theo quán tính, không ép mọi cảnh cùng nhịp sinh học.

### Bổ sung v1.1 — ngày 15/10/2026

- Gắn link Drive báo cáo 20 Reel và khuyến nghị đọc để hiểu/phát triển, không bị giới hạn bởi nghiên cứu.
- Yêu cầu cảnh key có twist, hành động cực nhanh hoặc một đổi trạng thái tạo câu chuyện, vẫn đúng sinh học/vật lý.
- Bỏ khuôn beat hai giây và giới hạn thời lượng beat cũ; thay bằng 5–8 beat linh hoạt, cho phép số thập phân, timeline liên tục đúng 10s.
- Bổ sung khóa môi trường/màu sắc/không gian/mùa/giờ/thời tiết và camera đời thực cho first frame; điện ảnh chỉ khi được yêu cầu.
- Đồng bộ mục quy trình, hợp đồng đầu ra, ví dụ và checklist; giữ các nghiên cứu, dữ liệu âm thanh, tiêu chuẩn sinh học/vật lý và caption 3–5 hashtag không xung đột.

### Bổ sung v1.2 — ngày 15/10/2026

- Theo yêu cầu người dùng, caption chỉ có câu hook tự nhiên và 3–5 hashtag về loài/câu cá/môi trường; không nhắc AI hoặc công nghệ tạo video, không thêm dòng giải thích nguồn tạo, không dùng hashtag AI.
- Đồng bộ quy trình, quy chuẩn caption, hợp đồng đầu ra, JSON, ví dụ và checklist. Các thay đổi v1.1 về link nghiên cứu, key, nhịp 5–8 beat linh hoạt và first frame đời thực được giữ nguyên.

### Bổ sung v1.3 — ngày 15/10/2026

- Tích hợp đầy đủ ghi chú người dùng về nghiên cứu và tái hiện môi trường nước: điều kiện thực tế; màu nước/độ trong riêng; hạt có cơ sở; khuấy trầm tích theo đáy và lực; góc camera thật; QA bằng ảnh thực tế.
- Đồng bộ quy trình nghiên cứu, FIRST FRAME PROMPT, OMNI FLASH VIDEO PROMPT, ví dụ Muskie và checklist. Không chỉ nối một phụ lục mà để phần giao việc cũ giữ chỉ dẫn trái nhau.
- Phân biệt giả định/số dàn cảnh với dữ liệu địa điểm đã kiểm; khi cần dễ nhìn hơn, đổi cự ly/bố cục thay vì làm nước trong hoặc chủ thể sáng/nét hơn thực tế.
- Giữ nguyên link nghiên cứu 20 Reel, cảnh key/twist/hành động nhanh hợp loài, 5–8 beat linh hoạt đủ 10s, dữ liệu âm thanh và caption hook + 3–5 hashtag không nhắc AI.

### Bổ sung v1.4 — ngày 15/10/2026

- Bỏ mặc định Redfish và việc tự chia ba loài khi đầu vào chưa chọn loài. Thiếu lựa chọn thì hỏi Redfish / Muskie / Walleye / loài cá được câu bất kỳ ở Mỹ rồi chờ; đã có lựa chọn hoặc quyền tự chọn thì triển khai, không hỏi lại.
- Mở phạm vi cá chính theo lựa chọn người dùng sang loài cá được câu ở Mỹ khác, với yêu cầu nghiên cứu riêng cho loài/vùng đó; giữ ba bảng loài hiện có làm cơ sở tham khảo.
- Mỗi lần tạo mới phải có ý tưởng mới phù hợp, không lặp mặc định Redfish–cua hoặc các ví dụ; sửa clip cũ thì giữ ý tưởng đã chọn.
- Chỉ đồng bộ các phần chọn loài/sáng tạo/đầu vào liên quan; nội dung môi trường, sinh học, quang học, vật lý, âm thanh, nhịp, ví dụ và caption giữ nguyên.

### Bổ sung v1.5 — ngày 15/10/2026

- Âm thanh bắt buộc gồm môi trường + hành động, volume lớn/rõ và xuất hiện xuyên suốt 0–10s; không nền gần câm hoặc chỉ có một tiếng tại key.
- Đồng bộ quy trình, công thức/đoạn sound design mẫu, lỗi audio, video prompt ví dụ và QA. Tiếng vẫn khớp nguồn/hành động/môi trường; bản mix lớn nhưng sạch, không clipping/rè/méo.
- Giữ nguyên dữ liệu audio tham chiếu như hồ sơ nghiên cứu, không sửa số đo để khớp lựa chọn sáng tạo mới. Các nội dung ngoài âm thanh được giữ nguyên.

### Bổ sung v1.6 — ngày 15/10/2026

- Thêm mục 2A về bộ mồi–móc–dây–leader–rig–phương pháp phù hợp Redfish/Muskie/Walleye và loài cá khác tại Mỹ, với nguồn nghiên cứu và cách chọn theo từng cảnh; phân biệt prey tự nhiên, natural bait và artificial lure.
- Quy định sơ đồ nối, số móc/phụ kiện, vật lý tải/phao/mồi, nhận lực, âm thanh dụng cụ và kiểm tính nhất quán trên ảnh/video. Phân biệt rig với bẫy/lồng thật; phương pháp đặc biệt phải đối chiếu loài/bang/thủy vực/mùa, không tuyên bố hợp lệ toàn Mỹ.
- Ưu tiên câu hỏi chọn loài có đáp án bấm được khi giao diện hỗ trợ, cho nhập loài khác; có phương án bốn lựa chọn chữ khi không hỗ trợ. Đáp án chọn sẵn không phải câu trả lời, không hỏi lại khi đã có loài/quyền chọn.
- Đồng bộ quy trình nghiên cứu, hai prompt, mẫu đầu vào và QA trong đúng phạm vi trên. Giữ nguyên nghiên cứu nền, môi trường/quang học, ý tưởng mới, key/5–8 beat đủ 10s, công thức/dữ liệu âm thanh và caption hook + 3–5 hashtag không nhắc AI.

### Bổ sung v1.7 — ngày 15/10/2026

- Chỉ điều chỉnh caption: hook và 3–5 hashtag viết liền thành một đoạn, không xuống dòng; đồng bộ cả chuỗi JSON, mẫu đầu vào, ví dụ và QA.
- Caption phải gợi tò mò từ chi tiết đúng trong clip, tiếng Anh Mỹ tự nhiên với người thích câu cá; ưu tiên cách nói/thuật ngữ câu cá phù hợp, không nhồi slang hoặc dùng sai hành vi/dụng cụ.
- Giữ nguyên các nội dung ngoài caption của v1.6, gồm nghiên cứu, chọn loài, ý tưởng, môi trường, dụng cụ câu, hai prompt hình/video, timeline và âm thanh.

### Bổ sung v1.9 — ngày 15/10/2026; chỉnh trực tiếp từ v1.7, bỏ qua v1.8

- Hành động key phải bắt đầu sau 5.0s, không phải đúng 5.0s; không chỉ dời đỉnh hoặc gọi một phản ứng muộn là key sau cú cắn sớm.
- Tách hook thị giác đầu clip với key: 0–5s có kỳ vọng và tiến triển hợp tự nhiên, không chờ bất động/slow motion/lặp hành vi; sau key còn hậu quả nhìn thấy trước 10s. Thời điểm cụ thể linh hoạt, không cố định cho mọi video.
- Đồng bộ quy trình, bố trí first frame, chỉ thị video, ví dụ, mẫu nhập và QA; ví dụ đầy đủ đổi onset sang 6.4s để minh họa không khóa ở sát giây 5. Không sửa dữ liệu nghiên cứu/audio kế thừa hoặc suy ra bảo đảm retention.
- Dùng nguyên v1.7 làm nền; không kế thừa v1.8. Các nội dung ngoài thời điểm key và nhịp chuẩn bị/hậu quả được giữ nguyên, gồm caption một đoạn + 3–5 hashtag, dụng cụ, môi trường và yêu cầu âm thanh.
