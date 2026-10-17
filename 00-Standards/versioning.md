# Phiên bản hệ thống

Version: 1.0 | Updated: 2026-10-17

Từ v2.0.0, VERSION dùng `MAJOR.MINOR.PATCH`. Thay đổi nhỏ tương thích, sửa lỗi hoặc tinh chỉnh routing/skill đã chốt phát hành: tăng PATCH, ví dụ 2.0.0 → 2.0.1 → 2.0.2. Tính năng tương thích có phạm vi lớn: cân nhắc MINOR (2.1.0); thay đổi phá tương thích: MAJOR (3.0.0). Không tăng bản hệ thống cho mỗi video, attempt hoặc file sửa nháp. Version của tài liệu/skill/Project độc lập.

```text
python scripts/versioning.py next
python scripts/versioning.py check
```

`next` mặc định chỉ in bản PATCH kế tiếp; không ghi VERSION. Khi chốt phát hành, cập nhật VERSION, CHANGELOG, phiên bản hiện hành trong README/START-HERE/SYSTEM và tạo ghi chú mới ở 07-Releases. `check` kiểm định dạng, sự hiện diện của marker hiện hành và file ghi chú; không xác minh nội dung release hoặc Git tag. CI chạy check cùng các kiểm tra hiện hành. Không sửa bản phát hành cũ; commit/tag/GitHub Release là thao tác riêng chỉ làm khi được giao.
