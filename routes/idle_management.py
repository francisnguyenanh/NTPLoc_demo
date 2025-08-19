from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import Employee, DropdownData, EmployeeHistory
from extensions import db
from datetime import datetime, date
from sqlalchemy import desc

idle_bp = Blueprint('idle', __name__)

@idle_bp.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    # Filter based on user role
    query = Employee.query.filter_by(is_deleted=False)
    
    if current_user.role == 'MNG':
        # Manager can only see their department
        query = query.filter_by(department=current_user.department)
    elif current_user.role == 'Viewer':
        # Viewer can see all but with restrictions
        query = query.filter(Employee.change_dept_lending != 'Not Yet Open')
    
    employees = query.order_by(desc(Employee.updated_at)).paginate(
        page=page, per_page=per_page, error_out=False)
    
    return render_template('idle_management.html', employees=employees)

@idle_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_employee():
    if current_user.role not in ['Admin', 'RA', 'MNG']:
        flash('Bạn không có quyền thêm nhân viên.', 'error')
        return redirect(url_for('idle.index'))
    
    if request.method == 'POST':
        # Create new employee
        employee = Employee()
        
        # Set all fields from form
        employee.source = request.form.get('source')
        employee.full_name = request.form.get('full_name')
        employee.account = request.form.get('account')
        employee.department = request.form.get('department')
        employee.child_department = request.form.get('child_department')
        employee.idle_mm = request.form.get('idle_mm', type=int)
        employee.type = request.form.get('type')
        
        # Handle dates
        idle_from_str = request.form.get('idle_from')
        if idle_from_str:
            employee.idle_from = datetime.strptime(idle_from_str, '%Y-%m-%d').date()
            
        idle_to_str = request.form.get('idle_to')
        if idle_to_str:
            employee.idle_to = datetime.strptime(idle_to_str, '%Y-%m-%d').date()
            
        fjp_join_date_str = request.form.get('fjp_join_date')
        if fjp_join_date_str:
            employee.fjp_join_date = datetime.strptime(fjp_join_date_str, '%Y-%m-%d').date()
        
        employee.progress_note = request.form.get('progress_note')
        employee.ra_pic = request.form.get('ra_pic')
        employee.change_dept_lending = request.form.get('change_dept_lending')
        employee.urgent_case = request.form.get('urgent_case', 'No')
        employee.hr_manage = request.form.get('hr_manage', 'No')
        employee.special_action_type = request.form.get('special_action_type')
        employee.skill = request.form.get('skill')
        employee.experience_it = request.form.get('experience_it')
        employee.jp_level = request.form.get('jp_level')
        employee.en_level = request.form.get('en_level')
        employee.national = request.form.get('national')
        employee.current_location = request.form.get('current_location')
        employee.expected_working_place = request.form.get('expected_working_place')
        employee.note_expected_working_place = request.form.get('note_expected_working_place')
        employee.job_rank = request.form.get('job_rank')
        employee.current_dept_comment = request.form.get('current_dept_comment')
        employee.interview_comment = request.form.get('interview_comment')
        employee.performance_che = request.form.get('performance_che')
        employee.sale_price_jpy = request.form.get('sale_price_jpy', type=int)
        employee.visa_status = request.form.get('visa_status')
        employee.application_date = request.form.get('application_date')
        employee.expired_coe_date = request.form.get('expired_coe_date')
        
        # Auto set urgent case if idle >= 2 months
        if employee.idle_mm and employee.idle_mm >= 2:
            employee.urgent_case = 'Yes'
        
        db.session.add(employee)
        db.session.commit()
        
        flash('Thêm nhân viên thành công!', 'success')
        return redirect(url_for('idle.index'))
    
    # Get dropdown data
    dropdown_data = get_all_dropdown_data()
    return render_template('add_employee.html', dropdown_data=dropdown_data)

