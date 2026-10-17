# Nature Studio — rà soát tổng thể

Date: 2026-10-17 | Workspace VERSION: 1.5 | Git HEAD: 87f2750a6a1ce7681e2a24d0932a2ab2693c53ae

Đối tượng là working tree local có thay đổi tracked/untracked chưa phát hành, gồm chayvideo v2.3, clonevideo v1.1 và các helper mới; không đồng nhất với HEAD/index hoặc khẳng định GitHub đã có các thay đổi này. Lượt kiểm chỉ thêm báo cáo này, không sửa quy tắc/mã/Project/runtime hoặc phát hành.

## Kết luận

Nền tảng tổ chức, quyền và bảo toàn dữ liệu khá rõ. Chưa đủ căn cứ gọi hệ thống tối ưu hoặc đã chứng minh hoạt động tốt cho mọi Project. Vấn đề chính là chính sách Project chưa được chuyển đầy đủ thành hành vi của helper, đường đọc lịch sử còn tốn khi tăng quy mô, và kiểm chứng chủ yếu ở tầng cấu trúc. Không cần thêm một tầng quy định sáng tạo; ưu tiên sửa chỗ áp dụng sai phạm vi, đồng bộ nguồn và thực nghiệm có giới hạn.

## Phát hiện có bằng chứng

### F1 — Helper dùng chung còn áp luật nội dung cố định

Ưu tiên: cao trước khi mở rộng nhiều Project.

- scripts/chayvideo_output.py:236–245 bắt mọi caption có 3–5 hashtag và cấm nhắc AI, kể cả underwater=False. Quy chuẩn số tag hoặc disclosure của Project khác chưa được đọc để quyết định các kiểm này. Việc cấm riêng #Underwater và nhịp 10s đã được đặt dưới nhánh underwater, nên khả năng tách phạm vi hiện mới được làm một phần.
- scripts/chayvideo_context.py:84–94 luôn thêm pending chọn loài khi mode khác caption và species trống; loài lạ được báo nghiên cứu species/habitat/tackle dù Project có thể là cảnh quan, không câu cá.
- Tái hiện ngoài repo: caption `Clouds cross the ridge.` ở Project giả lập cho phép không hashtag bị báo `caption: require 3–5 distinct hashtags`; caption `AI-assisted visualization. #Clouds #Weather #Climate` bị báo `caption: AI mention/tag`; packet Project giả lập với species rỗng nhận `Resolve species or granted choice before producing content`.

Đây là lệch giữa mục tiêu quy chuẩn riêng Project và hành vi helper; không đồng nghĩa phải bỏ các luật này của Underwater. Hướng xử lý: helper lấy yêu cầu nội dung/đầu vào từ Project và chỉ kiểm phần có cấu hình/nguồn rõ. Bổ sung ca âm tính chứng minh Project không có cá/không dùng hashtag không bị ép luật câu cá/caption của nơi khác. Không chỉ dùng fixture khác tên nhưng cùng caption 3 hashtag rồi kết luận đã hỗ trợ mọi Project.

### F2 — Check-frame đối chiếu snapshot được resolve, không tự phát hiện concept ngoài attempt đã đổi

Ưu tiên: vừa; giới hạn cần xử lý trong luồng đồng bộ, không là lỗi tính hash.

scripts/chayvideo_output.py:127–193 kiểm frame_state/first-frame prompt trong OUTPUT và nguồn QA. brief_version/concept_version trong template không được dùng để đối chiếu file brief/concept hiện hành.

Tái hiện trong RevisionFrameTests fixture: handoff và A01 khớp → matched; ghi concept.md ở production thành yêu cầu mở đầu khác nhưng không tạo revision OUTPUT → vẫn matched. Kết quả matched đúng với A01 được chỉ định; nó không chứng minh concept/chat mới đã được nhập vào A01. Workflow có yêu cầu AI đọc brief và đối chiếu, nên đây là điểm mù khi dữ liệu không được đồng bộ, không phải mọi lần matched đều sai.

