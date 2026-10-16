# Mã Project và video

Version: 1.0 | Updated: 2026-10-16 | Nature Studio v1.2

Video mới có mã `XXX-yyyyy`: ba chữ A–Z viết hoa riêng từng Project local, năm chữ số từ 00001 đến 99999. Ví dụ QMT-00001 chỉ minh họa, không phải prefix mặc định. Repo không gán sẵn prefix cho người clone. Mỗi video giữ mã qua revision; các attempt A01, A02… là lần thử bên trong, không tăng số video. Hủy/xóa video không giải phóng mã. Hết 99999 thì dừng và quyết định mở rộng chuẩn, không quay về 00001 hoặc tự đổi prefix.

## Công cụ cấp mã

Đọc PROJECT.md để chọn slug/ID ổn định; không suy slug từ tên hiển thị. Khi thiết lập Project lần đầu ở local hoặc trước video mới đầu tiên, chạy:

```text
python scripts/video_ids.py init underwater
```

Có thể dùng `--prefix ABC` nếu người dùng chỉ định ba chữ chưa dùng. Lệnh init trả lại cấu hình cũ nếu đã có; không cấp prefix mới khi cập nhật repo/đổi tên Project. Khi đủ brief và thực sự tạo video mới:

```text
python scripts/video_ids.py reserve underwater
```

reserve tự init nếu cần, giữ số bằng transaction SQLite và tạo `04-Productions/<slug>/<video-id>/IDENTITY.json`. Identity có UUID Project/video để phân biệt khi nhập dữ liệu từ máy khác. Registry `.nature-studio/video-ids.sqlite3` là dữ liệu local không có trong Git; không xóa/reset khi nâng phiên bản. Số đã commit vẫn bị giữ nếu bước tạo thư mục lỗi; khoảng trống là hợp lệ. Không gọi reserve khi chỉ hỏi kiến thức, sửa skill hoặc sửa video cũ. Không tự đặt mã bằng đoán số trong chat. Python/registry không hoạt động thì báo giới hạn và xử lý trước khi cấp mã.

Script kiểm prefix đã cấp trong registry và mã mới có trên thư mục production/ledger toàn workspace; số mới lớn hơn số registry và các mã cùng prefix tìm thấy. Các phiên trên cùng workspace sử dụng cùng registry. Không đảm bảo duy nhất toàn cầu bằng ba chữ; UUID là căn cứ phân biệt khi gộp dữ liệu. Hai bản clone được sản xuất độc lập không chia sẻ transaction; trước khi gộp phải so cả mã và UUID, không ghi đè vì mã giống nhau.

## Di chuyển, mẫu và lịch sử

- Tiếp tục cùng một Project trên máy khác: sao lưu cả `.nature-studio/` khi không có phiên đang ghi, cùng production/ledger. Đừng clone rồi khởi tạo mới nếu muốn giữ danh tính local cũ.
- Tạo Project độc lập từ mẫu: cấp ID Project mới và chạy init, không chép registry/IDENTITY từ mẫu. Chỉ clone repo sạch thì chưa có registry, prefix được thiết lập khi init lần đầu; không cần tạo toàn bộ Project ngay khi tải repo.
- Mất registry nhưng còn production: dừng khôi phục từ backup nếu cần tiếp tục danh tính cũ. init không tái nhận prefix có trên các mã đã có; nó cấp danh tính mới để tránh chiếm nhầm. Không nhận đã khôi phục UUID/bộ đếm chỉ từ tên thư mục.
- Repo/gói phân phối mẫu không chứa registry local; backup/di chuyển workspace cá nhân phải kèm registry riêng. UPDATE.md hướng dẫn bảo toàn nó. Khi nhập/gộp Project từ nguồn khác, so ID/UUID/prefix và giải quyết xung đột trước, không tự đổi mã lịch sử.
- UF-0001 và prefix UF là legacy: giữ nguyên đường dẫn, ID, attempt và tham chiếu. Chỉ video mới dùng prefix local ba chữ và bắt đầu 00001; không đổi UF-0001 thành mã mới, không tự gán UUID giả cho lịch sử. /dongvideo vẫn tra được mã cũ.
