# Knowledge chung, phạm vi riêng

Version: 1.0 | Updated: 2026-10-17

`01-Knowledge/` là thư viện toàn workspace, không thuộc riêng Underwater. Mỗi hồ sơ vẫn có phạm vi: loài, habitat, tương tác, dụng cụ, nguồn và trạng thái. Nội dung hiện tại tập trung Underwater; hồ sơ cá không tự áp cho deer. Quyết định format, khán giả và cách kể nằm trong Project, không chép vào Knowledge chung.

## Thêm loài hoặc Project

1. Thêm hồ sơ có ID, tên khoa học, nguồn/ngày, phạm vi và điểm chưa chắc theo chuẩn nghiên cứu; cập nhật chỉ mục Knowledge. Một loài một nguồn chính; không thay tên loài trong hồ sơ cũ.
2. Thêm key/đường dẫn trong `03-Projects/<slug>/context-map.json` đúng Project. Thêm mười hồ sơ cá không làm AI đọc cả mười: species map chọn hồ sơ đúng loài; các ràng buộc liên quan vẫn phải đọc.
3. Với Project deer mới: dùng mẫu Project, ID/slug riêng; map chỉ trỏ nguồn deer/habitat/tương tác và chuẩn liên quan, không kế thừa map Underwater. Chưa có dự án rõ thì hỏi/chốt trước khi sản xuất.
4. Xếp nguồn vào stage/effect trong `context-routing.json` nếu cần. Mode source list là mức bao phủ tối thiểu; nguồn chưa xếp stage được đọc rộng để tránh mất gate. Không đưa mọi loài vào danh sách nguồn nền của mọi mode.
5. Kiểm packet/verify/coverage, fallback thiếu loài và tác vụ revision/caption. Nguồn hash đổi thì dựng lại packet/đọc lại phần liên quan. Không sửa skill chỉ để thêm dữ liệu.

Xem [cấu hình và cơ chế đọc](context-routing.md). Giữ nguyên văn nguồn cần thiết, chỉ giảm đọc thừa/đọc lặp; không dùng quota token để bỏ dữ kiện hoặc ràng buộc. Thư viện lớn lên giúp chọn nguồn có lợi hơn so với đọc toàn kho, nhưng không có tỷ lệ tiết kiệm cố định hoặc bằng chứng tự động về chất lượng sáng tạo.