Hướng xử lý: xác định rõ nguồn thực thi đã resolve; brief/concept thay đổi liên quan phải được đối chiếu và ghi revision trước tái dùng binding. Thay đổi chưa đồng bộ cần thể hiện unverified/cần đối chiếu. Không tự sinh lại ảnh, không dùng mọi thay đổi chữ để hạ QA cũ, không nhận máy đã hiểu khác biệt ngữ nghĩa.

### F3 — Fingerprint câu chuyện hết hạn vì thay đổi văn bản không đổi chuyện

Ưu tiên: vừa, tăng theo số production/attempt.

scripts/chayvideo_context.py:143–166 đưa mọi Markdown/JSON/TXT của production vào freshness. Thêm caption/review/settings cũng làm capsule hết hạn; nhánh new yêu cầu đọc tất cả needs_read. Tái hiện: fingerprint hợp lệ trước khi thêm A02/caption.md; sau thêm caption-only, fingerprint=None và needs_read có cả concept lẫn caption mới.

Cách này bảo thủ về coverage nhưng chưa tối ưu theo tác động nội dung. Hướng xử lý: tách thay đổi cốt truyện và delta vận hành/diễn đạt đã được đánh giá; giữ capsule còn đúng và đọc phần phát sinh liên quan. Feedback/review có thể làm thay đổi hiểu biết về chuyện nên không được bỏ qua theo phần mở rộng file hoặc chỉ vì tên caption. Không cắt lịch sử top-k rồi chứng nhận độc nhất.

### F4 — Hai mô tả trái nhau về gói ZIP

Ưu tiên: vừa; dễ sửa và liên quan lựa chọn backup đúng.

SYSTEM.md:45 còn nói package_workspace.py giữ media/lịch sử. publication.md:30 và packager hiện hành xác định đây là gói hệ thống công khai, loại production/ledger/registry/private lesson; không thay backup cá nhân. README hiện hành đã theo policy mới.

Đây là câu cũ còn nằm trong điểm vào runtime, không chỉ nằm ở snapshot lịch sử. Packager đang thực thi policy mới; rủi ro là người dùng/AI hiểu nhầm ZIP đã bảo toàn dữ liệu riêng. Cần sửa mô tả trỏ về một nguồn hiện hành, giữ thông tin lịch sử ở changelog/snapshot.

### F5 — CI hiện chưa chạy bộ unit test

Ưu tiên: vừa.

.github/workflows/public-tree.yml:13–14 chỉ chạy publication validator và memory validator. Unit suite 118 ca hiện được chạy local; lỗi trong allocator/quota/resolve/reference/context có thể không bị hai validator này phát hiện. Hướng xử lý: thêm unittest discovery vào CI trước phát hành; đây là kiểm phần mềm, không thay kiểm hành vi/media.

## Mức tối ưu và chất lượng quy định

- START-HERE/SYSTEM/AGENTS vừa là entry vừa chứa nhiều đoạn lịch sử và quy định đã có ở nguồn chuyên biệt. Chỉ ba file này khoảng 19.815 ký tự Unicode trước khi đọc nhánh/Project. Không quy đổi số này thành token thật hoặc cho rằng toàn bộ đều thừa; có cơ hội rút phần lịch sử lặp và dẫn nguồn theo nhiệm vụ mà giữ thứ tự thẩm quyền/quyền/bảo toàn dữ liệu.
- Context-map có nhánh caption riêng là tiến bộ. Revision vẫn lấy cả format/output-contract, model, habitat và interaction; hợp lý cho sửa sâu nhưng có thể quá rộng cho sửa nhỏ. Chỉ tách sâu hơn khi đo được đường đọc/nhiệm vụ thật, không tăng thêm router ngay theo phỏng đoán.
- Hệ thống có đủ quy tắc cho các luồng hiện hành: quyền, ID, attempt, research, memory, QA, publication. Thiếu chủ yếu ở cấu hình Project thực sự điều khiển helper, đồng bộ dữ liệu và kiểm chứng có bằng chứng; thêm nhiều checklist khó giải quyết các thiếu sót này.
- Có cơ chế bảo toàn và xuất hệ thống nhưng chưa có backup runtime tự động được cấu hình theo repo. Đây là lựa chọn vận hành cần lịch/đích do người dùng quyết định, không phải lý do tự tạo automation trong lượt audit.

## Sáng tạo

