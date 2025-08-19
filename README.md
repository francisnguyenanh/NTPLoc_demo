# Hệ Thống Quản Lý Idle Resource

Một ứng dụng web Flask để quản lý thông tin nhân viên idle trong lĩnh vực outsource phần mềm.

## Tính năng chính

### 1. Đăng nhập và phân quyền
- **Admin**: Quản lý toàn bộ hệ thống, cấp quyền cho user, quản lý dropdown data
- **RA (Resource Administrator)**: Input/Import/Export/Update thông tin idle resource
- **MNG (Manager)**: View thông tin idle của bộ phận, tình trạng giải quyết
- **Viewer**: View danh sách idle của toàn FJP (không view status "Not Yet Open")

### 2. Dashboard
- Tổng quan thống kê nhân viên theo trạng thái
- Thống kê theo bộ phận
- Hiển thị số lượng trường hợp khẩn cấp

### 3. Quản lý Idle Resource
- Danh sách nhân viên idle với đầy đủ thông tin
- Thêm mới nhân viên idle
- Chỉnh sửa thông tin nhân viên
- Xem lịch sử thay đổi dữ liệu
- Xóa nhân viên (soft delete)
- Phân trang và lọc dữ liệu

### 4. Settings (Chỉ Admin)
- Quản lý người dùng: thêm user mới, tự động tạo password
- Quản lý Dropdown Data: thêm/xóa/sửa các giá trị dropdown list

### 5. Report (Sẵn sàng để phát triển)
- Menu report đã được tạo, chưa implement logic

## Cấu trúc dữ liệu

### Bảng Employee (Nhân viên)
Chứa đầy đủ 32+ trường thông tin theo yêu cầu từ main.md:

#### Thông tin cơ bản:
- **No**: Auto-generated ID (STT)
- **Source**: Nguồn (FJPer, FJP-Center, BA Program, XPM Program, External)
- **Full name**: Họ tên đầy đủ theo quốc tịch (*)
- **Account**: Account FPT (*)
- **Department**: Bộ phận (dropdown list)
- **Child Department**: Bộ phận con (dropdown list)

#### Thông tin Idle:
- **Idle MM**: Số tháng idle (number)
- **Type**: Loại idle (Being Idle, To be Idle, Idle Short Term, etc.)
- **Idle From**: Ngày bắt đầu idle (calendar)
- **Idle To**: Ngày kết thúc idle (calendar)
- **Progress note**: Ghi chú tiến độ (text)
- **RA PIC**: Người phụ trách RA (Account FPT)

#### Thông tin trạng thái:
- **Change Dept/Lending**: Trạng thái thay đổi bộ phận/lending (dropdown)
- **Urgent case**: Trường hợp khẩn cấp (Yes/No - auto fill nếu >=2 tháng)
- **HR manage**: HR quản lý (Yes/No)
- **Special Action type**: Loại hành động đặc biệt (dropdown có thể custom)

#### Thông tin kỹ năng:
- **Skill**: Kỹ năng (text)
- **Experience IT**: Kinh nghiệm IT (text)
- **JP Level**: Trình độ tiếng Nhật (dropdown: Native, N1, N2, N2-, N3, No JP)
- **EN level**: Trình độ tiếng Anh (dropdown với TOEIC levels)

#### Thông tin địa điểm:
- **National**: Quốc tịch (dropdown)
- **Current location**: Địa điểm hiện tại (dropdown)
- **Expected Working place**: Nơi làm việc mong muốn (dropdown)
- **Note Expected Working place**: Ghi chú nơi làm việc (text)

#### Thông tin công việc:
- **Job rank**: Cấp bậc công việc (dropdown với codes như DEVE01, FSEN02, etc.)
- **FJP Join date**: Ngày vào FJP (calendar)

#### Thông tin đánh giá:
- **Current Dept comment**: Nhận xét bộ phận hiện tại (text)
- **Interview comment**: Nhận xét phỏng vấn (text)
- **Performance CHE**: Đánh giá performance CHE (text)

