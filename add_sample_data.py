"""
Script to add sample employee data for testing the filter functionality
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import Employee
from extensions import db
from datetime import date

def add_sample_employees():
    app = create_app()
    
    with app.app_context():
        # Check if there are already employees
        existing_count = Employee.query.count()
        print(f"Current employees in database: {existing_count}")
        
        if existing_count > 0:
            print("Sample data already exists. Skipping...")
            return
        
        # Sample employees with different types for testing filter
        sample_employees = [
            {
                'source': 'FJPer',
                'full_name': 'Nguyen Van An',
                'account': 'AnNV',
                'type': 'Being Idle',
                'department': 'FJP RA',
                'child_department': 'RA RDC',
                'idle_mm': 3,
                'ra_pic': 'Manager A',
                'jp_level': 'N2',
                'idle_from': date(2024, 8, 1),
                'urgent_case': 'Yes'
            },
            {
                'source': 'FJP-Center',
                'full_name': 'Tran Thi Binh',
                'account': 'BinhTT',
                'type': 'To be Idle',
                'department': 'FJP IT',
                'child_department': 'IT Support',
                'idle_mm': 1,
                'ra_pic': 'Manager B',
                'jp_level': 'N1',
                'idle_from': date(2024, 9, 1),
                'urgent_case': 'No'
            },
            {
                'source': 'BA Program',
                'full_name': 'Le Van Cuong',
                'account': 'CuongLV',
                'type': 'Idle Short Term',
                'department': 'FJP FA',
                'child_department': 'FA G1D',
                'idle_mm': 2,
                'ra_pic': 'Manager C',
                'jp_level': 'N3',
                'idle_from': date(2024, 7, 15),
                'urgent_case': 'Yes'
            },
            {
                'source': 'External',
                'full_name': 'Pham Thi Dung',
                'account': 'DungPT',
                'type': 'Lack BMM',
                'department': 'FJP Sales',
                'child_department': 'Sales Team',
                'idle_mm': 0,
                'ra_pic': 'Manager D',
                'jp_level': 'No JP',
                'idle_from': date(2024, 8, 20),
                'urgent_case': 'No'
            },
            {
                'source': 'XPM Program',
                'full_name': 'Hoang Van Em',
                'account': 'EmHV',
                'type': 'Fix Customer',
                'department': 'FJP HR',
                'child_department': 'HR Admin',
                'idle_mm': 1,
                'ra_pic': 'Manager E',
                'jp_level': 'N2-',
                'idle_from': date(2024, 8, 10),
                'urgent_case': 'No'
            }
        ]
        
        for emp_data in sample_employees:
            employee = Employee(**emp_data)
            db.session.add(employee)
        
        db.session.commit()
        print(f"Added {len(sample_employees)} sample employees successfully!")
        
        # Print summary
        for emp in Employee.query.all():
            print(f"- {emp.full_name} ({emp.account}): {emp.type}")

if __name__ == '__main__':
    add_sample_employees()