Các nguyên tắc đang hỗ trợ sáng tạo: ví dụ mở; novelty theo cơ chế thay vì tên/màu; không mặc định twist/cứu hộ/săn–thoát; giảm nhiễu trước khi bỏ ý tưởng khó; reference được tái dùng có chủ đích; revision giữ ý định; quan sát và giả thuyết khán giả được phân biệt. Gói A–B–C bổ sung hình/âm/lời/nhịp và cho phép chuyển chức năng theo đích.

Giới hạn còn lại là tradeoff đã được Project chọn: Underwater 10s, một shot cố định, 5–8 beat, key onset >5s và ngưỡng hai khác biệt. Chúng thu hẹp dạng chuyện/nhịp có thể kể; không phải phát hiện sai hệ thống hoặc có quyền tự bỏ. Không có chứng cứ hiện tại rằng các con số đó là tối ưu audience/model. Nếu cần mở rộng sáng tạo, thử ngoại lệ có chủ đích dưới quyền người dùng, so đầu ra và giữ dữ kiện; không tự đưa giới hạn riêng này lên Standards chung.

Nguy cơ vận hành là AI cố điền đủ checklist/độ mới, kéo dài chuẩn bị hoặc thêm hành vi chỉ để đủ beat. Cần kiểm bằng đầu ra thật, không bổ sung thêm số mục/số khác biệt. Hệ thống đã cấm các cách lách này; chưa có kiểm hành vi độc lập chứng minh luôn tránh được.

## Bằng chứng kiểm và phạm vi chưa biết

- Unit suite: 118/118 đạt. Bốn skill chayvideo/clonevideo/taoanh/dongvideo qua quick_validate.
- Memory validator đạt, 1 lesson. Link file local trong 118 Markdown nguồn được quét không hỏng (loại runtime/snapshot/evidence; không xác minh mọi anchor hoặc mọi URL web).
- Publication validator trên HEAD và index đạt, mỗi cây 204 file. Chọn tập file theo packager trên working tree hiện hành rồi kiểm publication: 229 file đạt trước khi thêm báo cáo audit; không tạo ZIP hoặc stage/push. Kiểm này là cấu trúc/metadata, không chứng minh mọi nội dung riêng tư đã được rà bằng người.
- Các tái hiện F1–F3 dùng fixture tạm ngoài repo, không ghi production/registry/cache thật. Không sửa quy tắc/helper để tạo kết quả kiểm.
- Case hành vi/story/media trong 06-Evaluation/cases chủ yếu còn not run; các báo cáo triển khai phân biệt fixture/self-review với chạy AI/media thật. Chưa có bằng chứng đủ để kết luận chất lượng, retention hoặc tổng token/chi phí được tối ưu.
- Model profile Omni ghi unverified-interface phù hợp giới hạn. Đối chiếu [trang model chính thức](https://ai.google.dev/gemini-api/docs/models/gemini-omni-flash) hỗ trợ ID gemini-omni-1.1-flash; không suy từ đó rằng wrapper của người dùng đã kiểm. Fetch trực tiếp URL .md ghi trong hồ sơ bị timeout trong lượt này, không có căn cứ từ timeout để gọi nguồn cũ sai hoặc bịa. Không kiểm lại toàn bộ tài liệu sinh học, footage, âm thanh, analytics hoặc lịch sử Git cũ.

## Thứ tự xử lý đề nghị

1. Sửa F1 và thêm ca Project thực sự khác chính sách; sửa F4 để không hiểu nhầm gói phân phối là backup.
2. Khép luồng đồng bộ nguồn ở F2 và thêm unit suite vào CI (F5).
3. Đo rồi tối ưu đọc lịch sử/context ở F3; không đánh đổi coverage hoặc tự áp giới hạn token.
4. Chạy số ít ca hành vi đầu cuối cho tạo mới/reference/revision/caption với những Project khác bản chất; kiểm media chỉ khi có công cụ và quyền tương ứng. Sau đó mới quyết định có nên đổi ràng buộc sáng tạo hoặc bổ sung quy định.

Chưa thực hiện các sửa đề nghị; chúng là kết quả audit để lựa chọn phạm vi tiếp theo.
