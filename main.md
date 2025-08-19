# Project Build Hệ Thống Quản Lý Resource Idle Của FJP

## I. Yêu Cầu Về Tính Năng

### 1. Login
Có tính năng login, sign up.

### 2. Phân Quyền
1. **Admin**: Cấp quyền cho các role.
2. **RA**: Input/Import/Export/Update thông tin về idle resource.
   - RA All
   - RA bộ phận
3. **MNG**: View thông tin idle, status xử lý.
4. **Viewer**: Dept supportor + MNG khác view all thông tin idle của FJP (ko view được status xử lý idle).

### 3. Màn Hình Quản Lý Idle List
#### Quyền RA
- Update thông tin Idle idle, ngày idle, thông tin deploy, giá bán…
- Ngôn ngữ: EN, JP.
- Log các đánh giá: đánh giá từ RA, đánh giá qua các lần phỏng vấn, thông tin refer đặc biệt.
- Lấy thông tin của idle resource từ excel (skill, năng lực tiếng Nhật, đánh giá performance CHE…).
- Up CV của nhân viên idle -> AI đọc CV vào màn hình skill (CV theo temp hoặc ko theo temp).
- Input/Import/Export thông tin nhân sự idle + program các bạn sắp tốt nghiệp.
- Cho phép Search (Header...), Filter, Update multi Selection (add thông tin cụ thể 1 vài cái cần thiết) (V0.2).
- Drop downlist cho phép support search (V0.2).
- Cho phép Hide/UnHide các cột, cho phép Freeze/Unfreeze (V0.3).
- Cho phép High light màu vàng với những case chưa chốt chính thức ngày Idle From (V0.3).
- Phase 2: Master data: Cho phép custom Dropdownlist.
- Từng record sẽ có lưu lại history update.

#### Quyền Manager
- View thông tin idle của bộ phận, tình trạng giải quyết.
- Update/add new member idle.

#### Quyền Viewer
- View danh sách idle của toàn FJP (xem xét lại phần quyền cho view giá bán).
- Không cho view các case có trạng thái "Not Yet Open" (V0.3).
- Download CV pdf.

## II. Màn Hình/Template
1. **Login**
2. **Phân quyền**: Phân quyền tĩnh. RA sẽ có theo All, RA bộ phận.
3. **RA MNG** (*: Mandatory Field khi Export/Import)

### Bảng Dữ Liệu Mẫu
| No | Source | Full name | Account | Department | Child Department | Idle MM | Type | Idle From | Idle To | Progress note | RA PIC | Change Dept/Lending | Urgent case | HR manage | Special Action type | Skill | Experience IT | JP Level | EN level | National | Current location | Expected Working place | Note Expected Working place | Job rank | FJP Join date | Current Dept comment | Interview comment | Performance CHE | Sale price (JPY) | Visa Status | Application date | Expired COE date |
|----|--------|-----------|---------|------------|------------------|---------|------|-----------|---------|---------------|--------|---------------------|-------------|-----------|---------------------|-------|---------------|----------|----------|---------|------------------|-----------------------|--------------------------|----------|---------------|---------------------|-------------------|-----------------|------------------|-------------|------------------|------------------|
| 1 | FJPer | Nguyen Van An | AnNV | FJP RA | RA RDC | 1 | To be Idle | 45916 |  | [9-May] Join opp from 12-May to 15-Sep | HuongNTT6 | Change Dept or Lending | No | No |  | BrSE, test | 6 năm | N2- | 0 | Japanese | Tokyo | Tokyo |  | DEVE02 | 43228 |  | [14-Jul] … [7-Jul]… |  | 120 |  |  |  |
| 2 | BA Program | Nguyen Thi Be | BeNT | FJP FA | FA G1D | 1 | To be Idle | 45870 |  | [6-Jun] Secom GMG Reject Failed CV, Failed interview | HuongNTT6 | Not Yet Open | Yes | YES | MO | Java, C#, PHP, XML、HTML, Python | 日本で勤務年数: 6年 | N2 | Intermediate | Vietnamese | Việt Nam | Tokyo, Ibaraki |  | DEVE03 | 43436 |  |  |  | 85 |  |  |  |

### Yêu Cầu Về Dữ Liệu
| Field | Requirement |
|-------|-------------|
| No | Auto gen |
| Source | Drop down list |
| Full name | Full name theo tên quốc tịch |
| Account | Acc FPT |
| Department | Drop down list |
| Child Department | Drop down list |
| Idle MM | Number |
| Type | Drop down list |
| Idle From | Calendar |
| Idle To | Calendar |
| Progress note | Text |
| RA PIC | Acc FPT |
| Change Dept/Lending | Drop down list |
| Urgent case | Yes/No (Auto fill = YES nếu >=2 tháng) |
| HR manage | Yes/No |
| Special Action type | Drop down list và tự quản lý danh sách |
| Skill | Text |
| Experience IT | Text |
| JP Level | Drop down list |
| EN level | Drop down list |
| National | Drop down list |
| Current location | Drop down list |
| Expected Working place | Drop down list |
| Note Expected Working place | Text |
| Job rank | Drop down list |
| FJP Join date | Calendar |
| Current Dept comment | Text |
| Interview comment | Text |
| Performance CHE | Text |
| Sale price (JPY) | Number |
| Visa Status | Text |
| Application date | Text |
| Expired COE date | Text |
