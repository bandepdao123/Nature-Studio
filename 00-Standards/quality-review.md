# Kiểm chất lượng — v1.1

## Phân tầng kết luận

- Prompt-only: kiểm hợp đồng, tính nhất quán, cơ sở và khả năng thực hiện; chưa xác nhận hình/âm đạt.
- Image-reviewed: kiểm ảnh thật; chưa suy ra video giữ được cấu tạo/chuyển động.
- Video-reviewed: kiểm file thật, frame quanh key, chuyển động, kết nối, thời lượng và audio nếu thực sự nghe được.
- Published-measured: chỉ ghi hiệu quả từ dữ liệu đăng thực tế, có thời điểm đo và nguồn.

## Cách ghi review

Mỗi phát hiện: ID → timecode/frame → điều quan sát được → tiêu chí bị ảnh hưởng → mức độ → nguyên nhân nghi ngờ → sửa đề xuất → kết quả kiểm lại. Dùng pass / fail / not checked / not applicable cho từng tiêu chí. Kết luận chưa được kiểm khác với không đạt.

Ưu tiên: đúng loài/môi trường → nhất quán vật thể và nhân quả → câu chuyện/nhịp → hình/âm → caption theo dự án. Tiêu chí cụ thể ở format/output-contract, không áp cứng cùng trọng số cho mọi chủ đề.

## Hai bảng đánh giá riêng

1. Sản xuất: đúng dữ kiện, giải phẫu, vật lý, bố cục, timeline, audio, hợp đồng, số lượt sửa và lỗi lặp.
2. Hiệu quả nội dung: impressions/reach/view theo định nghĩa nền tảng, thời gian xem, retention, xem lại/tương tác nếu có; lưu tuổi bài và ngày đo. Thiếu chỉ số thì để unavailable, không điền 0.

Không suy nhân quả từ một clip hoặc một biến thể nhiều thay đổi; không chấm đạt chỉ vì prompt chứa từ khóa. Review có thể bị sửa khi có bằng chứng mới.