@idle_bp.route('/edit/<int:employee_id>', methods=['GET', 'POST'])
@login_required
def edit_employee(employee_id):
    if current_user.role not in ['Admin', 'RA', 'MNG']:
        flash('Bạn không có quyền chỉnh sửa nhân viên.', 'error')
        return redirect(url_for('idle.index'))
    
    employee = Employee.query.get_or_404(employee_id)
    
    if request.method == 'POST':
        # Track changes for history
        changes = []
        
        # Check each field for changes
        fields_to_check = [
            'source', 'full_name', 'account', 'department', 'child_department',
            'idle_mm', 'type', 'progress_note', 'ra_pic', 'change_dept_lending',
            'urgent_case', 'hr_manage', 'special_action_type', 'skill',
            'experience_it', 'jp_level', 'en_level', 'national',
            'current_location', 'expected_working_place', 'note_expected_working_place',
            'job_rank', 'current_dept_comment', 'interview_comment',
            'performance_che', 'sale_price_jpy', 'visa_status',
            'application_date', 'expired_coe_date'
        ]
        
        for field in fields_to_check:
            old_value = str(getattr(employee, field) or '')
            new_value = str(request.form.get(field) or '')
            
            if field == 'idle_mm' or field == 'sale_price_jpy':
                new_value = request.form.get(field, type=int)
                if new_value is None:
                    new_value = ''
                else:
                    new_value = str(new_value)
            
            if old_value != new_value:
                changes.append({
                    'field_name': field,
                    'old_value': old_value,
                    'new_value': new_value
                })
                
                # Update the field
                if field in ['idle_mm', 'sale_price_jpy']:
                    setattr(employee, field, request.form.get(field, type=int))
                else:
                    setattr(employee, field, request.form.get(field))
        
        # Handle date fields separately
        date_fields = ['idle_from', 'idle_to', 'fjp_join_date']
        for field in date_fields:
            old_value = str(getattr(employee, field) or '')
            new_value_str = request.form.get(field)
            
            if new_value_str:
                new_date = datetime.strptime(new_value_str, '%Y-%m-%d').date()
                new_value = str(new_date)
                
                if old_value != new_value:
                    changes.append({
                        'field_name': field,
                        'old_value': old_value,
                        'new_value': new_value
                    })
                    setattr(employee, field, new_date)
            elif getattr(employee, field) is not None:
                changes.append({
                    'field_name': field,
                    'old_value': old_value,
                    'new_value': ''
                })
                setattr(employee, field, None)
        
        # Auto set urgent case if idle >= 2 months
        if employee.idle_mm and employee.idle_mm >= 2:
            if employee.urgent_case != 'Yes':
                changes.append({
                    'field_name': 'urgent_case',
                    'old_value': employee.urgent_case,
                    'new_value': 'Yes'
                })
                employee.urgent_case = 'Yes'
        
        # Save changes to history
        for change in changes:
            history = EmployeeHistory(
                employee_id=employee.id,
                field_name=change['field_name'],
                old_value=change['old_value'],
                new_value=change['new_value'],
                changed_by=current_user.username
            )
            db.session.add(history)
        
        employee.updated_at = datetime.utcnow()
        db.session.commit()
        
        flash('Cập nhật nhân viên thành công!', 'success')
        return redirect(url_for('idle.index'))
    
    # Get dropdown data
    dropdown_data = get_all_dropdown_data()
    return render_template('edit_employee.html', employee=employee, dropdown_data=dropdown_data)

