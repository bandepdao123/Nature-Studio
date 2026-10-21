# Môi trường và quang học dưới nước

ID: K-HAB-UNDERWATER-001 | Status: inherited-reference | Updated: 2026-10-22

> Nhập nguyên nội dung liên quan từ hướng dẫn Under Fishing v1.9 do người dùng chốt, ngày 2026-10-15. Đây là dữ liệu kế thừa, không phải lần kiểm nguồn/đo/render mới. Các số mục và tham chiếu đánh số trong đoạn trích thuộc bản gốc; tra bản đầy đủ tại ../../07-Releases/standalone-guides/underwater-ai-realism-prompt-guide-v1.9.md. Ví dụ câu cá không tự áp dụng cho mọi kênh.

> Áp dụng hiện hành riêng Underwater — UF-D021, 2026-10-17: mô tả camera cố định của bản v1.9 là lịch sử. Ngày 2026-10-22 (UF-D024), hai đoạn camera bên dưới (Camera ngoài đời; Máy quay và khung) đã được viết lại theo UF-D021; phần còn lại giữ nguyên trích nguồn. Camera hiện hành theo [format Underwater](../../03-Projects/underwater/format.md#camera-cầm-tay-tự-nhiên--uf-d021): cầm tay chuyển động nhẹ tự nhiên như người quay điện thoại; không khóa vị trí/hướng máy. Giữ các yêu cầu quang học, vật liệu và phối cảnh; phân biệt chuyển động ảnh do máy với chuyển động thật của cá. Không suy thay đổi camera cho Project khác.

## 2. Môi trường phải khớp cả năm biến cùng lúc

Mỗi ý tưởng cần khóa một địa điểm có thật ở mức **vùng và kiểu thủy vực**, không cần bịa tên hồ/lạch cụ thể; rồi khóa năm biến: **độ sâu — nền đáy — độ trong — nguồn sáng — dòng chảy**. Nếu đổi một biến, kiểm lại bốn biến còn lại.

### Nghiên cứu và tái hiện môi trường nước chân thực

**Mục tiêu:** ảnh first frame phải giống hình ảnh một máy quay thực sự được đặt chìm tại địa điểm đã chọn có thể ghi lại. Ưu tiên tính đúng của môi trường, quang học và vật lý; không tự làm nước trong hơn, ánh sáng đẹp hơn hoặc chủ thể sắc nét hơn chỉ để tạo ảnh hấp dẫn.

#### 1. Nghiên cứu điều kiện thực tế trước khi viết prompt

AI phải xác định vùng địa lý, kiểu thủy vực, độ sâu, nền đáy, mùa, thời điểm, thời tiết và trạng thái dòng chảy hoặc thủy triều nếu có. Từ đó nghiên cứu:

- Nước thực tế thường có màu gì và vì sao: vật chất hữu cơ hòa tan, phù sa, tảo, vật liệu đáy hoặc các yếu tố khác.
- Độ trong biến thiên thế nào theo mưa, gió, dòng chảy, thủy triều và điều kiện tại thời điểm được chọn.
- Trong nước có những gì: hạt trầm tích lơ lửng, mảnh hữu cơ, tảo, vụn thực vật hoặc các thành phần phù hợp khác. Không mặc định nước tự nhiên luôn có rác, bong bóng hoặc nhiều hạt nhìn thấy.
- Nền đáy là bùn, sét, cát, sỏi, đá hay hỗn hợp; có lớp trầm tích mịn phủ trên bề mặt hay không.
- Chuyển động của con vật có thể tác động tới nền đáy, cây thủy sinh và nước xung quanh như thế nào.

Ưu tiên nguồn khoa học, cơ quan môi trường và hình ảnh/video dưới nước có thông tin địa điểm, điều kiện quay. Phân biệt hình ảnh quan sát được với diễn giải từ nguồn. Không lấy một ảnh nước trong đẹp làm đại diện cho toàn bộ thủy vực; không suy độ trong dưới nước chỉ từ màu mặt nước chụp trên bờ.

Nếu thiếu dữ liệu chính xác, chọn điều kiện có cơ sở phù hợp nhất và ghi rõ giả định trong ghi chú nghiên cứu. Không bịa số đo độ đục, tầm nhìn hoặc khẳng định đã kiểm chứng địa điểm. Các con số tự chọn để bố trí cảnh phải được xem là thông số dàn cảnh.

#### 2. Khóa màu nước và độ trong thành hai yêu cầu riêng

**Màu nước** là sắc nước trong điều kiện ánh sáng cụ thể. **Độ trong** là khả năng nhìn xuyên nước và nhận ra vật thể ở các khoảng cách khác nhau. Nước có màu không nhất thiết đục; phủ màu nâu hoặc xanh lên một cảnh rõ nét không tạo ra nước đục chân thực.

Prompt phải mô tả đồng thời:

- Sắc nước và nguyên nhân phù hợp.
- Mức độ, loại và phân bố của vật chất lơ lửng.
- Vật gần camera còn thấy những chi tiết nào.
- Vật xa mất chi tiết, tương phản và màu sắc đến mức nào.
- Hậu cảnh hòa dần vào nước như thế nào.

Sự suy giảm phải tăng theo đường truyền qua nước. Không cho chủ thể xa vẫn rõ từng chi tiết như ở sát ống kính. Không thay tán xạ trong nước bằng hiệu ứng xóa phông, làm mờ toàn ảnh hoặc một lớp sương phẳng.

Không chuyển trực tiếp số đo nhìn theo chiều sâu thành khoảng nhìn ngang của camera.

#### 3. Tạp chất và hạt lơ lửng phải có cơ sở

Chỉ thêm những thành phần hợp môi trường đã nghiên cứu. Hạt nhìn thấy cần có mật độ, kích thước, độ sáng và vị trí không đều; một số có thể nằm ngoài vùng nét hoặc quá nhỏ để phân biệt.

Không dùng lớp hạt trắng đồng đều như tuyết để biểu thị nước tự nhiên. Không tự thêm rác, bong bóng liên tục hoặc các mảnh vụn lớn để làm cảnh “thật hơn”. Nếu nước tương đối trong và ít hạt nhìn thấy, giữ đúng điều kiện đó.

#### 4. Bùn bị khuấy phải tuân theo nền đáy và nguồn lực

Không mặc định cứ con vật di chuyển mạnh là có mây bùn. AI phải xét:

- Đáy có vật liệu đủ mịn, rời và dễ tái huyền phù hay không.
- Con vật ở cách đáy bao xa.
- Vây, đuôi, thân, chân hoặc mõm có tiếp xúc nền hay tạo dòng nước đủ mạnh tới nền không.
- Hướng tác động và dòng chảy sẽ đưa vật liệu đi đâu.

Nếu điều kiện phù hợp, trầm tích phải bắt đầu nổi từ vùng thực sự bị tác động, sau tác động; sau đó lan, trôi và lắng theo vật liệu cùng dòng nước. Độ đục tăng cục bộ trước, không xuất hiện đồng loạt khắp khung. Đá và sỏi lớn không bay lơ lửng như bùn mịn.

Nếu con vật bơi cách xa đáy hoặc nền không có lớp vật liệu dễ bị khuấy, có thể không xuất hiện mây bùn. Không thêm bùn chỉ để tạo kịch tính.

**First frame chỉ thể hiện trạng thái tại t=0.** Không đặt sẵn mây bùn của một cú lao sẽ xảy ra trong video. Nếu đã có đám đục tại t=0, phải có nguyên nhân hợp lý và được xác định trong thiết kế cảnh.

#### 5. First frame phải tuân theo góc nhìn của máy quay thật

Xác định vị trí có thể đặt máy, độ cao so với đáy, hướng nhìn, góc ống kính và khoảng cách tới chủ thể. Những thông số này phải thống nhất với phối cảnh, tỷ lệ và mức nhìn thấy qua nước.

Ánh sáng phải đi qua mặt nước và môi trường đúng điều kiện đã chọn. Không tự thêm đèn rọi, vân nắng trong cảnh thiếu nắng trực tiếp hoặc ánh sáng làm mọi vật sáng rõ đồng đều.

Cho phép che khuất tự nhiên, bề mặt không đều và mất chi tiết theo khoảng cách. Không sắp chủ thể và con mồi như ảnh quảng cáo. Không dùng nhiễu, méo ống kính hoặc tối góc giả để che các sai lệch môi trường.

Nếu điều kiện nước khiến chủ thể khó nhìn, điều chỉnh khoảng cách hoặc bố cục hợp lý; không âm thầm làm nước trong hơn thực tế. Ảnh vẫn phải đọc được câu chuyện trong giới hạn mà máy quay tại vị trí đó có thể nhìn thấy.

#### 6. QA bằng ảnh thực tế, không bằng lời trong prompt

Sau khi sinh ảnh, đối chiếu lại với điều kiện đã nghiên cứu:

- Màu nước và độ trong có cùng hợp lý với địa điểm, ánh sáng và thời tiết không?
- Hạt lơ lửng, vật liệu đáy và lớp bùn có đúng loại, đúng mức không?
- Vật xa có mất chi tiết và tương phản theo khoảng cách không?
- Chủ thể có bị sắc nét, sáng hoặc bão hòa bất thường so với môi trường không?
- Có mây bùn, bong bóng hoặc tạp chất không có nguyên nhân không?
- Hình ảnh có giống góc nhìn từ một camera chìm thực sự, hay chỉ là cảnh rõ nét được phủ màu nước?

Nếu sai, sửa đúng thuộc tính gây lỗi rồi kiểm lại. **Không đánh dấu đạt chỉ vì ảnh đẹp, có màu nước phù hợp hoặc prompt đã ghi “photorealistic”.** Chỉ kết luận về những gì thực sự quan sát được; ghi rõ điểm chưa xác minh thay vì tuyên bố chính xác tuyệt đối.

**Cách ghi nhận nghiên cứu:** lưu nguồn/ngày truy cập và điều kiện nguồn nếu có; tách quan sát trực tiếp, diễn giải khoa học, giả định chọn cảnh và số dàn cảnh. Không bịa NTU, tầm nhìn hoặc việc kiểm chứng địa điểm. Ghi chú này là tóm tắt dữ kiện/giả định, không phải suy luận nội bộ phải xuất ra. Hợp đồng cuối vẫn có đúng ba sản phẩm; chỉ trình bày ghi chú nghiên cứu khi người dùng yêu cầu hoặc có giới hạn quan trọng cần thông báo ngắn. Khi không truy cập được nguồn mới, dùng cơ sở sẵn có đúng phạm vi, ghi rõ điều chưa xác minh và không tự nhận đã nghiên cứu hiện trường.

**Độ ưu tiên:** nếu một ví dụ hay mô tả thẩm mỹ khác trong file gợi ý thêm hạt, tăng độ rõ hoặc khuấy bùn nhưng điều kiện thực tế không hỗ trợ, áp dụng các quy tắc môi trường của mục này. Hạt không bắt buộc phải nhìn thấy; nước tự nhiên không bắt buộc đục. Nhịp key và độ hấp dẫn không được dùng để phủ nhận giới hạn nhìn thực của camera.

### Khóa môi trường tự nhiên và góc máy ngay trong first frame

First frame phải mô tả **đúng nơi con vật có thể sống**, không chỉ một phông nền dưới nước đẹp. Chọn và ghi rõ các chi tiết phù hợp cảnh:

- **Địa lý và không gian sống:** vùng Mỹ, hồ/sông/lạch triều/bãi cỏ biển/mép oyster, nước ngọt/lợ/mặn; độ sâu, độ dốc, khoảng mở giữa cá–mồi, vật che và đường di chuyển. Cây, vật liệu đáy, sinh vật phụ phải hợp cùng một hệ sinh thái và có tỷ lệ thật.
- **Mùa, giờ và thời tiết:** nêu một tổ hợp nhất quán, ví dụ đầu thu, chiều trời nhiều mây, gió nhẹ. Thời tiết phải được thể hiện bằng **hệ quả dưới nước** như ánh sáng tán xạ, dao động mặt nước, vân sáng hoặc độ đục có lý do; không bắt vẽ bầu trời hay hạt mưa rơi như trên cạn trong một khung hoàn toàn chìm. Không tự thêm bão, mưa, sóng hay bùn dày chỉ để tăng kịch tính.
- **Màu sắc đời thực:** màu thân/vây/đốm cá dưới nguồn sáng và đường đi ánh sáng trong nước; màu bùn, sỏi, cỏ, hàu và nước có độ biến thiên tự nhiên. Vật xa mất chi tiết/tương phản đúng môi trường; không dùng màu đỏ/cam bão hòa, teal–orange, HDR bóng bẩy hoặc nền xanh nhiệt đới cho mọi loài.
- **Camera ngoài đời:** Underwater mặc định camera cầm tay tự nhiên như người quay điện thoại chống nước, chi tiết theo [format Underwater — UF-D021](../../03-Projects/underwater/format.md#camera-cầm-tay-tự-nhiên--uf-d021); người cầm và thiết bị nằm ngoài khung. Máy ở vị trí người quay có thể tới thật, chiều cao thấp, hướng nhìn và góc rộng vừa phải. Góc ngang/hơi chếch hợp khoảng cách và địa hình; phối cảnh tự nhiên, không canh cả cá và mồi như ảnh quảng cáo. Không mặc định góc máy điện ảnh, hero shot, góc bay, dolly, gimbal/orbit phô diễn, ánh sáng sân khấu, bokeh kịch tính hoặc lao máy đuổi theo cá. Chỉ dùng phong cách/góc điện ảnh khi người dùng yêu cầu rõ; camera cố định chỉ khi người dùng hoặc brief đã chốt yêu cầu.

Giữ cùng tổ hợp môi trường/thời tiết/nguồn sáng từ ảnh t=0 sang video. Sự chân thực không có nghĩa phải làm ảnh tối hoặc bẩn quá mức: điểm key và mối quan hệ cá–mồi vẫn phải đọc được.


| Loài và cảnh hợp lý | Vật liệu thật trong khung | Nước và ánh sáng | Mồi/con mồi, kiểu tiếp cận | Dấu hiệu sai cần sửa |
|---|---|---|---|---|
| **Redfish:** rìa đầm mặn Louisiana/Texas; lạch thủy triều Florida; bãi cỏ biển, bùn hoặc mép oyster ở nước lợ/ven biển | Rễ/cọng cỏ mặn, bùn mịn, vỏ oyster không đều; cua/tôm/cá nhỏ; chỗ nước chảy quanh cỏ | Nông, hơi tannin hoặc phù sa; nắng tán qua mặt nước nếu ban ngày; cỏ đung đưa theo dòng | Cúi đầu dò đáy, có thể tailing; tiến tới cua/tôm hoặc jig thích hợp; đuôi khuấy bùn tại điểm đó | Hồ nước ngọt kiểu hồ núi; cá đỏ rực đồng nhất; ria cằm như black drum; spot đuôi chuyển chỗ giữa các frame |
| **Walleye:** hồ/sông ở Wisconsin, Minnesota hoặc vùng Great Lakes; điểm đá/sỏi, mép thảm cỏ | Sỏi đủ cỡ, tảng đá, ít cành/cỏ địa phương; minnow hoặc jig nhỏ ở độ cao hợp lý | Hoàng hôn/bình minh hoặc nước hơi đục; nếu giữa ngày và nước trong, cá thường ở sâu/tối hơn | Bơi dò tìm con mồi, áp sát và hút/đớp ngắn; đôi khi chỉ theo rồi bỏ | Bãi oyster nước mặn; chiếu sáng nhiệt đới giữa trưa trong veo; mắt phát sáng như đèn LED |
| **Muskie:** hồ mát/sông lớn miền Bắc; mép cỏ thủy sinh, gốc gỗ, gờ đá hoặc hố nước chậm | Bẹ cỏ “cabbage”, gỗ chìm/đá có kích thước thật; baitfish hoặc lure lớn phù hợp | Độ trong đủ để cá săn bằng thị giác; ánh sáng tự nhiên, vùng tối sau cỏ/gỗ | **Một** cá đơn độc núp/đi theo; tăng tốc một lần, đớp ngang con mồi hoặc hụt | Đàn nhiều muskie; hoa văn/vây biến thành northern pike; cá đứng bất động rồi dịch chuyển tức thời |

Đối chiếu nhận dạng và hành vi với [Texas Parks & Wildlife về red drum](https://tpwd.texas.gov/fishing/sea-center-texas/flora-fauna-guide/bays-and-estuaries/bay-animals/red-drum), [Florida FWC về red drum](https://myfwc.com/wildlifehabitats/profiles/saltwater/drums/red-drum/), [Wisconsin DNR về walleye](https://dnr.wisconsin.gov/sites/default/files/topic/Fishing/Species_walleye.pdf) và [Wisconsin DNR về muskie](https://dnr.wisconsin.gov/sites/default/files/topic/Fishing/Musky_MuskellungeFactSheet2012.pdf).

### Nước đục kiểu Underfishing: áp dụng khác nhau cho ba loài

**Nhận xét từ ảnh tham chiếu:** nhiều thumbnail có lớp nước xanh lục, xanh lam lẫn hạt, hoặc xám nâu; cá ở xa mờ và ít tương phản, trong khi miệng/mồi gần đáy còn đọc được. Có cảnh bụi đáy bùng **sau** khi cá quẫy. Đây là **độ đục cục bộ và có chiều sâu**, không phải phủ một lớp sương đồng nhất lên toàn màn hình. Thumbnail không đủ để suy ra độ đục đo bằng NTU hoặc độ sâu nhìn bằng đĩa Secchi.

| Loài | Độ đục có hợp sinh thái không? | Cấu hình cảnh nên dùng | Khi nào cần giảm độ đục |
|---|---|---|---|
| **Redfish** | **Có, rất hợp cho một số cảnh ven bờ.** Cửa sông pha nước ngọt–mặn có thể sẫm và đục; red drum thường kiếm ăn ở nước nông, nền bùn mềm, cỏ biển hoặc mép oyster. Nhưng không phải mọi bãi cỏ biển hay vùng redfish đều đục. | Lạch thủy triều/bãi bùn Louisiana hoặc Texas; nước lợ **nâu xanh/olive**, phù sa mịn lơ lửng, bùn chỉ bốc thêm khi đầu/đuôi chạm đáy. Ở gần camera thấy rõ mồi và đốm đuôi; cá xa là bóng đồng nâu nhạt, mép cỏ mờ dần. Nếu dùng mép oyster, giữ vỏ sắc nét trong tiền cảnh và mềm đi ở hậu cảnh. | Cảnh bãi cỏ biển Florida nắng đẹp hoặc nước nông rất trong; giảm lớp phù sa nền, vẫn giữ mất tương phản theo khoảng cách. |
| **Walleye** | **Có, ở mức vừa phải rất hợp.** Wisconsin DNR nói walleye ở nước trong thường trú sâu ban ngày và vào nông ban đêm; ở nước đục hơn có thể hoạt động cả ban ngày. Walleye cũng sống trong nhiều loại hồ, nên không bắt buộc nước đục ở mọi cảnh. | Hồ/sông phía bắc có nước **xanh rêu, nâu trà hoặc xám lục**; sỏi và jig rõ ở tiền cảnh, mép đá xa mềm và tối. Nước hơi đục hoặc ánh chiều tối tạo lợi thế thị giác cho cá, nhưng vẫn đủ để mắt, vây lưng và chóp trắng đuôi nhận ra khi cá tới gần. Có thể dùng bùn rất mịn ở khe sỏi; tránh đám bùn dày phủ cả bãi đá. | Hồ nước trong giữa ngày: đặt camera/cá sâu hơn hoặc dưới bóng cấu trúc; cảnh đêm/hoàng hôn có thể khá trong mà vẫn đúng loài. |
| **Muskie** | **Chỉ đục nhẹ đến vừa trong cảnh săn bằng mắt.** Wisconsin DNR mô tả muskie dựa nhiều vào thị giác và gặp khó hơn khi nước quá đục. Nó có thể ở hồ/sông với biến thiên độ trong; một lớp haze tự nhiên hợp lý, nhưng “súp bùn” kín tầm nhìn kém hợp cảnh nó phát hiện mồi từ xa và lao chính xác. | Hồ mát Wisconsin/Minnesota: nước **xanh lục dịu hoặc nâu trà trong vừa**, hậu cảnh mờ nhẹ, thảm cỏ và thân cá ở khoảng vài mét vẫn có bóng/hướng rõ. Đặt muskie núp sau cỏ/gỗ, mồi đi vào **tầm nhìn gần**, cú lao bắt đầu khi khoảng cách đã ngắn. Đám silt riêng chỉ nổi khi đuôi quét sát đáy hoặc vật va vào nền. | Nếu muốn mây đục dày như các Reel cá chép, đặt nó **sau cú lao** để che kết quả; không cho muskie khóa mồi ở xa qua nước đặc như sữa. |

Cơ sở: [Texas Parks & Wildlife về nước cửa sông thường sẫm/đục](https://tpwd.texas.gov/education/resources/aquatic-science/tas/chapters/chapter-6/) và [môi trường red drum](https://tpwd.texas.gov/huntwild/wild/species/reddrum/); [Wisconsin DNR về walleye trong nước trong/đục](https://dnr.wisconsin.gov/topic/Fishing/species/walleye.html); [Wisconsin DNR về muskie săn bằng thị giác và khó kiếm ăn hơn khi nước đục](https://dnr.wisconsin.gov/sites/default/files/topic/Fishing/Musky_MuskellungeFactSheet2012.pdf). [NOAA](https://repository.library.noaa.gov/view/noaa/44989/noaa_44989_DS1.pdf) giải thích hạt lơ lửng làm giảm tương phản và tầm nhìn ảnh dưới nước.

**Quy tắc dựng ảnh, không phải ngưỡng sinh học:** chọn khoảng nhìn *theo chiều ngang của camera* đủ cho câu chuyện. Ví dụ, với redfish cho mồi rõ trong ~0,3–0,7 m và cá chỉ thành bóng ở ~1,5–2 m; với walleye cho tiền cảnh rõ và cá mờ ở ~2–3 m; với muskie cho cá còn nhận được dáng ở ~2–4 m trước cú lao. Các khoảng này là **gợi ý bố cục để model sinh ảnh**, không phải số đo bắt buộc của hồ/sông, và **không được đổi thẳng từ độ sâu Secchi**. Nếu muốn nước đục hơn, kéo cá xuất hiện gần camera hơn; không giữ cá xa mà vẫn nhìn sắc như ảnh studio.

**Cách khóa môi trường trong prompt:** viết đủ sáu chi tiết theo thứ tự: `kiểu nước + nguồn đục + màu nền + mức nhìn xa + vật gần/vật xa + đám bùn phát sinh`. Ví dụ: “slightly tannic, sediment-bearing brackish creek water; olive-brown cast; shell and crab sharp within 50 cm, redfish silhouette soft at 1.5 m; a small local silt plume only after the tail brushes the mud.” Không dùng riêng từ “murky” vì model dễ phủ màn sương phẳng. Nếu có hạt lơ lửng nhìn thấy, chúng phải có phân bố phù hợp và không đều sáng như tuyết; màu nước, tán xạ và độ tương phản phải duy trì cùng trạng thái suốt shot trừ biến cố vật lý thấy được.

**Chống tiền cảnh quá sạch:** tiền cảnh đủ rõ để hiểu hành động, nhưng bùn có hạt mịn lẫn hạt thô, vỏ hàu/đá có mép mòn và mảng bám không đều, cỏ có lá gãy hoặc bị che một phần. Chỉ thêm hạt phù sa nhìn thấy khi hợp điều kiện nghiên cứu, ở các độ sâu khác nhau với kích cỡ/độ sáng khác nhau; một số hạt đi theo dòng rất chậm, không thành lớp hạt dày phủ đều. Tránh viền vật thể sắc như ảnh sản phẩm, bề mặt đồng nhất, sắp xếp vỏ/đá cân đối, ánh sáng rọi đều vào cả cá lẫn con mồi. Giữ chi tiết gần có chọn lọc; giảm độ rõ và tương phản của cá ở xa bằng tán xạ nước **ngay từ t=0**, không thêm màn sương toàn khung hoặc làm mờ giả toàn ảnh.

**Xếp ba lớp trong khung dọc 9:16:** (1) **tiền cảnh** 0–0,7 m: một mồi/con mồi, vài vật đáy đủ rõ để mắt người xem bám vào; hạt gần ống kính chỉ thêm nếu điều kiện nước hỗ trợ; (2) **trung cảnh** khoảng 0,7–2 m: đường cá đi vào hoặc chỗ cá núp, độ tương phản giảm nhẹ; (3) **hậu cảnh**: cỏ, đá, gốc gỗ hoặc bờ dần hòa vào màu nước, không dựng một “tường sương” phẳng. Số mét chỉ là gợi ý dàn cảnh. Với redfish thay hậu cảnh bằng rễ/cỏ mặn hay mép oyster; với walleye dùng bãi sỏi/gờ đá, bóng tối tăng ở xa; với muskie dùng mép thảm cỏ/gỗ chìm còn đủ hình dạng để cú phục kích đọc được. Nếu đã có mây bùn ở t=0, phải có nguyên nhân vừa xảy ra ngoài khung; mặc định bắt đầu bằng độ đục nền ổn định rồi mới thêm mây bùn từ hành động trong video.

### Chi tiết sinh học cần giữ ổn định

- **Redfish / red drum — *Sciaenops ocellatus*:** thân đồng ánh nâu đến bạc tùy nước, bụng nhạt, một hoặc nhiều đốm đen ở gốc đuôi; **không có râu cằm**. Đầu chúc xuống khi kiếm cua, tôm, giun biển hoặc cá nhỏ; đuôi có thể nhô trên mặt nước nông. Đừng vẽ răng nanh to ở miệng. Đốm đuôi là điểm nhận dạng cố định trên cùng một cá suốt video.
- **Walleye — *Sander vitreus*:** thân olive-vàng/đồng, bụng sáng, vây lưng trước có gai và đốm sẫm ở góc sau dưới; chóp trắng ở phần dưới vây đuôi. Mắt lớn phản sáng **khi có tia sáng tới đúng góc**, không tự phát quang. Cú đớp mồi của cá săn mồi phải diễn ra sau khi nó rút ngắn khoảng cách. Có thể có vài cá cùng khu vực, nhưng không cần dựng đội hình bơi đồng bộ.
- **Muskie — *Esox masquinongy*:** thân dài, mõm bẹt thuôn, hàm răng nhọn, vây lưng và vây hậu môn nằm lùi về gần đuôi; hoa văn vạch/đốm sẫm trên nền sáng biến thiên theo cá. Đừng trộn với pike có các đốm sáng trên nền sẫm. Muskie thường đơn độc, phục kích bên cỏ/gỗ/đá và lao ngắn có định hướng; không rỉa hạt mồi ở đáy kiểu cá chép.

## 3. Quy luật hình ảnh dưới nước tạo cảm giác quay thật

**Khoảng cách và độ trong.** Xác định khoảng nhìn hữu ích, chẳng hạn một vài mét hoặc ít hơn trong lạch nhiều phù sa. Vật ở xa phải giảm tương phản và mất chi tiết trước khi đến gần. Không cho đáy xa sắc nét hơn mõm cá gần máy. Độ đục phải nhất quán trong cả cảnh, trừ một đám bùn mới phát sinh tại vị trí bị khuấy. Hạt lơ lửng có kích thước và mật độ không đều; chúng **không phải màn tuyết hạt trắng đồng đều**. Hấp thụ và tán xạ ánh sáng làm màu thay đổi theo đường đi trong nước, nên đừng tô cá đỏ/cam bão hòa như ảnh trên cạn. [Nghiên cứu lưu trữ tại NOAA về màu ảnh dưới nước](https://repository.library.noaa.gov/view/noaa/70095) và [NOAA về ánh sáng, màu ở độ sâu](https://oceanexplorer.noaa.gov/lesson/bioluminescence-light-and-color/) hỗ trợ nguyên tắc này.

**Ánh sáng.** Quyết định một thời điểm: trưa nắng nông, trời âm u, hoàng hôn, hoặc bóng mát dưới cỏ. Chỉ vẽ vân nắng dao động trên đáy khi có ánh mặt trời trực tiếp và nước đủ nông/trong. Với walleye ở chiều tối, cảnh nên tối vừa đủ để vẫn đọc được cá và mồi, không dùng đèn sân khấu chiếu riêng lên thân. Một nguồn sáng từ phía trên tạo bóng và độ tương phản phù hợp ở mọi vật, kể cả dây, mồi và cỏ.

**Máy quay và khung.** Camera cầm tay theo [format Underwater — UF-D021](../../03-Projects/underwater/format.md#camera-cầm-tay-tự-nhiên--uf-d021): máy thấp, góc nhìn ngang/hơi chếch lên, ống kính góc rộng vừa phải; trôi và chỉnh khung nhẹ, không đều như tay người, không khóa vị trí/hướng máy. Giữ tiêu cự thực ổn định, phơi sáng/màu nước liên tục suốt 10 giây; khi máy dịch, vật chỉ đổi vị trí tương đối theo parallax, vẫn giữ vị trí trong không gian, kích thước và hình thể. Mép khung có thể bị cỏ/vỏ sò chắn một phần; bụi đáy và thân cá có thể che máy thoáng chốc. Cho cá tiến **trong không gian**, lớn lên vì tới gần ống kính, không vì crop/zoom. Tránh dolly, drone underwater, gimbal/orbit quá hoàn hảo, rung mạnh, zoom số, chuyển nét kịch tính hoặc cut đúng lúc cá đớp. Không cố làm footage bẩn bằng quá nhiều noise, méo ống kính, vignetting hay bong bóng giả.

**Tránh cảm giác cảnh được dàn:** trước khi chốt first frame, nhìn xem cá và con mồi có đang cùng sáng, cùng nét, cùng phô toàn thân ở hai vị trí “đẹp” không. Nếu có, che bớt **một** mép bằng cỏ/hàu/đá đúng địa hình, cho vật xa mất tương phản, hoặc đặt con mồi lệch trục cá một chút. Giữ điểm quan sát chính đọc được trên điện thoại. Không phá bố cục bằng lỗi ống kính giả; sự bất toàn phải có nguyên nhân quang học/vật lý trong cảnh.

**Tỷ lệ.** Ghi chiều dài cá, mồi và khoảng cách ở mức tương đối hợp lý. Cua nhỏ bên cạnh redfish, jig nhỏ hơn mõm walleye, baitfish/lure đủ kích thước để muskie chú ý. Cỏ, sỏi, móc câu và dây phải có tỷ lệ thống nhất khi cá đi qua. Một cá lớn gần máy có thể lấp khung; nó không thể đột ngột tăng gấp đôi chiều dài ở cùng khoảng cách.
