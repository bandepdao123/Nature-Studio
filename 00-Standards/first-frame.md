# Tạo ảnh first frame và QA

Version: 1.0 | Updated: 2026-10-16

Thực thi theo [.agents/skills/taoanh/SKILL.md](../.agents/skills/taoanh/SKILL.md). Đây là phương pháp chung; tiêu chí hình ảnh lấy từ Project, không mặc định cá/nước/9:16 cho mọi dự án.

## Các tiêu chí bắt buộc

| Tiêu chí | Kiểm trên ảnh/file thực |
|---|---|
| Khớp brief | Chủ thể, số lượng, nhận dạng, tỷ lệ và lựa chọn đã khóa; không thêm/bớt vật để làm dễ |
| Đúng t=0 | Trạng thái trước biến cố theo concept; không vẽ sẵn kết quả dành cho phần sau |
| Cấu tạo/kết nối | Hình thể/giải phẫu hoặc cấu trúc vật, tiếp xúc/đường nối phù hợp; không nhân đôi/dính/biến dạng |
| Không gian | Vị trí tương đối, tỷ lệ, che khuất, phối cảnh hợp lý; đủ không gian cho diễn biến đã chọn |
| Môi trường/phong cách | Chất liệu, ánh sáng, màu, quang học và camera đúng Project, không chỉ ảnh đẹp |
| Khả năng làm đầu vào video | Bố cục hỗ trợ câu chuyện; không khóa chủ thể vào trạng thái không thể tiếp nối. Đây là đánh giá bố cục, không là test chuyển động |
| File đầu ra | Mở được và đã xem ảnh; đo pixel/tỷ lệ/thông tin alpha khi liên quan; không suy từ prompt |
| Ràng buộc Project | Mọi tiêu chí bổ sung Project xác định là bắt buộc đã được kiểm |

Trước sinh ghi danh sách áp dụng, điều kiện/ngoại lệ. Không đặt toàn bộ tiêu chí khó thành not_applicable sau khi thấy ảnh lỗi. Nếu chi tiết nhận dạng bắt buộc bị che/mờ không kiểm được, ghi not_checked và sửa bố cục hoặc báo giới hạn.

Mỗi mục pass/fail/not_checked/not_applicable kèm bằng chứng. `qa_pass` chỉ khi mọi mục bắt buộc pass, không lỗi chặn và không mục bắt buộc chưa kiểm. Lỗi nhỏ chỉ không chặn nếu không ảnh hưởng brief/khả năng dùng và được nêu rõ. Không dùng tổng điểm/giới hạn 5 lượt để hạ chuẩn. Yêu cầu không kiểm được do tool/model phải ghi riêng.

## Hạn mức và danh tính

Tối đa 5 yêu cầu sinh/edit/regenerate mỗi cycle; lỗi tool cũng tính nếu đã gửi. Script `scripts/image_budget.py` lưu quota atomically trong production, không gọi API. Bắt buộc reserve trước call, ghi call_id vào attempt, không reset qua phiên chat. Xin thêm số lượt cụ thể sau khi hết; nguồn chấp thuận được lưu local trước grant. Script ghi nhận nguồn nhưng không tự chứng minh đó là lời đồng ý: agent phải kiểm quyền thật.

Mỗi lượt là một attempt Axx riêng, dùng đúng mã video hiện có. Chốt FIRST-FRAME.json trỏ chính xác file/hash/review đạt; user approval độc lập. Không ghi đè output/review/ảnh nguồn. Không viết lại lịch sử input video đã render khi thay ảnh mở đầu; attempt video sau phải dùng đúng ảnh mới đã chọn và ghi provenance.

## Lựa chọn model

Sunburst là ưu tiên, image_gen là tuyến thực thi. Chọn Sunburst nếu công cụ hỗ trợ; nếu không tìm được hoặc không có selector thì dùng model mặc định và tiếp tục không hỏi lại. Danh tính model không thuộc tiêu chí QA và không chặn sinh/duyệt chất lượng ảnh. Ghi actual_model=unknown nếu tool không công bố, không nhận đã dùng Sunburst. Không tự chuyển API/CLI. Xem [model profile](../02-Models/model-profiles/sunburst-imagegen.md).
