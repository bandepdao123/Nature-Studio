# Hợp đồng đầu ra — v1.3

Updated: 2026-10-16 | Origin: approved guide v1.9 + user /chayvideo requirements

## Hợp đồng hiện hành khi gọi /chayvideo

Theo điều chỉnh mới nhất của người dùng ngày 2026-10-16, trả bốn mục: **Ý TƯỞNG** (tiếng Việt), **FIRST FRAME PROMPT** (tiếng Anh), **VIDEO PROMPT** (tiếng Anh), **CAPTION** (tiếng Anh Mỹ tự nhiên, phù hợp người câu cá Mỹ, có 3–5 hashtag đúng cảnh). Mỗi prompt là một đoạn văn không xuống dòng trong nội dung; beat/timecode và sound design viết liền trong video prompt. Caption có hook ngắn gợi tò mò, thường 3–8 từ, hashtag nối cùng đoạn, không nhắc AI. Không xuất bản dịch song ngữ trừ khi được yêu cầu. Hợp đồng này áp dụng cả khi gọi /chayvideo lẫn khi skill tự nhận dự án từ đặc trưng; thay yêu cầu v1.1 toàn bộ tiếng Việt. Cấu trúc Omni Flash theo model profile: ảnh mở đầu → thời lượng/tỷ lệ/camera → tính nhất quán cảnh → chuyển động/beat → Sound design → loại trừ ngắn; không bịa tham số hoặc hứa model bảo đảm timecode.

Trước khi chọn ý tưởng, thực hiện bước rà trùng trong [skill chayvideo](../../.agents/skills/chayvideo/SKILL.md): kiểm chat truy cập được, ledger, SUMMARY/concept và hồ sơ thực, kể cả nháp đã giao và ý tưởng bị loại. So cơ chế tương tác/key/kết cục, không chỉ tên loài hoặc chữ trùng; ghi bằng chứng so sánh và giới hạn lịch sử trong concept. Lưu bản drafted và cập nhật ledger để lần sau tra được.

JSON khi được yêu cầu dùng bốn khóa `idea`, `first_frame_prompt`, `video_prompt`, `caption`; hai prompt và caption không chứa CR/LF. Giữ đầy đủ yêu cầu nội dung kỹ thuật dưới đây: t=0, loài/môi trường/dụng cụ, 10s 9:16, 5–8 beat liên tục, key bắt đầu sau 5.0s, âm thanh hai lớp và caption đúng bằng chứng. Chế độ này thay yêu cầu ba mục/tên mục/ba khóa JSON trong phần kế thừa và checklist cũ; các yêu cầu khác vẫn áp dụng. Yêu cầu trực tiếp mới của người dùng được ưu tiên.

## Hợp đồng nền ngoài chế độ /chayvideo

Phần dưới giữ nội dung v1.9 để truy nguyên và dùng ngoài chế độ /chayvideo. Khi chạy skill, áp dụng thay đổi ở trên, không xuất lại ba mục tiếng Anh.

Các tham chiếu mục đánh số dưới đây thuộc hướng dẫn baseline v1.9. Trong kho mới: loài/địa điểm/dụng cụ ở Knowledge, chọn loài ở PROJECT.md, nhịp/audio/QA ở format.md. Chỉ thị đủ dùng được nhập nguyên để không làm mất ràng buộc.

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
