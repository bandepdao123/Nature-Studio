# GPT Image 2.5 Sunburst — ưu tiên qua image_gen

ID: MODEL-SUNBURST-IMAGEGEN | Version: 1.0 | Updated: 2026-10-16
Preferred model (requested_model): gpt-image-2.5-sunburst
Requested route: built-in image_gen
Fallback: model mặc định của image_gen, đã được người dùng cho phép; không hỏi lại

Tài liệu OpenAI đã mở 2026-10-16: [Sunburst](https://developers.openai.com/api/docs/models/gpt-image-2.5-sunburst) mô tả model tạo/sửa ảnh ưu tiên chất lượng và độ chính xác sửa; [image prompting](https://developers.openai.com/api/docs/guides/image-prompting#choose-a-model) khuyến nghị thử Sunburst khi yêu cầu chất lượng cao. Đây là thông tin tài liệu, chưa có so sánh Sunburst/Flare trên Underwater.

Schema image_gen hiện có prompt, cơ chế tham chiếu ảnh và transparent_background; không có model/quality/seed selector hoặc bảo đảm công bố backend. Tên model trong prompt không điều khiển routing. Chọn Sunburst qua API là khả năng tuyến khác, không chứng minh tool tích hợp đã chọn model đó.

Tra schema thực mỗi môi trường: nếu chọn được Sunburst thì chọn, selection_mode=sunburst; nếu không tìm được hoặc không có selector thì dùng mặc định, selection_mode=tool_default, tiếp tục không hỏi lại. Ghi requested_model và actual_model/model_verified riêng. Không có nguồn công bố model thì actual_model=unknown, model_verified=false. Không tự dùng API key, CLI hoặc chỉ định Flare để thay thế.

Built-in image_gen là tuyến thực thi. Danh tính model chỉ là metadata, không phải tiêu chí QA hoặc cổng chặn sinh ảnh. Không hứa đã dùng Sunburst khi công cụ không công bố. Tối đa 5 lượt và gate ảnh theo first-frame.md; không dùng chất lượng model làm lý do bỏ QA.
