# Simple Object Detection

# Đề bài:

Trong bài tập lần này, bạn sẽ thực hiện bài toán nhận diện đối tượng trên Video được cung cấp sẵn bằng cách sử dụng thư viện OpenCV. Thông qua bài tập, bạn sẽ được làm quen nhiều hơn với các kỹ thuật xử lý ảnh cơ bản đã được học và phương pháp phát hiện đối tượng không sử dụng mô hình Deep Learning phức tạp.

Link Video: https://pixabay.com/videos/roads-motorways-highway-1952

## Yêu cầu:

1. Phát hiện đối tượng

- Nhiệm vụ của bạn là phát hiện các phương tiện giao thông xuất hiện trong video bằng cách sử dụng thư viện OpenCV.
- Ưu tiên các đối tượng nằm trong nửa khung hình bên dưới (phần dưới của video).

2. Vẽ bounding box

- Bạn cần vẽ 1 bounding box xung quanh mỗi xe phát hiện được trong khung hình.
- Bounding box phải di chuyển cùng với chuyển động của các xe trong từng frame của video.
- Có thể xảy ra trường hợp cùng 1 xe có nhiều bounding box, hãy sử dụng các kỹ thuật đã học để loại bỏ các bounding box
  dư thừa của cùng 1 xe.
- Bạn cần vẽ được toàn bộ bounding box cho tất cả các các xe xuất hiện trong nửa khung hình bên dưới.
- Đồng thời, vẽ được tối đa lượng bounding box có thể cho các xe xuất hiện trong nửa khung hình bên trên.

3. Đếm số lượng xe trong mỗi làn đường

- Chọn 1 khoảng diện tích cố định ở mỗi làn đường, hiển thị vùng diện tích lên video.
- Dựa vào bounding box có được, bạn cần đếm số lượng xe xuất hiện trong vùng diện tích đó ở mỗi frame.
- Hiển thị số lượng xe trực tiếp trên video (VD: "Làn trái: 1 | Làn phải: 1" hiển thị ở góc trên cùng bên phải).

4. Xác định hướng đi của xe

- Đặt 1 đường kẻ ngang video. Bạn cần xác định hướng đi của xe (lên hay xuống) sau khi chạm vào đường kẻ.
- Thay đổi màu sắc của bounding box tương ứng với từng hướng xe (VD: sau khi xe đi xuống và chạm line, bounding box
  chuyển sang màu xanh)

## Cách giải quyết:

Yêu cầu 1:

- Chuyển video sang thang gray
- Làm mờ video
- Thresholding sao cho phát hiện được xe

Yêu cầu 2:

- Dilation để các bộ phận tách rời của xe hợp vào làm một
- Tìm contour của các khối xe đó
- Vẽ bounding box dựa theo các contour

Yêu cầu 3:

- Vẽ vùng diện tích hai bên đường `cv2.polylines`
- Tạo biến đếm xe vùng bên trái và bên phải `left_car_count` và `right_car_count`, reset sau mỗi frame
- Tính tâm của bounding box
- Kiểm tra điểm đó có nằm trong vùng diện tích đó không bằng hàm `cv2.pointPolygonTest`, nếu có thì biến đếm cộng thêm 1.

Yêu cầu 4:

- Vẽ đường kẻ ngang trên video.
- Tạo dictionary `car_positions` để lưu trữ tọa độ ở tâm của xe ở frame trước và dictionary `current_centers` để lưu tọa độ ở tâm của xe frame hiện tại.
- Màu sắc mặt định của bounding box sẽ là màu xanh lá cây.
- So sánh tâm của xe ở frame trước với hiện tại:
  - Nếu tâm của xe ở frame hiện tại lớn hơn frame lúc trước thì chứng tỏ xe đang đi lên và chuyển màu của bounding box thành màu đen.
  - Ngược lại sẽ là đi xuống và chuyển bounding box thành màu vàng.

# Kết quả
