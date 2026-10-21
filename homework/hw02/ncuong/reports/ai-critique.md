# AI Critique (HW02 §10)

Trong bài HW02, AI giúp em chia lớp tương đương, chọn điểm biên và lập bộ test cho cả bốn feature. Tuy nhiên, bộ ca ban đầu vẫn thiếu những tình huống phải kết hợp dữ liệu, quyền người dùng và giao diện.

Ở FR-02, AI thử email sai định dạng bằng tài khoản chưa tồn tại và chỉ thấy API trả 401. Khi em tạo tài khoản mang email đó rồi đăng nhập trên web, form vẫn cho gửi và đăng nhập được. AI cũng chưa tách `password` vắng hẳn với `password: null`; ca `null` làm lộ lỗi cấp JWT cho tài khoản không có mật khẩu hợp lệ. Ở FR-10, AI luôn dùng token admin trong các ca đổi trạng thái, nên chưa thử user thường gọi API Admin và tự đổi trạng thái đơn.

Với FR-17, đặc tả chỉ yêu cầu giá trị giảm dương nên AI không xét coupon giảm hơn 100%. Em thấy mức 150% không hợp lý, đề xuất giới hạn rồi chạy thêm ca để kiểm chứng. Ở FR-06, AI chấm PASS khi thêm hai chiếc vì quantity trong giỏ đúng, nhưng nhãn “Giỏ (1)” có thể khiến người mua hiểu sai. Vì đặc tả chưa nói badge đếm số dòng hay tổng số món, em ghi đây là điểm cần làm rõ chứ chưa kết luận bug.

Qua bốn feature, em thấy AI hữu ích để tạo khung kiểm thử nhưng không thể thay phần đánh giá nghiệp vụ. Em cần đọc lại yêu cầu, tách các đầu vào dễ bị gộp, thử theo thao tác thực tế và lưu bằng chứng. Với điều chưa rõ, em nên hỏi hoặc ghi giả thuyết trước khi báo lỗi.
