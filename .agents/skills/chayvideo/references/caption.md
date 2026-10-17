# Chỉ sửa caption

Đọc packet caption/stage write qua view (Project, giọng viết, memory policy và descriptor bài học rồi mở gốc phù hợp) cùng nội dung clip đã chốt: concept/attempt/video được cung cấp. Theo [lõi chung](../../../../00-Standards/video-prompt-workflow.md), không nạp JSON/hash inventory hoặc toàn bộ Memory INDEX. Chỉ mở phần nguồn đủ xác định hành động/kết cục/dụng cụ và caption trước. Không đọc toàn bộ lịch sử concept, habitat, model, Story Development hoặc tái phát triển chuyện chỉ để sửa một câu. Có nghi vấn thuật ngữ/cơ chế thì mở đúng nguồn bổ sung. So caption gần đây để tránh lặp cách mở khi cần. Coverage không thay tự kiểm giọng/đúng cảnh.

Underwater: nguyên bản, ngắn/trực tiếp, chọn một chi tiết đáng xem, giọng người câu cá Mỹ. Linh hoạt hỏi/nhận xét/phản ứng/chỉ dẫn, thường 1–8 từ nhưng không quota. Không nhồi slang/jargon hoặc khẳng định mắc/bắt/nuốt khi hình chưa chứng minh. Hook và 3–5 hashtag khác nhau liên quan viết **cùng một đoạn**; không AI/công nghệ tạo nội dung, không #Underwater bất kể hoa/thường. Prompt/concept chỉ là dự kiến; render được cung cấp thì bám điều đã quan sát thật. Giữ mức không chắc chắn khi bị che.

Trả CAPTION (hoặc JSON một trường caption nếu được yêu cầu). Kiểm cú pháp bằng output helper và tự kiểm giọng/đúng cảnh; lưu revision tham chiếu production/attempt gốc, không cấp ID hoặc viết lại hai prompt. Không sửa caption/attempt lịch sử tự động.

Khi lưu bằng helper, resolve đúng bản gốc rồi truyền base_attempt/base_sha256 theo lõi chung. Caption-only không được kèm thay đổi idea/prompt/frame_state; tự kế thừa phần giữ nguyên, không mở lại QA ảnh nếu không có nhiệm vụ dùng ảnh.
