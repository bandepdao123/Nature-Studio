# Cập nhật Nature Studio từ GitHub

Version của quy trình: 1.0 | Updated: 2026-10-16

Repository nguồn hiện hành: [bandepdao123/Nature-Studio-v1.0](https://github.com/bandepdao123/Nature-Studio-v1.0). Phiên bản workspace: [VERSION](VERSION); lịch sử: [CHANGELOG.md](CHANGELOG.md). Không giả định nguồn luôn mới hơn local hoặc mọi bản cùng VERSION có nội dung giống nhau.

## Điểm vào cho AI nhận link repository

Đọc theo thứ tự: README.md → VERSION → REPOSITORY.json → CHANGELOG.md → START-HERE.md → SYSTEM.md → AGENTS.md → UPDATE.md. Sau đó tra 03-Projects/INDEX.md và PROJECT.md liên quan; chỉ đọc thêm nội dung cần cho nhiệm vụ. AGENTS.md là điểm vào cho host có hỗ trợ, còn README/START-HERE là đường đọc cho AI khác.

Link repository chỉ cho biết dữ liệu trên GitHub. Muốn xác định máy người dùng cần cập nhật gì, phải đọc được workspace local hoặc gói ZIP/manifest của bản họ đang dùng. Nếu thiếu, vẫn giải thích được hệ thống và bản đích, nhưng phải ghi phần chênh lệch local là chưa xác định; không nhận đã đồng bộ hoặc bảo toàn dữ liệu chưa thấy.

## 1. Xác định bản đang dùng và bản đích

- Local: đọc VERSION; nếu có Git, ghi HEAD, branch, remote, trạng thái tracked/untracked và staged/unstaged. Nếu dùng ZIP, đọc PACKAGE-MANIFEST.json và đối chiếu hash file thực; manifest cũ không chứng minh file chưa bị sửa. Thiếu VERSION không suy ra v0.0: tra manifest/lịch sử hoặc ghi unknown.
- GitHub: nếu người dùng chỉ định commit/tag/release, dùng đúng bản đó. Nếu họ muốn bản phát hành ổn định, đọc GitHub Releases, bỏ draft/prerelease trừ khi được yêu cầu. Nếu chưa có release, dùng VERSION tại main và ghi rõ đây là bản trên nhánh main, không gọi là GitHub Release.
- Nếu yêu cầu là bản mới nhất trên GitHub, đối chiếu main hiện tại cùng VERSION/CHANGELOG; chỉ ra nếu main còn thay đổi chưa nằm trong release ổn định. Không chọn file có số phiên bản lớn nhất trong 07-Releases làm bản đích.
- Tên repo thay đổi theo phiên bản. Đọc REPOSITORY.json: repository_id 1421542100 là danh tính ổn định của repo gốc, tên hiện tại theo mẫu Nature-Studio-v{version}. Khi nhận link cũ, phân giải URL qua GitHub hoặc tra repo bằng ID để tìm tên hiện hành; xác nhận đúng owner/ID trước khi cập nhật remote. Không lấy tên suffix lớn nhất từ các repo tìm được làm bằng chứng bản mới nhất; không theo repo khác chỉ vì trùng tên. Bản local cũ có thể chưa có REPOSITORY.json, khi đó xác minh danh tính qua nguồn GitHub đã biết trước khi thay remote.
- Chốt một commit SHA cụ thể của bản đích và dùng cùng SHA khi đọc mọi file. Kiểm remote đúng repository trước khi fetch; không dùng nhầm fork. Nếu không truy cập được nguồn, nói rõ và không đoán nội dung bản mới.
- Báo cả `workspace version + commit + local modifications`, không chỉ VERSION. Một bản ZIP tạo lúc working tree dirty không hoàn toàn tương ứng với source commit; dùng hash các file trong gói để biết nội dung thật.

## 2. Lập chênh lệch trước khi sửa

Với Git, fetch để đọc bản đích rồi so lịch sử và file; kiểm thay đổi local trước khi merge/pull. Với ZIP, đối chiếu manifest nguồn gốc và file thực với manifest/nội dung bản đích. Khi có baseline chung, so ba phía: baseline → local và baseline → bản đích.

| Tình huống | Xử lý |
|---|---|
| Chỉ bản đích đổi file, local còn đúng baseline | Có thể nhận thay đổi trong phạm vi cập nhật đã giao |
| Chỉ local đổi | Giữ chỉnh sửa local; không chép bản đích đè lên |
| Hai phía đổi giống nhau | Giữ một bản, kiểm nội dung/hash |
| Hai phía đổi khác nhau | Merge theo mục đích và kiểm lại; hỏi khi phải chọn chính sách/ý định không suy được |
| File mới cùng đường dẫn nhưng khác nội dung | Xung đột; không tự chọn theo ngày hay VERSION |
| Nguồn xóa/đổi tên file | Kiểm nội dung local và mapping di chuyển; không tự xóa dữ liệu riêng |
| Không biết baseline | Không ghi đè file khác nội dung; làm bản so sánh và giữ bản gốc, hỏi khi cần quyết định |

Trình bày ngắn: local, bản đích, điều thêm/sửa/di chuyển, dữ liệu giữ lại, xung đột/điểm chưa biết và kiểm sẽ chạy. Lập diff theo nội dung, không chỉ đọc CHANGELOG rồi kết luận đã biết mọi thay đổi.

## 3. Bảo toàn dữ liệu riêng

Nguồn runtime gồm `.agents/skills`, Standards, Models và các tài liệu đầu vào. Các nơi này vẫn có thể chứa chỉnh sửa riêng; không có thư mục nào mặc định được phép chép đè toàn bộ.

Đặc biệt kiểm PROJECT.md, decisions, idea-ledger, 04-Productions, 05-Memory, hồ sơ nguồn Knowledge và kết quả Evaluation. Giữ ID, attempt, media, feedback, bài học và liên kết của người dùng. Khi nhận dữ liệu mới từ upstream, kiểm va chạm ID/đường dẫn; không gộp hai production khác nhau chỉ vì cùng UF-0001. Không biến lesson candidate thành active hoặc coi mẫu là sản phẩm thật.

07-Releases chứa lịch sử: không sửa baseline/manifest/snapshot đã đóng. Trong kho hiện tại, migration từ 03-Channels/under-fishing-us sang 03-Projects/underwater đã được ghi; chỉ áp mapping nếu bản local thật sự còn ở cấu trúc cũ. Không tạo hai dự án Underwater và tên cũ từ cùng một ID. Token, credential và cấu hình cá nhân không đưa vào repo hoặc gói cập nhật.

## 4. Thực hiện trong phạm vi được giao

- Nếu chỉ được yêu cầu kiểm tra, dừng ở báo cáo chênh lệch. Nếu đã được yêu cầu cập nhật, tiếp tục phần đã rõ; chỉ hỏi khi thiếu lựa chọn thực sự hoặc có hành động ngoài phạm vi.
- Trước khi ghi, giữ bản khôi phục local gồm cả file untracked: snapshot/bản sao có manifest, hoặc commit/nhánh bảo toàn phù hợp. Không tự push bản sao lên public. Không dùng `reset --hard`, `clean`, force-push hoặc chép ZIP đè nguyên thư mục để giải quyết xung đột.
- Với Git, giữ/ghi nhận thay đổi đang làm rồi cập nhật qua nhánh và merge phù hợp; không tự stash rồi bỏ quên. Với ZIP, giải nén bản đích vào thư mục riêng, so và áp file đã phân giải thay vì giải nén thẳng lên workspace đang dùng.
- Di chuyển theo mapping có kiểm đường dẫn, sửa liên kết/chỉ mục và giữ lịch sử. Ghi thay đổi phiên bản/tài liệu đúng phạm vi; không chỉ sửa VERSION để giả cập nhật xong. Nếu cập nhật còn dở, ghi rõ phần chưa hoàn tất và không tuyên bố workspace đã đồng bộ.
- Tách cập nhật framework/skill khỏi cập nhật production thành commit riêng khi thực hiện Git; không đưa thay đổi không liên quan vào cùng commit. Publish/push chỉ khi nằm trong yêu cầu người dùng.

## 5. Kiểm tra và bàn giao

Kiểm file đầu vào và VERSION/CHANGELOG, liên kết tương đối, khả năng tìm PROJECT.md/skill, ID và số attempt/media trước–sau, trạng thái bài học, file bị xóa/đổi tên và các xung đột còn lại. Với skill sửa đổi, chạy validator sẵn có nếu môi trường hỗ trợ; kiểm hành vi/media chỉ khi được giao và có đầu vào/công cụ phù hợp.

Ghi bản trước, commit đích, file đã cập nhật, chỉnh sửa local được giữ, kiểm đã chạy và giới hạn. Khi dùng Git, kiểm diff/status cuối; khi dùng ZIP, tạo manifest sau cập nhật cho chính trạng thái mới. Chỉ gọi là khớp hoàn toàn khi đã so nội dung/hash thực. Workspace đã merge chỉnh sửa riêng có thể đúng bản nền mới nhưng không byte-identical với upstream; phải nói rõ.

Không tự render, tiêu tiền hay đăng nội dung để kiểm việc cập nhật. Chỉ tạo gói/release hoặc đẩy lên GitHub theo phạm vi được giao. VERSION v1.0 là phiên bản toàn Nature Studio; các số phiên bản skill/project/guide là độc lập.

## Mẫu yêu cầu dùng với AI bất kỳ

> Đây là Nature Studio: https://github.com/bandepdao123/Nature-Studio-v1.0. Đọc README.md và UPDATE.md ở bản nguồn, kiểm VERSION/CHANGELOG và đối chiếu với workspace tôi cung cấp. Cho biết cần cập nhật gì; khi thực hiện, giữ chỉnh sửa riêng, dữ liệu sản xuất, bài học và lịch sử. Nếu thiếu quyền đọc local hoặc không biết baseline, nêu rõ thay vì đoán.

## Quy tắc đặt tên repo theo phiên bản — 2026-10-16

Theo yêu cầu người dùng, mỗi lần chốt phát hành bản cập nhật mới phải tăng VERSION, ghi CHANGELOG và đổi tên chính repository theo `Nature-Studio-v{version}`; ví dụ v1.0 → v1.1 thì repo thành Nature-Studio-v1.1. Các chỉnh sửa đang làm có thể chưa phát hành; trước khi công bố phải đồng bộ phiên bản và tên repo, không tự tiếp tục công bố bản mới dưới cùng tên/số cũ.

Đổi tên trên cùng repository, giữ repository_id và lịch sử; không tự tạo một repo rời cho mỗi phiên bản. Xác minh tên mới và ID, cập nhật REPOSITORY.json, URL trong tài liệu đầu vào và remote Git, rồi kiểm link, commit và gói ZIP. Chỉ thay remote khi danh tính đã được xác minh. Giữ manifest/gói/snapshot cũ và các URL provenance trong đó; mỗi bản được nhận diện thêm bằng commit/tag để phân biệt lịch sử. Nếu không có quyền đổi tên hoặc tên đích đã thuộc repo khác, dừng bước phát hành và báo tình trạng; không giả đã đổi tên.
