from flask_login import UserMixin
from datetime import datetime
from extensions import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # Admin, RA, MNG, Viewer
    department = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Employee(db.Model):
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(100))
    full_name = db.Column(db.String(200), nullable=False)
    account = db.Column(db.String(100), unique=True, nullable=False)
    department = db.Column(db.String(100))
    child_department = db.Column(db.String(100))
    idle_mm = db.Column(db.Integer)
    type = db.Column(db.String(100))
    idle_from = db.Column(db.Date)
    idle_to = db.Column(db.Date)
    progress_note = db.Column(db.Text)
    ra_pic = db.Column(db.String(100))
    change_dept_lending = db.Column(db.String(100))
    urgent_case = db.Column(db.String(10), default='No')
    hr_manage = db.Column(db.String(10), default='No')
    special_action_type = db.Column(db.String(100))
    skill = db.Column(db.Text)
    experience_it = db.Column(db.Text)
    jp_level = db.Column(db.String(50))
    en_level = db.Column(db.String(100))
    national = db.Column(db.String(100))
    current_location = db.Column(db.String(100))
    expected_working_place = db.Column(db.String(100))
    note_expected_working_place = db.Column(db.Text)
    job_rank = db.Column(db.String(50))
    fjp_join_date = db.Column(db.Date)
    current_dept_comment = db.Column(db.Text)
    interview_comment = db.Column(db.Text)
    performance_che = db.Column(db.Text)
    sale_price_jpy = db.Column(db.Integer)
    visa_status = db.Column(db.String(100))
    application_date = db.Column(db.String(100))
    expired_coe_date = db.Column(db.String(100))
    is_deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Employee {self.full_name}>'

class DropdownData(db.Model):
    __tablename__ = 'dropdown_data'
    
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False)
    value = db.Column(db.String(200), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<DropdownData {self.category}: {self.value}>'

class EmployeeHistory(db.Model):
    __tablename__ = 'employee_history'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    field_name = db.Column(db.String(100), nullable=False)
    old_value = db.Column(db.Text)
    new_value = db.Column(db.Text)
    changed_by = db.Column(db.String(100), nullable=False)
    changed_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    employee = db.relationship('Employee', backref=db.backref('history', lazy=True))
    
    def __repr__(self):
        return f'<EmployeeHistory {self.field_name}: {self.old_value} -> {self.new_value}>'
