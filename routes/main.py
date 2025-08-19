from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from models import Employee, User
from extensions import db
from sqlalchemy import func

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required
def dashboard():
    # Thống kê tổng quan
    total_employees = Employee.query.filter_by(is_deleted=False).count()
    
    # Thống kê theo trạng thái
    status_stats = db.session.query(
        Employee.type,
        func.count(Employee.id)
    ).filter_by(is_deleted=False).group_by(Employee.type).all()
    
    # Thống kê theo bộ phận
    dept_stats = db.session.query(
        Employee.department,
        func.count(Employee.id)
    ).filter_by(is_deleted=False).group_by(Employee.department).all()
    
    # Thống kê urgent cases
    urgent_cases = Employee.query.filter_by(urgent_case='Yes', is_deleted=False).count()
    
    return render_template('dashboard.html', 
                         total_employees=total_employees,
                         status_stats=status_stats,
                         dept_stats=dept_stats,
                         urgent_cases=urgent_cases)

@main_bp.route('/report')
@login_required
def report():
    return render_template('report.html')
