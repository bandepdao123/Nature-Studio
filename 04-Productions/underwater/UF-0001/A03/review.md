# Video review — A03
Date: 2026-10-16 | Level: video-reviewed (frames) + measured-audio, chưa nghe audio
Source: source-video.mp4, người dùng gửi C:/Users/Admin/Downloads/Muskellunge_hunting_white_sucker…_20261016100904.mp4
SHA256: 747C1D3537DD202150717EAED801925994A5D68C7C96CCB5271F5E8C1F6402B4
Actual generation prompt/model/settings: unknown; metadata encoder Google không xác định model hoặc prompt thực dùng.

## Phạm vi kiểm
Đọc ffprobe, xem contact sheet 4fps toàn clip, frame nguyên kích thước0/1/2s; xem tất cả28frame liên tiếp n128–155 (5.333–6.458s) quanh sự kiện dự kiến. Chưa phát/nghe audio; phân tích ebur128 đo loudness, không nhận dạng nguồn âm bằng nghe. Không xem liên tục mọi frame toàn clip; không chứng nhận không có lỗi nhỏ giữa các mẫu.

| ID | Time | Observation | Verdict | Correction |
|---|---|---|---|---|
| V01 | toàn clip | video720x1280,24fps,240frames,10.000s; AAC stereo48kHz10.005s | pass thông số hình; mux lệch5ms được ghi đúng | giữ10s9:16 |
| V02 | 1.000 và2.000s | cùng lúc có hai cá nhỏ: một phía xa trên gỗ, một tiền cảnh dưới/phía trước gỗ; xem frame-1.png/frame-2.png | fail số lượng/identity, nghiêm trọng | đúng1prey, cùng hành lang, không duplicate/spawn |
| V03 | 1–2s trở đi | cá tiền cảnh đã ở phía trước gỗ rất sớm; con mồi dưới gỗ trước5s | fail cause/key >5s: kết cục thoát đã xuất hiện sớm | giữ prey hoàn toàn ngoài cửa trước5.8s |
| V04 | 5.333–6.458s | Muskie tiến tới, quay hướng camera và há miệng phía trên gỗ; không thấy hàm khép sát đuôi con mồi tại cửa; cá nhỏ đã dưới gỗ | fail key kể chuyện; không gọi mouth opening là cú săn đúng vị trí | corridor mở, cùng đường tiếp cận, một burst ngắn, khép hụt ngay ngoài cửa |
| V05 | t=0 và bố cục | gỗ ngang chắn nửa dưới, prey phía xa cao hơn khe; đường từ prey đến cửa xa bị che | nguy cơ bố cục đã có từ ảnhA02; nguyên nhân nghi ngờ chứ không kết luận duy nhất | đặt gỗ ở phải, cả2cá ngoài khe cùng phía, đường vào nhìn rõ |
| V06 | toàn clip | nền/camera nhìn ổn định ở mẫu kiểm, màu nước hồ và gỗ hợp cơ sở dàn cảnh; không mây bùn vô nguồn lớn | pass có giới hạn | giữ môi trường, không tăng trong để che lỗi |
| V07 | 0–10s | integrated-20.0LUFS, LRA22.9LU, true peak-1.7dBFS. M tại1s-42.0LUFS,3s-46.5,5s-48.5,9s-47.5 | fail yêu cầu volume cảm nhận lớn/rõ xuyên suốt theo tương quan đo; nền quá thấp so với transient | thiết kế lại bed và action, cân mức toàn diễn biến; không chỉ nâng gain tổng |
| V08 | audio | chưa nghe trực tiếp | not checked tiếng nhạc/voice/nguồn âm/sync nghe | nghe kiểm bản render tiếp theo |
| V09 | nhận dạng | cá nhỏ thay số/vị trí đốm và kích thước biểu kiến; một số mẫu trông sâu thân; không xác nhận đúng white sucker khoa học | chưa đạt consistency | ảnh mới prey nhỏ/thân thon; giữ pattern gắn từng cá |

Overall: CHƯA ĐẠT để dùng như câu chuyện đã chốt. Không thể sửa lỗi cá nhân đôi/thoát quá sớm chỉ bằng chỉnh caption, gain hoặc cắt ngắn mà vẫn giữ cấu trúc10s và key>5s. Cần dựng lại chuyển động từ ảnh sửa.
Actions: A04 sửa ảnh đầu + prompt; giữ cốt lõi Muskie hụt vì khe trú thấp. Đơn giản hóa từ xuyên qua gỗ sang chui vào trú và còn thấy ở cùng cửa, tránh yêu cầu hai cửa đối diện cùng hiện. Không nâng thành policy/active lesson.
