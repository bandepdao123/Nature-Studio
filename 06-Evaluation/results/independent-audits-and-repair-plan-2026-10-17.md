# Hai audit độc lập và phương án sửa tối thiểu

Date: 2026-10-17 | VERSION 1.5 | HEAD 87f2750a6a1ce7681e2a24d0932a2ab2693c53ae + working tree local chưa phát hành

## Cách kiểm

Hai reviewer riêng được giao repo và yêu cầu audit, không nhận findings trước, không đọc system-audit-2026-10-17.md hoặc kết quả của nhau. Cả hai đọc điểm vào/quy chuẩn rồi tự rà và dùng fixture tạm ngoài repo. Root đối chiếu lại findings với nguồn và tự tái hiện những điểm cần quyết định. Đây là audit độc lập giữa các agent, không phải kiểm của người thật hoặc hai model khác nhau, không là thử nghiệm media/audience.

Không reviewer nào sửa repo, production/registry/quota hoặc tạo media. Lượt tổng hợp chỉ thêm báo cáo/phương án này; chưa sửa các lỗi bên dưới, chưa commit/push.

## Kết quả hội tụ của hai lượt

Cả hai reviewer độc lập tìm và tái hiện ba lỗi sau, đều đánh giá P2 trong phạm vi kiểm; không có cơ sở gắn P0/P1 chỉ vì hệ thống còn chưa tối ưu.

| Finding | Bằng chứng độc lập và root kiểm lại | Sửa nhỏ nhất |
|---|---|---|
| Brief tham chiếu bị sửa vẫn verify thành công | reference_video.py:251–257 so hash analysis rồi thay data bằng analysis. Reviewer 1 sửa roles/story trong brief; reviewer 2 xóa events/đổi coverage/story; cả hai nhận exit 0/complete=true. Root sửa roles=[] và story trong brief, giữ analysis/media fixture nguyên, cũng nhận exit 0/complete=true. | So bảy trường capsule đã compile với analysis hiện hành và schema; khác thì từ chối và yêu cầu compile bản mới. Tính lại review/freshness hiện tại, không tin cờ lưu trong brief. Không yêu cầu máy chứng minh ngữ nghĩa video. |
| Save fullset nhận identity sai Project | chayvideo_output.py:278–282 chỉ kiểm video_id; production()/resolve ở 40–46 kiểm cả project_id. Cả hai reviewer và root tạo fixture identity thuộc Project khác: save tạo A01, resolve chính A01 báo Reserved Project identity mismatch. | Dùng chung production() trước mọi ghi trong save, giữ tương thích legacy. Identity sai thì báo để xác minh, không sửa IDENTITY hoặc di chuyển hồ sơ tự động. |
| Caption riêng Underwater bị áp ngoài Underwater | chayvideo_output.py:236–245 yêu cầu 3–5 hashtag/cấm AI dù underwater=False. Cả hai reviewer tái hiện caption Project khác bị chặn. UPDATE/template Project yêu cầu không mặc định kế thừa policy riêng. | Đặt gate riêng vào phạm vi rõ ràng của Project. Giữ nguyên policy Underwater; Project khác nhận kiểm cú pháp chung và tự kiểm contract hiện có, chưa xây framework cấu hình mới. |

## Findings bổ sung và phân loại lại

- Reviewer 1 phát hiện packager nhận manifest cài đặt local có trường backup_root. Root kiểm chỉ đọc: 07-Releases/manifests/story-development-installation-2026-10-16.json được included=True; public guard cũng valid=True khi file đứng riêng. Không build ZIP hay publish thật; đây là đường xuất có thể mang metadata máy, không có bằng chứng đã có rò rỉ thực tế. Sửa bằng một quy tắc dùng chung để loại/chặn manifest cài đặt local đã xác định ở package/public tree; giữ file gốc và lịch sử. Không thêm scanner đoán riêng tư cho mọi đoạn văn.
- Câu ZIP ở SYSTEM.md:45 trái mô tả packager/publication hiện hành được reviewer 1 xác nhận. Sửa mô tả gói phân phối, dẫn rõ backup runtime riêng; không sửa snapshot/release cũ.
- Root đã tái hiện pending yêu cầu loài trên packet Project giả lập không có loài. Cần sửa cùng phạm vi helper: Project không yêu cầu loài không bị ép chọn; Project cần loài giữ gate của nó. Không suy có field/map loài là mọi nhiệm vụ của mọi Project đều phải chọn loài, không bịa loài để hết pending.
- CI hiện chỉ có publication/memory validator, chưa có unit suite. Thêm unittest discovery vào workflow hiện có; không tạo pipeline hoặc dependency mới.

