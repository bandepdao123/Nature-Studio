# Cập nhật Nature Studio từ GitHub

Version của quy trình: 1.2 | Updated: 2026-10-17

Repository nguồn: [bandepdao123/Nature-Studio](https://github.com/bandepdao123/Nature-Studio). Phiên bản workspace: [VERSION](VERSION); lịch sử: [CHANGELOG.md](CHANGELOG.md). Không giả định nguồn luôn mới hơn local hoặc mọi bản cùng VERSION có nội dung giống nhau.

## Điểm vào cho AI nhận link repository

Đọc theo thứ tự: README.md → VERSION → REPOSITORY.json (nếu có) → CHANGELOG.md → START-HERE.md → SYSTEM.md → AGENTS.md → UPDATE.md. Sau đó tra 03-Projects/INDEX.md và PROJECT.md liên quan; chỉ đọc thêm nội dung cần cho nhiệm vụ. AGENTS.md là điểm vào cho host có hỗ trợ, còn README/START-HERE là đường đọc cho AI khác.

Link repository chỉ cho biết dữ liệu trên GitHub. Muốn xác định máy người dùng cần cập nhật gì, phải đọc được workspace local hoặc gói ZIP/manifest của bản họ đang dùng. Nếu thiếu, vẫn giải thích được hệ thống và bản đích, nhưng phải ghi phần chênh lệch local là chưa xác định; không nhận đã đồng bộ hoặc bảo toàn dữ liệu chưa thấy.

## 1. Xác định bản đang dùng và bản đích

- Local: đọc VERSION; nếu có Git, ghi HEAD, branch, remote, trạng thái tracked/untracked và staged/unstaged. Nếu dùng ZIP, đọc PACKAGE-MANIFEST.json và đối chiếu hash file thực; manifest cũ không chứng minh file chưa bị sửa. Thiếu VERSION không suy ra v0.0: tra manifest/lịch sử hoặc ghi unknown.
- GitHub: nếu người dùng chỉ định commit/tag/release, dùng đúng bản đó. Nếu họ muốn bản phát hành ổn định, đọc GitHub Releases, bỏ draft/prerelease trừ khi được yêu cầu. Nếu chưa có release, dùng VERSION tại main và ghi rõ đây là bản trên nhánh main, không gọi là GitHub Release.
- Nếu yêu cầu là bản mới nhất trên GitHub, đối chiếu main hiện tại cùng VERSION/CHANGELOG; chỉ ra nếu main còn thay đổi chưa nằm trong release ổn định. Không chọn file có số phiên bản lớn nhất trong 07-Releases làm bản đích.
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

Không tự render, tiêu tiền hay đăng nội dung để kiểm việc cập nhật. Chỉ tạo gói/release hoặc đẩy lên GitHub theo phạm vi được giao. VERSION là phiên bản toàn Nature Studio; các số phiên bản skill/project/guide là độc lập.

## Mẫu yêu cầu dùng với AI bất kỳ

> Đây là Nature Studio: https://github.com/bandepdao123/Nature-Studio. Đọc README.md và UPDATE.md ở bản nguồn, kiểm VERSION/CHANGELOG và đối chiếu với workspace tôi cung cấp. Cho biết cần cập nhật gì; khi thực hiện, giữ chỉnh sửa riêng, dữ liệu sản xuất, bài học và lịch sử. Nếu thiếu quyền đọc local hoặc không biết baseline, nêu rõ thay vì đoán.

## Tên repository ổn định — quyết định hiện hành 2026-10-16

Giữ nguyên repository `bandepdao123/Nature-Studio`, ID GitHub 1421542100; không đổi tên repo hoặc remote vì nâng VERSION. Phiên bản thể hiện trong README, VERSION, CHANGELOG, manifest, tên gói ZIP và tag/release nếu được tạo. Số phiên bản không phải một phần URL repo.

REPOSITORY.json ghi danh tính nguồn, không nhân bản VERSION. Với bản cũ mang tên thử Nature-Studio-v1.0, phân giải URL hoặc tra repository_id trên GitHub để xác minh đúng nguồn trước khi cập nhật remote về URL ổn định; không chọn repo khác chỉ vì trùng tên. Quy tắc này thay đề xuất đổi tên repo theo phiên bản trước đó. Giữ các manifest/gói đã đóng để truy vết, không sửa URL provenance trong chúng.

## Nâng từ v1.0 lên v1.1

v1.1 thêm /dongvideo, bộ nhớ Project/shared, metadata lesson có thể kiểm và quyền kích hoạt có gate. Không đổi tên repo, ID dự án, format, production hoặc trạng thái duyệt video.

### Đường đi cho người dùng

1. Giao AI link repo và workspace đang dùng; yêu cầu: “Nâng Nature Studio lên v1.1 theo UPDATE.md, giữ production và bài học riêng; kiểm chênh lệch trước khi ghi.” Với ZIP, giải nén bản mới sang thư mục riêng, không chép đè workspace.
2. AI đọc VERSION/commit/hash thực và chốt commit đích. Kiểm Git status gồm cả untracked/attempt/media. Tạo bản khôi phục gồm thay đổi local và manifest hash; không tự đưa bản sao lên public. Repo mẫu có 0 lesson không chứng minh máy người dùng cũng có 0.
3. So ba phía và cập nhật nguồn hệ thống đã phân giải: AGENTS/START-HERE/SYSTEM/README, Standards/templates, hai skill, validator/tests và hướng dẫn này. Giữ chỉnh sửa riêng; không ghi đè PROJECT.md, decisions, ledger, SUMMARY hoặc production đang làm để lấy bản mẫu.
4. Phân loại và chuyển bộ nhớ theo mapping bên dưới, sửa liên kết hiện hành và chỉ mục; giữ ID, trạng thái, lịch sử và bằng chứng. Không áp gate mới để tự nâng candidate cũ thành active.
5. Thêm đường đọc Memory của từng Project vào PROJECT.md. Tạo namespace cho mọi Project thực có trong local, không chỉ Underwater. Giữ ID ổn định, dùng slug hiện hành làm thư mục.
6. Kiểm số production/attempt/media, ID và hash dữ liệu riêng trước–sau. Chạy validator và tests; kiểm hai skill bằng validator skill-creator nếu host có. Ghi rõ các ca cần media/AI thực chưa chạy. Chỉ chốt VERSION 1.1 khi phần migration đã hoàn tất; nếu còn xung đột ghi pending, không giả đồng bộ.
7. Báo bản nền/commit đích, thay đổi giữ lại, mapping, kết quả kiểm và trạng thái local. GitHub push hoặc xuất gói theo yêu cầu riêng đã được giao; dữ liệu sản xuất local không tự thành dữ liệu public khi nâng framework.

### Mapping bộ nhớ cũ

| v1.0 | v1.1 | Điều kiện |
|---|---|---|
| 05-Memory/candidates/<lesson>.md | 05-Memory/projects/<slug>/candidates/ hoặc shared/candidates/ | Phân loại theo nội dung/phạm vi; không tự active |
| 05-Memory/active/<lesson>.md | 05-Memory/projects/<slug>/active/ hoặc shared/active/ | Chỉ giữ active khi căn cứ/phạm vi cũ còn hợp lệ; thiếu bằng chứng thì ghi rõ để xử lý, không bịa validation |
| 05-Memory/retired/<lesson>.md | 05-Memory/projects/<slug>/retired/ hoặc shared/retired/ | Giữ lý do/trạng thái/ID thay thế |
| Metadata lesson dạng văn bản | JSON frontmatter theo templates/lesson.md | Giữ phần thân và lịch sử; bổ sung unknown trong nội dung, không tự nhận đã kiểm |
| Project không có namespace | projects/<slug>/INDEX.md + ba thư mục trạng thái | Đăng ký ở INDEX gốc, thêm liên kết trong PROJECT.md |

Bài học đa Project thực sự có phương pháp dùng chung → shared với điều kiện. Nếu chưa xác định được phạm vi, giữ file cũ trong bản khôi phục và workspace, ghi danh sách pending; không tự chọn shared, không xóa. Validator sẽ báo phần chưa chuyển thay vì bỏ qua. Nếu lesson active cũ không có hồ sơ kích hoạt có thể truy nguyên, ghi đúng dữ liệu thiếu và xin quyết định cần thiết; không tạo lại một phê duyệt giả hoặc coi việc nâng cấp là duyệt lesson.

Không đổi ID đã cấp. Với ID trùng từ nhiều nguồn, giữ cả bản gốc trong backup, xác định đó là cùng bài học hay hai bài học khác trước khi gộp/cấp ID mới, ghi mapping. Không cập nhật snapshot/manifest/release cũ hoặc sửa INPUTS lịch sử để giả đã dùng phiên bản mới; liên kết lịch sử cần đổi đường dẫn thì giữ ID và ghi mapping.

Kho nguồn lần chuyển này có 0 lesson nên chỉ thay README rỗng tại ba thư mục cũ. Đây không phải lệnh xóa ba thư mục khi áp cho workspace người khác.

### Kiểm sau nâng cấp

```text
python scripts/validate_memory.py
python -m unittest discover -s scripts/tests
```

Hai lệnh dùng Python stdlib, không cần API/token/model và không render. Validator chỉ kiểm metadata/phạm vi/liên kết/gate có thể kiểm bằng cấu trúc, không chứng minh bài học đúng. Dùng /chayvideo hoặc /dongvideo khi có nhiệm vụ thực tương ứng; không tạo lesson/video giả để “test xong”. Xem 06-Evaluation/cases/EV-SYS-004.md cho các ca hành vi chưa được kiểm tự động.

### Nếu cần quay lại v1.0

Giữ bản khôi phục và diff migration. Không chép v1.0 đè lên production mới. Khôi phục nguồn hệ thống từ baseline/bản sao đã xác minh, giữ riêng lesson/sessions phát sinh sau v1.1 rồi lập mapping trước khi đưa về cấu trúc cũ. Không dùng reset --hard/clean hoặc xóa dữ liệu mới để rollback. v1.0 chưa biết namespace mới nên không nhận rollback hoàn tất chỉ bằng sửa VERSION.

## Nâng từ v1.1 lên v1.2

Tiếp tục so commit/baseline/local, tạo bản khôi phục gồm tracked/untracked trước khi ghi. Giữ nguyên production, attempts, ledger, Memory và registry `.nature-studio/` nếu đã có; không dùng registry từ repo mẫu hoặc máy khác ghi đè. Các bản v1.0 phải thực hiện migration bộ nhớ v1.1 trước rồi bước này.

1. Nhận nguồn hệ thống v1.2 đã phân giải xung đột: scripts/video_ids.py, quy tắc video-identifiers.md, templates, hai skill và packaging exclusion.
2. PROJECT.md thay prefix sản xuất cố định bằng local-generated; ghi prefix cũ ở legacy, không đổi ID Project, tên folder/production/attempt cũ hoặc lịch sử INPUTS.
3. Chạy `python scripts/video_ids.py init <slug>` cho Project muốn thiết lập trên local (hoặc để /chayvideo gọi trước video mới đầu tiên). Không chạy reserve chỉ để nâng cấp; không tạo video giả. Không copy prefix minh họa vào mọi Project.
4. Nếu đã có registry thì init trả lại cấu hình hiện hành. Khi tiếp tục cùng Project trên máy khác, chuyển nguyên registry cùng production khi không còn phiên ghi. Clone sạch không mang danh tính local; tạo độc lập được prefix mới. Mất registry thì ưu tiên khôi phục bản sao, không tự nhận UUID cũ.
5. Kiểm `python -m unittest discover -s scripts/tests`, `python scripts/validate_memory.py`, đối chiếu hash dữ liệu riêng và diff trước–sau. Chốt VERSION 1.2 sau khi hoàn tất. Test allocator dùng workspace tạm, không gọi reserve trong production thật.

Registry `.nature-studio/video-ids.sqlite3` bị Git ignore và bị loại khỏi ZIP phân phối. Backup cá nhân phải kèm registry riêng sau khi các tác vụ ghi kết thúc; không chỉ sao chép database trong lúc transaction đang chạy. Khi import nhiều nguồn, mã giống nhau nhưng UUID khác là xung đột thật: giữ cả hai, xử lý mapping trước khi gộp. Công cụ không hỗ trợ tự gộp hay bảo đảm prefix duy nhất toàn cầu.

Rollback: giữ bản sao registry và IDENTITY/production mới; không xóa để trở về v1.1. v1.1 chưa biết bộ cấp mã nên chỉ khôi phục source sau khi bảo toàn dữ liệu và lập mapping, không coi sửa VERSION là rollback hoàn tất.

## Nâng từ v1.2 lên v1.3

Theo quy trình so commit/baseline/local ở trên; giữ nguyên registry, production, attempt và caption lịch sử. Merge audience-and-caption, output-contract, PROJECT/decisions và chayvideo cùng nhau để không còn hướng dẫn trái UF-D015/016. Caption mới theo phong cách ngắn, trực tiếp, đa dạng kiểu câu; giữ 3–5 hashtag khác, loại #Underwater không phân biệt hoa/thường. Không sửa hàng loạt caption đã tạo hoặc file baseline/release cũ.

Nhận benchmark/corpus văn bản và đường đọc tương ứng. Candidate nhập từ nguồn giữ trạng thái chưa kiểm; so ID/nội dung trước khi nhận, không ghi đè bộ nhớ local hoặc tự active. INDEX có thể dựng lại theo lesson thực; không lấy số đếm từ repo đè lên workspace có nhiều lesson.

Cập nhật .gitignore và packager để ảnh giao diện/evidence nghiên cứu ở local không lên public; không xóa ảnh local. Kiểm liên kết, validator bộ nhớ và hai skill, sau đó chốt VERSION 1.3. Giữ các gói/manifest lịch sử. Không áp phong cách hoặc danh sách tag của Underwater cho Project khác.

## Nâng từ v1.3 lên v1.4 — ngừng phân phối lịch sử video

v1.4 xóa 04-Productions runtime và idea-ledger khỏi cây Git hiện hành, giữ bài học public đã rà. Nếu Git báo deletion trùng dữ liệu của máy đang dùng, **không xóa file local**: backup toàn bộ tracked/untracked/registry; ngừng tracking đúng file bằng git rm --cached hoặc dùng worktree xuất, rồi áp thay đổi hệ thống. Không dùng pull/checkout/giải nén đè để xóa production theo upstream. Giữ lesson private và bằng chứng gốc local, chỉ merge lesson public theo ID/version/scope.

Đọc 00-Standards/publication.md. Sau migration chạy memory validator trên local, publication validator trên cây index/worktree xuất. Không mặc định mọi lesson active là public; candidate có thể công khai nếu đã làm sạch và vẫn ghi chưa kiểm. Thêm publication vào metadata: private/reviewed=false mặc định; public/reviewed=true sau rà. Nếu lesson public cần evidence ở production local, giữ nguồn riêng và tạo căn cứ công khai đã làm sạch; thiếu cơ sở thì không xuất hoặc hạ mức kết luận trong bản xuất đúng sự thật, không bịa validation.

Public index dựng từ lesson thực đã xuất, không copy index có mục private. ZIP hệ thống loại runtime/private lessons và kiểm tập file xuất; backup cá nhân là việc riêng cần đủ production/ledger/registry. Rollback không được xóa dữ liệu mới hoặc tự push production trở lại. Việc xóa main không xóa dữ liệu trong commit cũ; rewrite lịch sử cần yêu cầu và quy trình riêng.

## Nâng lên v1.5 — /taoanh và Story Development

Khi nhận bản có skill taoanh, merge routing AGENTS/START-HERE, first-frame.md, model profile và QA guide của Project cùng nhau. Giữ production/attempt/ảnh/quota .image-qa.sqlite3/FIRST-FRAME.json, không reset số lượt từ template hoặc cập nhật repo. Test dùng thư mục tạm, không chạy init/reserve trên production thật để thử. Model requested Sunburst không chứng minh backend; không đổi actual unknown thành Sunburst khi nâng phiên bản. Sunburst là ưu tiên; nếu không tìm được thì dùng model mặc định image_gen, không hỏi lại hoặc thêm cổng xác minh model vào QA. Không tự đưa production/QA lên GitHub; lesson chia sẻ qua publication.md. Bản v1.5 bổ sung cả Story Development và đường đọc qua creativity; giữ dữ liệu riêng khi merge. Các manifest installation là hồ sơ local cũ, không dùng như danh mục gói public.

## Nâng từ v1.5 lên v1.6

Đối chiếu commit và thay đổi local theo quy trình trên, không dùng VERSION 1.5 đơn lẻ để kết luận hai workspace giống nhau. Phạm vi bản v1.6 ở [ghi chú phát hành](07-Releases/v1.6.md); [bản tổng hợp chuẩn bị](07-Releases/v1.6-preparation-2026-10-17.md) là mốc lịch sử trước khi chốt phiên bản.

1. Merge đồng bộ skills chayvideo/clonevideo/taoanh, các references, lõi video-prompt-workflow, chuẩn chuyển thể, templates và ba helper chayvideo_context/chayvideo_output/reference_video. Nhận routing và context-map cùng quy chuẩn Project; Project khác không sao chép mặc định gate Underwater.
2. Attempt mới ghi đúng nguồn revision và hash; save kiểm Project trước khi ghi. Giữ nguyên ID/attempt cũ, không chọn lại bản approved hoặc sửa hàng loạt hồ sơ legacy để qua validator. Thiếu nguồn legacy phải đối chiếu; unverified không đồng nghĩa nội dung sai.
3. Handoff schema 2 chỉ ghi bằng chứng thực sau QA; không điền hash/t=0/qa_sources giả cho ảnh cũ. Giữ ảnh, review, ngân sách và database quota local. Caption-only không reset quota hay tự buộc tạo lại ảnh.
4. Giữ production, ledger, registry, memory private và manifest cài đặt local. Không dùng gói phân phối thay backup; không áp deletion upstream lên dữ liệu riêng. Brief nguồn cũ/đã sửa phải được tạo lại và verify, không chỉnh cờ để bỏ qua thiếu coverage.
5. Chạy unit suite, memory validator, kiểm skill và public-tree guard trên toàn cây index dự định xuất. Chốt VERSION cùng README/START-HERE/SYSTEM khi thực sự phát hành; commit/tag/GitHub Release là các trạng thái cần xác nhận riêng.

Rollback nguồn cần giữ toàn bộ dữ liệu mới và bản khôi phục; các helper cũ có thể chưa hiểu schema mới. Không reset/xóa attempts, quota hay registry để ép tương thích.
