# Năm sửa lỗi sau hai audit độc lập

Date: 2026-10-17 | chayvideo v2.4 | clonevideo v1.2 | Workspace VERSION 1.5, chưa phát hành

Thực hiện [phương án đã duyệt](independent-audits-and-repair-plan-2026-10-17.md). Báo cáo audit và kết quả cũ giữ nguyên trạng thái tại thời điểm ghi; báo cáo này mô tả trạng thái sau sửa. Không commit/push hoặc sinh media.

## Thay đổi

1. **Reference brief:** dùng cùng danh sách bảy trường khi compile và verify. Verify kiểm hash analysis, schema nguyên kiểu số nguyên 1 và payload source/coverage/roles/shots/events/audio_cues/story trong chính brief; khác/thiếu thì lỗi và complete=false. So JSON theo giá trị/kiểu, không phụ thuộc khoảng trắng/thứ tự key. Review/freshness tính lại từ analysis/media, không tin cờ dẫn xuất được lưu. Analysis schema sai kiểu bị chặn trước khi ghi brief. Không sửa/ghi đè brief gốc để tự chữa lỗi.
2. **Identity trước ghi:** save dùng production() như resolve. Identity sai Project hoặc video ID bị từ chối trước tạo stage/attempt; nguồn đúng và legacy giữ hành vi đọc/lưu. Không sửa IDENTITY, không chuyển hồ sơ tự động.
3. **Phạm vi Project:** tag count/hook/tag cấm/AI của Underwater ở nhánh profile Underwater, cùng các gate timing hiện hành. Project khác chỉ nhận kiểm cú pháp chung và phải kiểm contract thật bằng workflow; không suy helper đã máy kiểm hết policy riêng. Pending bắt chọn loài chỉ giữ cho Underwater hiện được cấu hình; profile loài tùy chọn ở Project khác không làm species thành bắt buộc. Loài được nêu vẫn được tìm profile/nghiên cứu đúng đối tượng. Không thêm schema/config máy mới, không đổi định dạng bốn mục hoặc quy định của Project.
4. **Manifest cài đặt local:** một quy tắc trong publication guard chặn manifest có thành phần tên installation tại 07-Releases/manifests, kể cả bản lồng trong snapshot. Package selector đã gọi chính guard này nên tự loại cùng tập file; không sao chép quy tắc sang packager. Ignore manifest cài đặt local ở vị trí hiện hành để giảm stage nhầm. File gốc và mọi release trên đĩa được giữ nguyên; các manifest hệ thống hợp lệ khác vẫn dùng được. Đây là lọc đường dẫn, không phải máy chứng minh mọi file khác không có dữ liệu riêng.
5. **CI và mô tả:** thêm unittest discovery vào workflow hiện có, không thêm dependency/dịch vụ. SYSTEM và publication nói đúng ZIP hệ thống là tập nguồn được phép xuất, không thay backup runtime/registry riêng. Cập nhật version tài liệu/skill và hướng dẫn liên quan, VERSION vẫn 1.5.

Không đổi story/creativity, policy Underwater, quota ảnh, allocator, resolver/binding ngoài việc thống nhất kiểm identity, cache/fingerprint hoặc quyền duyệt. Check-frame vẫn là kiểm liên kết snapshot; không thêm cổng quét mọi concept/chat. Không sửa production hoặc tự backfill legacy.

## Kiểm trước và sau

Viết test hồi quy trước sửa mã: lượt chạy 129 test khi đó có 20 failure tính cả subtest, tái hiện các lớp lỗi payload brief/identity/phạm vi Project/manifest. Các test bảo toàn hành vi hợp lệ đã đạt trước sửa vẫn được giữ. Một fixture cũ kiểm path save được bổ sung PROJECT.md hợp lệ để phù hợp đường kiểm ownership thống nhất, không nới gate trong mã.

Kết quả cuối `python -X utf8 -m unittest discover -s scripts/tests -q`: **133/133 đạt** (118 ca trước + 15 ca mới, nhiều ca có subtest):

- Từng trường capsule và schema bị đổi; trường thiếu; analysis/media đổi; brief nguyên vẫn verify được. Thay format JSON không gây lỗi; đổi bool thành số bị phát hiện. Cờ review/draft bị chỉnh không nâng nguồn partial thành complete.
- Save sai Project ở new/reference không tạo stage/attempt; identity đúng, legacy và resolver hoạt động cùng nhau.
- Caption Project khác có 0/2 hashtag hoặc disclosure kỹ thuật được cú pháp chung chấp nhận khi phù hợp nhiệm vụ fixture. Underwater vẫn chặn các caption tương ứng, giữ cấm AI/#Underwater, 3–5 tag và timing. Common checks vẫn chặn rỗng/nhiều đoạn.
- Project ngoài Underwater không bị bắt chọn loài trong new/revision/reference dù có profile loài tùy chọn. Underwater vẫn có pending khi thiếu loài/quyền chọn; loài được cung cấp vẫn cần nghiên cứu đúng đối tượng.
- CLI check chọn đúng phạm vi; không ghi runtime. Public guard chặn manifest installation local và bản snapshot; packager dùng cùng lọc, giữ bytes file gốc; manifest hệ thống hợp lệ không bị loại.

Fixture chạy ở thư mục tạm ngoài repo, không gọi model/API, không xem/nghe media. Các bytes media fixture chỉ phục vụ hash/schema; complete của validator không chứng minh có quan sát thật.

## Kiểm tích hợp và bảo toàn

- Bốn skill chayvideo/clonevideo/taoanh/dongvideo qua quick_validate (Python UTF-8, PyYAML phục vụ kiểm nằm ngoài repo).
- Memory validator đạt, 1 lesson, không đổi trạng thái. Publication validator cây index đạt, 204 file; phân biệt cây index với working tree có thay đổi chưa stage.
- Tập file working tree do package selector chọn đạt publication guard; không tạo ZIP. Hai manifest installation local thực trên máy đều còn nguyên và bị loại khỏi tập xuất. Chưa chạy workflow trên GitHub; lệnh unit suite tương ứng đã chạy local.
- Các liên kết file trong tài liệu sửa hợp lệ. Git diff whitespace đạt với core.whitespace=cr-at-eol; giữ CRLF có trước, không chuẩn hóa hàng loạt nguồn khác.
- Trước ghi có backup các nguồn sửa (kể cả untracked), status/diff và hash file bảo vệ ngoài repo. Sau sửa **480 file được bảo vệ: 0 thay đổi hoặc mất**, gồm production, registry/cache local, Memory, Project và toàn bộ 07-Releases. Không xóa/sửa manifest hoặc release lịch sử để vượt bộ lọc.

Giới hạn: kiểm này chứng minh hành vi phần mềm ở các ca đã chạy; chưa chứng minh mọi Project có policy máy đầy đủ, chất lượng quyết định agent, sáng tạo, hình/âm thật, audience hay giảm token. Vẫn cần đọc contract Project và kiểm media khi có nhiệm vụ/quyền thực tế tương ứng. Không từ test pass suy hệ thống đã tối ưu tuyệt đối.
