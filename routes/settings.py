from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from models import User, DropdownData
from extensions import db
import string
import random

settings_bp = Blueprint('settings', __name__)

def generate_password(length=8):
    """Generate random password"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

@settings_bp.route('/')
@login_required
def index():
    if current_user.role != 'Admin':
        flash('Bạn không có quyền truy cập trang này.', 'error')
        return redirect(url_for('main.dashboard'))
    
    users = User.query.all()
    dropdown_categories = db.session.query(DropdownData.category).distinct().all()
    
    return render_template('settings.html', users=users, dropdown_categories=dropdown_categories)

@settings_bp.route('/add_user', methods=['POST'])
@login_required
def add_user():
    if current_user.role != 'Admin':
        return jsonify({'success': False, 'message': 'Không có quyền'}), 403
    
    username = request.form['username']
    role = request.form['role']
    department = request.form['department']
    
    # Check if user exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'success': False, 'message': 'Tên đăng nhập đã tồn tại'}), 400
    
    # Generate password
    password = generate_password()
    
    # Create user
    user = User(
        username=username,
        password_hash=generate_password_hash(password),
        role=role,
        department=department,
        is_active=True
    )
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'success': True, 
        'message': f'Tạo user thành công. Mật khẩu: {password}',
        'password': password
    })

@settings_bp.route('/dropdown_data/<category>')
@login_required
def get_dropdown_data(category):
    if current_user.role != 'Admin':
        return jsonify({'success': False, 'message': 'Không có quyền'}), 403
    
    data = DropdownData.query.filter_by(category=category, is_active=True).all()
    return jsonify({
        'data': [{'id': item.id, 'value': item.value} for item in data]
    })

@settings_bp.route('/add_dropdown_item', methods=['POST'])
@login_required
def add_dropdown_item():
    if current_user.role != 'Admin':
        return jsonify({'success': False, 'message': 'Không có quyền'}), 403
    
    category = request.form['category']
    value = request.form['value']
    
    # Check if item exists
    existing_item = DropdownData.query.filter_by(category=category, value=value).first()
    if existing_item:
        return jsonify({'success': False, 'message': 'Giá trị đã tồn tại'}), 400
    
    item = DropdownData(category=category, value=value)
    db.session.add(item)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Thêm thành công'})

@settings_bp.route('/delete_dropdown_item/<int:item_id>', methods=['POST'])
@login_required
def delete_dropdown_item(item_id):
    if current_user.role != 'Admin':
        return jsonify({'success': False, 'message': 'Không có quyền'}), 403
    
    item = DropdownData.query.get(item_id)
    if item:
        item.is_active = False
        db.session.commit()
        return jsonify({'success': True, 'message': 'Xóa thành công'})
    
    return jsonify({'success': False, 'message': 'Không tìm thấy item'}), 404
