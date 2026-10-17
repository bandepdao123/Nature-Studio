# Gói A–B–C — cập nhật skill dùng chung nhiều Project

Date: 2026-10-17 | chayvideo v2.3 | clonevideo v1.1 | VERSION 1.5, chưa phát hành

## Phạm vi được duyệt và đã làm

- **A:** Bước G của Story Development v1.1 đối chiếu chi tiết/quan hệ quyết định với hình, âm, lời hoặc nhịp trong prompt. Kiểm thiếu/mâu thuẫn và chỉ đạo phụ gây nhiễu; giữ cấu tạo/thao tác/tính đúng, không rút theo số từ. Chỉ ghi quyết định đáng giữ vào hồ sơ hiện có. Cảnh quan/biến đổi chậm không bị ép cao trào; narration được xét theo Project. Phân biệt kiểm thiết kế với quan sát media thật.
- **B:** Nhánh revision v1.1 phân biệt yêu cầu thay đổi rõ với xử lý lỗi; xét đúng nguồn cần sửa và phần liên đới. Chỉ có phản hồi người dùng thì ghi nguồn, không tự nhận đã xem media. Nguyên nhân chưa rõ giữ là giả thuyết; không kết luận model không có khả năng từ một lần lỗi. Giữ kế thừa/binding đã triển khai; caption-only vẫn dùng đường nhẹ.
- **C:** Chuẩn chuyển thể v1.1 và analysis v1.1 nối quan sát với chức năng cần cho bản đích. Thành phần bị bỏ/thay được xét để giữ bằng cách khác, thay hoặc chủ động bỏ theo brief/Project. Cho phép gộp/tách event, retime hợp lý; đủ ID không chứng minh đúng nghĩa. Role có thể là cảnh vật, event là đoạn biến đổi/trạng thái có ý nghĩa, key là phần quan trọng chứ không bắt cao trào. Không bịa dữ kiện để đủ schema.

Hai entry skill tăng version để truy nguyên, không chép lại quy trình. Không sửa format/Project, helper/schema/template, routing caption, registry/quota hoặc memory policy. Không thêm hồ sơ bắt buộc, bước duyệt, model/API/media tools. Không tạo production, media hay ID để kiểm cập nhật; không commit/push.