#### Thông tin tài chính & visa:
- **Sale price (JPY)**: Giá bán (number)
- **Visa Status**: Tình trạng visa (text)
- **Application date**: Ngày apply (text)
- **Expired COE date**: Ngày hết hạn COE (text)

#### Trường hệ thống:
- **is_deleted**: Soft delete flag (boolean)
- **created_at**: Ngày tạo (datetime)
- **updated_at**: Ngày cập nhật (datetime)

(*) = Trường bắt buộc khi Export/Import

### Bảng DropdownData
Quản lý các giá trị dropdown list có thể custom được

### Bảng EmployeeHistory
Lưu trữ lịch sử thay đổi dữ liệu của nhân viên

## Cài đặt và chạy

### 1. Cài đặt dependencies
```bash
cd idle_management_system
pip install -r requirements.txt
```

### 2. Chạy ứng dụng
```bash
python app.py
```

### 3. Truy cập ứng dụng
- URL: http://localhost:5000
- Admin mặc định:
  - Username: `admin`
  - Password: `admin123`

## Thông tin kỹ thuật

### Backend
- **Framework**: Flask 2.3.3
- **Database**: SQLite với SQLAlchemy ORM
- **Authentication**: Flask-Login
- **Password hashing**: Werkzeug

### Frontend
- **CSS Framework**: Bootstrap 5.1.3
- **Icons**: Font Awesome 6.0.0
- **JavaScript**: Vanilla JavaScript với Bootstrap JS

### Cấu trúc project
```
idle_management_system/
├── app.py                 # Main application file
├── extensions.py          # Flask extensions initialization
├── models.py             # Database models
├── requirements.txt      # Python dependencies
├── routes/               # Route blueprints
│   ├── __init__.py
│   ├── auth.py          # Authentication routes
│   ├── main.py          # Main dashboard routes
│   ├── settings.py      # Settings management routes
│   └── idle_management.py # Idle resource management routes
├── templates/           # Jinja2 templates
│   ├── base.html        # Base template
│   ├── login.html       # Login page
│   ├── dashboard.html   # Dashboard
│   ├── settings.html    # Settings page
│   ├── idle_management.html # Idle list view
│   ├── add_employee.html    # Add employee form
│   ├── edit_employee.html   # Edit employee form
│   ├── employee_history.html # Employee history
│   └── report.html         # Report page
└── static/              # Static files
    ├── css/
    │   └── style.css    # Custom CSS
    └── js/
        └── app.js       # Custom JavaScript
```

## Tính năng nổi bật

### 1. Phân quyền linh hoạt
- 4 loại role với quyền hạn khác nhau
- Kiểm soát truy cập ở mức route và view

### 2. Quản lý dropdown data động
- Admin có thể thêm/xóa/sửa các giá trị dropdown
- Dữ liệu được lưu trong database, không hardcode

### 3. Lịch sử thay đổi chi tiết
- Theo dõi tất cả thay đổi dữ liệu
- Lưu trữ giá trị cũ và mới
- Ghi nhận người thực hiện và thời gian

### 4. Auto-update logic
- Tự động đánh dấu "Urgent case" khi idle >= 2 tháng
- Cập nhật timestamp khi có thay đổi

### 5. Responsive design
- Giao diện thân thiện trên mobile và desktop
- Sử dụng Bootstrap components

## Hướng phát triển tiếp theo

1. **Export/Import Excel**: Xuất/nhập dữ liệu từ file Excel
2. **Report nâng cao**: Biểu đồ, báo cáo định kỳ
3. **Search và Filter nâng cao**: Full-text search, multi-field filter
4. **Email notification**: Thông báo khi có thay đổi quan trọng
5. **API endpoints**: Tích hợp với hệ thống khác
6. **Audit log**: Log chi tiết các hoạt động của user

## Lưu ý bảo mật

- Mật khẩu được hash bằng Werkzeug
- Session-based authentication
- CSRF protection cần được thêm vào cho production
- Cần thay đổi SECRET_KEY cho production