Điều chỉnh nhận định trước: check-frame đối chiếu source attempt rõ ràng, nên concept ngoài attempt đổi mà matched với snapshot cũ không tự là lỗi hash. Workflow vẫn phải đọc/đối chiếu brief và đồng bộ nguồn. Không mở thêm cổng quét mọi concept/chat hoặc hạ QA tự động trong gói sửa này. Có thể làm rõ ý nghĩa matched trong hướng dẫn, giữ giới hạn metadata-only.

Fingerprint hết hạn vì mọi text thay đổi là tradeoff bảo thủ đã được mô tả, chưa có bằng chứng chi phí thực tế đủ để bỏ gate freshness. Reviewer 2 không thấy căn cứ thay kiến trúc packet hoặc rút prompt theo số từ; đo tải nguồn không bằng token/latency/chi phí thực. Giữ cơ chế hiện tại trong gói sửa lỗi, đo trước khi tối ưu delta/history. Không bỏ feedback/review khỏi coverage chỉ để giữ capsule xanh.

## Gói đề nghị phê duyệt — năm hạng mục

1. **Toàn vẹn reference brief:** sửa verify, regression cho payload brief đổi trong khi analysis nguyên; payload nguyên vẫn qua và analysis/media đổi vẫn bị phát hiện.
2. **Identity trước mutation:** thống nhất save/resolve; từ chối sai Project trước khi tạo stage/attempt, không làm mất legacy và không sửa dữ liệu thật.
3. **Phạm vi Project của helper:** cô lập gate caption riêng, gỡ yêu cầu loài toàn cục không được Project quy định. Kiểm Project có hai tag/không tag/cho phép nhắc kỹ thuật và Project không có loài; Underwater giữ đầy đủ gate. Không đổi định dạng bốn mục đã chốt, không thêm file cấu hình/biểu mẫu bắt buộc. Nếu cần cấu hình máy mới vượt phạm vi tách gate tối thiểu thì nêu tradeoff trước khi mở rộng.
4. **Loại metadata cài đặt local khỏi tập xuất:** package và public-tree guard dùng cùng quy tắc; thêm fixture local manifest bị loại/chặn và manifest hệ thống hợp lệ còn dùng được. Không xóa hoặc viết lại manifest local/lịch sử.
5. **Hồi quy tự động và mô tả đúng:** chạy unit suite trong workflow hiện có; sửa câu ZIP trong SYSTEM, ghi version/changelog/báo cáo đúng phạm vi.

File dự kiến: scripts/reference_video.py, scripts/chayvideo_output.py, scripts/chayvideo_context.py, logic xuất package/publication dùng chung và test tương ứng, .github/workflows/public-tree.yml, SYSTEM.md, các hướng dẫn liên quan cần đồng bộ và CHANGELOG/Evaluation. Không tạo skill, dịch vụ hoặc hệ thống registry mới.

## Điều kiện nghiệm thu

- Các fixture lỗi mới tái hiện trước sửa và bị chặn sau sửa; test phải xác nhận hành vi, không chỉ khớp câu chữ.
- Brief chỉnh payload không thể verify đạt; brief nguyên/analysis thay đổi/media thay đổi giữ kết quả đúng.
- Save sai identity không tạo stage/attempt; nguồn đúng và legacy vẫn hoạt động.
- Project khác thực sự khác policy không bị gate Underwater; toàn bộ gate Underwater vẫn đạt/loại đúng ca.
- Manifest cài đặt local được bảo toàn trên đĩa nhưng không đi vào ZIP/public tree; không sửa release đóng.
- Unit suite, memory/publication validators và skill checks khi hướng dẫn thay đổi đều đạt; hash runtime trước/sau nguyên vẹn.
- VERSION giữ 1.5 cho tới khi được giao phát hành; chưa commit/push/media từ quyền sửa local.

## Những phần đề nghị giữ nguyên lúc này

Không đổi 10s/9:16, camera, beat, key sau 5s hoặc luật âm/caption Underwater; không thêm điểm viral, checklist sáng tạo, máy chứng thực user approval hoặc schema mapping mới. Không gọi test phần mềm là bằng chứng model/agent sáng tạo tốt. Chưa thực nghiệm concept/prompt trên nhiệm vụ sản xuất thật, reference hình/âm, render, image QA, audience hoặc chi phí token.

Hai reviewer đều chạy lại unit suite: 118/118 đạt. Reviewer 1 kiểm memory 1 lesson và publication index 204 file đạt; reviewer 2 kiểm link file nội bộ trong các miền skill/Standards/Project không thiếu. Các kết quả đó không phủ ba lỗi fixture mới, nên không dùng chúng để kết luận hệ thống không còn bug.
