"""
Script to initialize sample employee data for testing
Run this after the application starts to add sample data
"""
from app import create_app
from models import Employee, User, DropdownData, EmployeeHistory
from extensions import db
from datetime import datetime, date
from werkzeug.security import generate_password_hash

def init_sample_data():
    app = create_app()
    
    with app.app_context():
        # Create sample employees based on the data in main.md
        sample_employees = [
            {
                'source': 'FJPer',
                'full_name': 'Nguyen Van An',
                'account': 'AnNV',
                'department': 'FJP RA',
                'child_department': 'RA RDC',
                'idle_mm': 1,
                'type': 'To be Idle',
                'idle_from': date(2024, 5, 9),
                'idle_to': None,
                'progress_note': '[9-May] Join opp from 12-May to 15-Sep',
                'ra_pic': 'HuongNTT6',
                'change_dept_lending': 'Change Dept or Lending',
                'urgent_case': 'No',
                'hr_manage': 'No',
                'special_action_type': None,
                'skill': 'BrSE, test',
                'experience_it': '6 năm',
                'jp_level': 'N2-',
                'en_level': 'Elementary/Pre-intermediate (TOEIC 400-600)',
                'national': 'Japanese',
                'current_location': 'Tokyo',
                'expected_working_place': 'Tokyo',
                'note_expected_working_place': None,
                'job_rank': 'DEVE02',
                'fjp_join_date': date(2018, 6, 15),
                'current_dept_comment': None,
                'interview_comment': '[14-Jul] … [7-Jul]…',
                'performance_che': None,
                'sale_price_jpy': 120,
                'visa_status': None,
                'application_date': None,
                'expired_coe_date': None
            },
            {
                'source': 'BA Program',
                'full_name': 'Nguyen Thi Be',
                'account': 'BeNT',
                'department': 'FJP FA',
                'child_department': 'FA G1D',
                'idle_mm': 1,
                'type': 'To be Idle',
                'idle_from': date(2024, 4, 23),
                'idle_to': None,
                'progress_note': '[6-Jun] Secom GMG Reject Failed CV, Failed interview',
                'ra_pic': 'HuongNTT6',
                'change_dept_lending': 'Not Yet Open',
                'urgent_case': 'Yes',
                'hr_manage': 'Yes',
                'special_action_type': 'MO',
                'skill': 'Java, C#, PHP, XML、HTML, Python',
                'experience_it': '日本で勤務年数: 6年',
                'jp_level': 'N2',
                'en_level': 'Intermediate (TOEIC 600-780)',
                'national': 'Vietnamese',
                'current_location': 'Việt Nam',
                'expected_working_place': 'Tokyo',
                'note_expected_working_place': 'Ibaraki cũng được',
                'job_rank': 'DEVE03',
                'fjp_join_date': date(2019, 1, 20),
                'current_dept_comment': None,
                'interview_comment': None,
                'performance_che': None,
                'sale_price_jpy': 85,
                'visa_status': None,
                'application_date': None,
                'expired_coe_date': None
            },
            {
                'source': 'XPM Program',
                'full_name': 'Tran Van Cuong',
                'account': 'CuongTV',
                'department': 'FJP IT',
                'child_department': 'IT Support',
                'idle_mm': 3,
                'type': 'Being Idle',
                'idle_from': date(2024, 2, 1),
                'idle_to': None,
                'progress_note': 'Đang tìm kiếm dự án phù hợp',
                'ra_pic': 'MinhNQ',
                'change_dept_lending': 'Find Opp',
                'urgent_case': 'Yes',
                'hr_manage': 'No',
                'special_action_type': 'Find Opp',
                'skill': 'React, Node.js, MongoDB, AWS',
                'experience_it': '4 năm fullstack development',
                'jp_level': 'N3',
                'en_level': 'Upper-intermediate/Advanced (TOEIC 780 up)',
                'national': 'Vietnamese',
                'current_location': 'Tokyo',
                'expected_working_place': 'Tokyo',
                'note_expected_working_place': 'Remote work preferred',
                'job_rank': 'FSEN02',
                'fjp_join_date': date(2020, 3, 15),
                'current_dept_comment': 'Kỹ năng tốt, cần dự án thử thách',
                'interview_comment': 'Phỏng vấn tốt, communication skills cần cải thiện',
                'performance_che': 'Good performer',
                'sale_price_jpy': 95,
                'visa_status': 'Working Visa',
                'application_date': '2024-01-15',
                'expired_coe_date': '2025-03-15'
            }
        ]
        
        # Create sample users with different roles
        sample_users = [
            {
                'username': 'ra_user',
                'password': 'ra123',
                'role': 'RA',
                'department': 'FJP RA'
            },
            {
                'username': 'manager_user',
                'password': 'manager123',
                'role': 'MNG',
                'department': 'FJP IT'
            },
            {
                'username': 'viewer_user',
                'password': 'viewer123',
                'role': 'Viewer',
                'department': 'FJP FA'
            }
        ]
        
        # Add sample users
        for user_data in sample_users:
            existing_user = User.query.filter_by(username=user_data['username']).first()
            if not existing_user:
                user = User(
                    username=user_data['username'],
                    password_hash=generate_password_hash(user_data['password']),
                    role=user_data['role'],
                    department=user_data['department'],
                    is_active=True
                )
                db.session.add(user)
        
        # Add sample employees
        for emp_data in sample_employees:
            existing_emp = Employee.query.filter_by(account=emp_data['account']).first()
            if not existing_emp:
                employee = Employee(**emp_data)
                db.session.add(employee)
        
        db.session.commit()
        print("Sample data initialized successfully!")
        print("\nSample user accounts:")
        print("RA User: ra_user / ra123")
        print("Manager User: manager_user / manager123") 
        print("Viewer User: viewer_user / viewer123")
        print("Admin User: admin / admin123")

if __name__ == '__main__':
    init_sample_data()