Nguyên tắc tham khảo từ Hypit tại commit dc2b7a8f31b1ef1443a79ca448548d69e3ceb6a0: [Brief và Treatment](https://github.com/hypit-ai/hypit/blob/dc2b7a8f31b1ef1443a79ca448548d69e3ceb6a0/skills/hypit/references/creation/brief.md), [Transformations](https://github.com/hypit-ai/hypit/blob/dc2b7a8f31b1ef1443a79ca448548d69e3ceb6a0/skills/hypit/references/creation/transformations.md). Quyết định triển khai là gói đã được người dùng duyệt; không coi nguồn tham khảo là chứng minh hiệu quả sáng tạo hoặc quyền thay chính sách Project.

## Kiểm thiết kế bằng tình huống

Fixture và handling output được ghi trong workspace tạm ngoài repo; đường dẫn được giữ ở bản sao phục hồi ngoài repo. Dưới đây là kết quả **walkthrough do cùng agent soạn và đối chiếu hướng dẫn**, không phải chạy agent độc lập, video analysis hoặc human audience validation.

| Ca / đầu vào fixture | Handling output đã ghi / đối chiếu |
|---|---|
| Cảnh quan 24s, bóng mây qua sườn núi, không yêu cầu cao trào | Giữ biến đổi ánh sáng/bề mặt và nhịp; không thêm động vật, cú lao, key sau 5s hoặc kết cục đóng |
| Giải thích 35s, lời kể mang thông tin so sánh vòng cây | Giữ narration theo Project; tắt lời chỉ chẩn đoán hình, không thành lệnh bỏ lời |
| Thao tác 16s, hai chốt khóa và gioăng phải đúng, yêu cầu prompt gọn | Giữ số chốt và quan hệ gioăng–khóa; chỉ bỏ tính từ lặp/chỉ đạo phụ không cần |
| Mẫu có cut cận cảnh lúc đổi hướng, đích một shot và cần thấy đổi hướng | Thay cách làm rõ bằng bố cục/cự ly/quỹ đạo phù hợp; ghi lựa chọn vào adaptation, không thêm sự kiện |
| Người dùng muốn chuyển mẫu hồi hộp thành quan sát bình tĩnh | Chủ động bỏ chức năng gây hồi hộp theo quyền đã giao, không cố giữ vì giả thuyết hấp dẫn |
| Hai event nguồn gộp một đoạn đích, phản ứng được tách rõ hơn | Cho phép mapping nhiều–một/một–nhiều; kiểm quan hệ/tính đúng, không suy pass ngữ nghĩa từ ID |
| Sửa hướng nhìn, người dùng phản ánh mất nét nhưng chưa cung cấp file | Sửa phần được giao và bố cục liên đới; mất nét là phản hồi được dẫn nguồn, nguyên nhân chưa rõ, không đổi chuyện hoặc quy lỗi chắc cho model |
| Chỉ sửa caption với nguồn kế thừa rõ | Dùng nhánh caption, giữ prompt/chuyện/binding ảnh, không phân tích mẫu hoặc mở lại Story Development |

Đối chiếu ngược những cách xử lý sai: thêm cú cắn/cao trào vào cảnh núi; bỏ narration dù Project cho phép; bỏ số chốt để ngắn prompt; giữ hồi hộp trái brief; ép một event bằng một beat; nhận đã xem render chưa có. Hướng dẫn mới có điều kiện loại từng cách xử lý đó. Đây vẫn là self-review thiết kế, chưa chứng minh agent/model luôn làm đúng khi dùng thật.

## Kiểm cấu trúc và hồi quy

- Ba profile fixture tạm: landscape 24s, narrated-explanation 35s, precise-procedure 16s. Mỗi profile qua reference_video.validate và output.validate cho new/reference ngoài Underwater: **9/9 kiểm cấu trúc đạt**. Không sửa schema/helper. Fixture dùng bytes không phải media phát được; coverage/evidence là khai báo giả lập, không được dùng làm bằng chứng đã xem/nghe hoặc QA nội dung thật.
- `python -m unittest discover -s scripts/tests`: **118/118 đạt**. Không thêm test khớp câu chữ; bộ kiểm phần mềm không chứng minh phương pháp sáng tạo hiệu quả.
- Hai skill qua quick_validate bằng Python UTF-8, PyYAML phục vụ kiểm nằm ngoài repo. Memory validator đạt, 1 lesson không đổi trạng thái.
- Liên kết file mới/sửa không hỏng. `git -c core.whitespace=cr-at-eol diff --check` đạt; giữ CRLF có trước, không chuẩn hóa file ngoài phạm vi.
- Backup trước ghi gồm nguồn sẽ sửa, status/diff local và hash bảo vệ. **393 file được bảo vệ không thay đổi/mất**, gồm production/local registry-cache/Memory, scripts/tests và toàn bộ Project. Không áp deletion/ghi đè dữ liệu riêng.

## Chi phí vận hành và giới hạn

Sáu nguồn hướng dẫn/entry tăng ròng **3.699 ký tự Unicode** so với snapshot trước đợt này; changelog/báo cáo là hồ sơ cập nhật riêng. Không thêm file hướng dẫn phải nạp, tool call bắt buộc hoặc dữ liệu schema mỗi video; caption-only không đọc phần mới. Đây là số ký tự source-text, không là token/usage thực tế hay bằng chứng tiết kiệm chi phí.

Chưa chạy thử agent độc lập, render, quan sát hình/âm thật, A/B model hoặc đo token/thời gian/retention/view. Các báo cáo trước giữ nguyên trạng thái tại thời điểm ghi; VERSION vẫn 1.5 cho tới khi được giao phát hành.
