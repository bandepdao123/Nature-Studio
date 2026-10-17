# Kiểm triển khai truy xuất bộ nhớ v1.8

Ngày2026-10-17. Expected xác định trước trong scripts/tests/benchmark_memory_retrieval.py; actual đo bằng engine thật, fixture riêng không sửa production.

- Unit suite152 ca:150pass,2skip do FFmpeg/FFprobe không có trong PATH. Ca retrieval bổ sung10/10pass sau sửa fingerprint source engine.
- Fixture1000lesson active có metadata hợp lệ qua validate_memory. Ca video-review cần line/motion/shared: expected3, actual3;997bài caption loại bởi task rõ. Query rộng phân trang đi đủ1000bài, không cắt top-k.
- Baseline toàn body: 6,108,991 byte. Descriptor +3body được chọn: 20,686 byte, giảm 99.66% trong fixture. Không đo token thực; không bảo đảm mức giảm này cho workload rộng hoặc semantic recall ngoài ca kiểm. Thời gian query riêng trên máy kiểm: 1.331s, không so latency model.
- Kiểm mutation/new/delete/status/taxonomy, legacy/unknown, ID conflict, path escape, source hash và packet selection có ca riêng. Candidate/retired không thành active, Project khác không lọt vào, topic không là điều kiện loại tuyệt đối.
- Guard cây public/staging và memory validator trên tập xuất chạy đạt. Catalog JSON/query runtime bị chặn; INDEX công khai dựng từ lesson public/reviewed được xuất, không từ local INDEX. Không công khai nguồn production riêng.
- Không chạy external skill-creator quick_validate.py vì PyYAML tùy chọn chưa có; không coi đó là pass. Kiểm stdlib bốn skill có name/description và các liên kết nguồn mới riêng. Runtime lõi vẫn stdlib như v1.7.1.

Kết quả máy đọc: [record](memory-retrieval-v1.8.json). Đây là bằng chứng kiểm công cụ truy xuất, không kích hoạt bất kỳ lesson sáng tạo/empirical nào và không chứng minh video/prompt render tốt hơn. Không có bài học thực mới được tự nâng active trong đợt cập nhật.
