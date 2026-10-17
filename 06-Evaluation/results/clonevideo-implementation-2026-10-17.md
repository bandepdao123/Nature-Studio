# Clonevideo — triển khai và QA

Date: 2026-10-17 | clonevideo v1.0 | chayvideo v2.1 | VERSION workspace giữ 1.5, chưa phát hành.

## Thiết kế

Clonevideo tiếp nhận file/link, phân tích hình/âm có timecode/coverage/provenance, ánh xạ vai trò và hành động sang đối tượng/bối cảnh đích. Đây là chuyển thể có chủ đích; không áp ngưỡng phải khác chuyện mẫu. Vẫn giữ các gate tự nhiên, Project, prompt/caption, audio và QA thật. Mặc định đầu ra bốn mục như chayvideo; phân tích/mapping giữ local.

Lõi viết prompt/lưu hồ sơ đã chuyển từ workflow riêng chayvideo sang 00-Standards/video-prompt-workflow.md. File cũ chỉ trỏ về lõi để giữ liên kết. Hai skill dùng cùng quy chuẩn Project, model, helper output/ID/history. Context mode reference kế thừa recipe new bằng alias, không sao chép danh sách nguồn; thiếu alias có fallback new. Hash dependency gồm lõi và nhánh tham chiếu để packet cũ hết hạn khi nguồn đổi. Sửa dispatcher chỉ dành chayvideo hoặc phân tích media riêng không tự đổi chính sách của nhánh khác.

Helper reference_video.py không xem/nghe video; nó kiểm hồ sơ AI đã phân tích, coverage/timeline/IDs/evidence khai báo, hash nguồn và brief. File nguồn đổi, analysis đổi, thiếu review toàn thời lượng, sampled frames tự nhận full, audio chỉ được trích xuất hoặc audio không truy cập mà có cue đều bị phát hiện theo cấu trúc. Helper không chứng minh AI trung thực/hiểu đúng hoặc xác nhận hành vi/nguồn âm.

## Các tình huống đã QA ở mức hướng dẫn

- Chỉ link không mở được: xin file/quyền truy cập, chưa giao bản full dựa trên thumbnail/transcript; không cấp video ID lúc thiếu nguồn.
- Chỉ có frame hoặc chưa nghe audio: partial/unavailable, không nhận full; draft giới hạn chỉ sau chấp thuận thật, không im lặng đi tiếp.
- Cá/con mồi đổi sang loài khác: giữ chức năng/nhân quả, nghiên cứu lại tạo lực, chỗ trú, cự ly, đồng loài/cây/đáy/dụng cụ và âm; không giữ động tác trái đặc tính loài.
- Mẫu nhiều cut/key sớm/video dài: mapping chỉ rõ phần dùng/retime/đổi camera theo Project; không tăng tốc phi lý hoặc ép đứng chờ, không âm thầm bỏ hành động cốt lõi đã khóa.
- Mẫu có nhạc/voice nhưng Project cấm: ghi khác biệt và thay âm đúng nguồn, không tự gọi âm nhạc là tiếng môi trường.
- Đổi target sau khi có analysis hợp lệ: dùng lại hồ sơ, chỉ xem lại phần thiếu/mơ hồ; Project đổi không buộc đọc lại toàn video nếu nguồn media nguyên vẹn.
- Clip ngoài Underwater: catalog/Project phù hợp hoặc hỏi khi chưa có, không tự áp cá/10s/key sau5s cho mọi thiên nhiên.

Đây là QA thiết kế/đối chiếu yêu cầu, không phải test hành vi bằng agent độc lập hoặc phân tích một video thật.

## Kiểm thử

Chạy unittest trên workspace tạm; kiểm chung cả new và reference, alias/fallback/cycle, cập nhật nguồn/lõi làm packet cũ stale, output gate chung, coverage hình/âm, audio vắng thật, ID tham chiếu sai, event đồng thời, shot hở/chồng, số thời gian lỗi, source hash đổi, URL không đủ freshness, remote version khác, brief không ghi đè/thoát runtime, và verify CLI phát hiện analysis thay đổi.

Kết quả cuối: **99/99 test đạt**, gồm 76 test Plan 01/hệ thống trước đó và 23 test mới cho reference/clonevideo. Hai skill qua quick_validate, memory validator giữ nguyên lesson/state, liên kết nội bộ mới không hỏng, git diff --check sạch. Hash baseline ngoài repo đối chiếu 365 file runtime có sẵn: không đổi/mất. Backup giữ bản Plan 01 trước thay lõi; không ghi đè production/registry/quota/media hoặc ba manifest local cũ.

Chưa chạy native video/audio analysis, render, API hoặc thử nghiệm model/khán giả. Không quảng cáo đã có công cụ đọc được mọi link hoặc phân tích từng frame. Khi sử dụng, skill phải kiểm khả năng media thật của phiên và xử lý phần thiếu theo hướng dẫn. Chưa commit/push hoặc nâng VERSION phát hành; không đo lại token 6.1 Sol trong việc này.
