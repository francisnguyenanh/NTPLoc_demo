from flask import Flask
from extensions import db, login_manager
import os

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = 'your-secret-key-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///idle_management.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Vui lòng đăng nhập để truy cập trang này.'
    
    # Import models inside app context to avoid circular imports
    with app.app_context():
        from models import User, Employee, DropdownData, EmployeeHistory
        
        # Create tables
        db.create_all()
        
        # Initialize default dropdown data
        init_dropdown_data()
    
    # Register blueprints
    from routes.auth import auth_bp
    from routes.main import main_bp
    from routes.settings import settings_bp
    from routes.idle_management import idle_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)
    app.register_blueprint(settings_bp, url_prefix='/settings')
    app.register_blueprint(idle_bp, url_prefix='/idle')
    
    @login_manager.user_loader
    def load_user(user_id):
        from models import User
        return User.query.get(int(user_id))
    
    return app

def init_dropdown_data():
    """Initialize dropdown data from requirements"""
    from models import DropdownData, User
    from extensions import db
    
    dropdown_data = {
        'Source': ['FJPer', 'FJP-Center', 'BA Program', 'XPM Program', 'External'],
        'Type': ['Being Idle', 'To be Idle', 'Idle Short Term', 'Lack BMM', 'Fix Customer', 'OUT FJP'],
        'Change Dept/Lending': ['Change Dept or Lending', 'Lending Only', 'Not Yet Open', 'Back to offshore', 
                               'Support internal Task', 'Invested', 'Unpaid Leave', 'Paid Leave', 'Training',
                               'Lack allocate for change Org', 'Long term off'],
        'JP Level': ['Native', 'N1', 'N2', 'N2-', 'N3', 'No JP'],
        'EN level': ['Native', 'Upper-intermediate/Advanced (TOEIC 780 up)', 
                    'Intermediate (TOEIC 600-780)', 'Elementary/Pre-intermediate (TOEIC 400-600)',
                    'Trình độ cơ bản (Beginner/Elementary) (TOEIC < 400)'],
        'Special Action type': ['Back to offshore', 'HR Health Check', 'MO', 'Find Opp', 'Fresher Program'],
        'National': ['Japanese', 'Vietnamese', 'Chinese', 'Korean', 'Other'],
        'Current location': ['Tokyo', 'Osaka', 'Nagoya', 'Fukuoka', 'Shizuoka', 'Hokkaido', 
                           'Okinawa', 'Ibaraki', 'Tochigi', 'Gunma', 'Hiroshima', 'Việt Nam', 'Other'],
        'Expected Working place': ['Tokyo', 'Osaka', 'Nagoya', 'Fukuoka', 'Shizuoka', 'Hokkaido',
                                  'Okinawa', 'Ibaraki', 'Tochigi', 'Gunma', 'Hiroshima', 'Việt Nam', 'Other'],
        'Job rank': ['DEVE01', 'DEVE02', 'DEVE03', 'DEVE04', 'DEVE05', 'DEVE06', 'FSEN01', 'FSEN02',
                    'BANE01', 'BANE02', 'TEST01', 'TEST02', 'SALE 01', 'SALE 02', 'HRMG01', 'HRMG02'],
        'Department': ['FJP RA', 'FJP FA', 'FJP IT', 'FJP Sales', 'FJP HR'],
        'Child Department': ['RA RDC', 'FA G1D', 'IT Support', 'Sales Team', 'HR Admin']
    }
    
    for category, values in dropdown_data.items():
        existing_category = DropdownData.query.filter_by(category=category).first()
        if not existing_category:
            for value in values:
                dropdown_item = DropdownData(category=category, value=value)
                db.session.add(dropdown_item)
    
    # Create default admin user
    from werkzeug.security import generate_password_hash
    admin_user = User.query.filter_by(username='admin').first()
    if not admin_user:
        admin = User(
            username='admin',
            password_hash=generate_password_hash('admin123'),
            role='Admin',
            department='Admin',
            is_active=True
        )
        db.session.add(admin)
    
    db.session.commit()

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