@idle_bp.route('/history/<int:employee_id>')
@login_required
def employee_history(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    history = EmployeeHistory.query.filter_by(employee_id=employee_id).order_by(desc(EmployeeHistory.changed_at)).all()
    
    def get_field_display_name(field_name):
        field_names = {
            'source': 'Nguồn',
            'full_name': 'Họ tên',
            'account': 'Account',
            'department': 'Bộ phận',
            'child_department': 'Bộ phận con',
            'idle_mm': 'Số tháng idle',
            'type': 'Loại',
            'idle_from': 'Idle từ',
            'idle_to': 'Idle đến',
            'progress_note': 'Ghi chú tiến độ',
            'ra_pic': 'RA PIC',
            'change_dept_lending': 'Thay đổi bộ phận/Lending',
            'urgent_case': 'Trường hợp khẩn cấp',
            'hr_manage': 'HR quản lý',
            'special_action_type': 'Loại hành động đặc biệt',
            'skill': 'Kỹ năng',
            'experience_it': 'Kinh nghiệm IT',
            'jp_level': 'Trình độ tiếng Nhật',
            'en_level': 'Trình độ tiếng Anh',
            'national': 'Quốc tịch',
            'current_location': 'Địa điểm hiện tại',
            'expected_working_place': 'Nơi làm việc mong muốn',
            'note_expected_working_place': 'Ghi chú nơi làm việc',
            'job_rank': 'Vị trí công việc',
            'fjp_join_date': 'Ngày vào FJP',
            'current_dept_comment': 'Nhận xét bộ phận',
            'interview_comment': 'Nhận xét phỏng vấn',
            'performance_che': 'Đánh giá Performance CHE',
            'sale_price_jpy': 'Giá bán (JPY)',
            'visa_status': 'Tình trạng Visa',
            'application_date': 'Ngày apply',
            'expired_coe_date': 'Ngày hết hạn COE',
            'is_deleted': 'Trạng thái xóa'
        }
        return field_names.get(field_name, field_name)
    
    return render_template('employee_history.html', employee=employee, history=history, get_field_display_name=get_field_display_name)

@idle_bp.route('/delete/<int:employee_id>', methods=['POST'])
@login_required
def delete_employee(employee_id):
    if current_user.role not in ['Admin', 'RA']:
        return jsonify({'success': False, 'message': 'Không có quyền xóa'}), 403
    
    employee = Employee.query.get_or_404(employee_id)
    employee.is_deleted = True
    
    # Log the deletion
    history = EmployeeHistory(
        employee_id=employee.id,
        field_name='is_deleted',
        old_value='False',
        new_value='True',
        changed_by=current_user.username
    )
    db.session.add(history)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Xóa nhân viên thành công'})

@idle_bp.route('/employee/<int:employee_id>/detail')
@login_required
def get_employee_detail(employee_id):
    """API endpoint to get employee details for modal"""
    employee = Employee.query.get_or_404(employee_id)
    
    # Convert employee to dict
    employee_data = {
        'id': employee.id,
        'source': employee.source,
        'full_name': employee.full_name,
        'account': employee.account,
        'department': employee.department,
        'child_department': employee.child_department,
        'idle_mm': employee.idle_mm,
        'type': employee.type,
        'idle_from': employee.idle_from.strftime('%d/%m/%Y') if employee.idle_from else None,
        'idle_to': employee.idle_to.strftime('%d/%m/%Y') if employee.idle_to else None,
        'progress_note': employee.progress_note,
        'ra_pic': employee.ra_pic,
        'change_dept_lending': employee.change_dept_lending,
        'urgent_case': employee.urgent_case,
        'hr_manage': employee.hr_manage,
        'special_action_type': employee.special_action_type,
        'skill': employee.skill,
        'experience_it': employee.experience_it,
        'jp_level': employee.jp_level,
        'en_level': employee.en_level,
        'national': employee.national,
        'current_location': employee.current_location,
        'expected_working_place': employee.expected_working_place,
        'note_expected_working_place': employee.note_expected_working_place,
        'job_rank': employee.job_rank,
        'fjp_join_date': employee.fjp_join_date.strftime('%d/%m/%Y') if employee.fjp_join_date else None,
        'current_dept_comment': employee.current_dept_comment,
        'interview_comment': employee.interview_comment,
        'performance_che': employee.performance_che,
        'sale_price_jpy': employee.sale_price_jpy,
        'visa_status': employee.visa_status,
        'application_date': employee.application_date,
        'expired_coe_date': employee.expired_coe_date,
        'created_at': employee.created_at.strftime('%d/%m/%Y %H:%M') if employee.created_at else None,
        'updated_at': employee.updated_at.strftime('%d/%m/%Y %H:%M') if employee.updated_at else None
    }
    
    return jsonify({'success': True, 'employee': employee_data})

def get_all_dropdown_data():
    """Get all dropdown data grouped by category"""
    categories = ['Source', 'Type', 'Change Dept/Lending', 'JP Level', 'EN level',
                 'Special Action type', 'National', 'Current location', 
                 'Expected Working place', 'Job rank', 'Department', 'Child Department']
    
    dropdown_data = {}
    for category in categories:
        items = DropdownData.query.filter_by(category=category, is_active=True).all()
        dropdown_data[category] = [item.value for item in items]
    
    return dropdown_data
