"""
Database update script to set specific user and location counts
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db, User, Location, LoginHistory
from dotenv import load_dotenv

load_dotenv()


def update_database():
    """Update database with specific counts"""
    app = create_app()

    with app.app_context():
        print("=" * 50)
        print("Updating Database with Specific Counts")
        print("=" * 50)

        # ===== UPDATE USERS =====
        print("\n--- Updating Users ---")
        
        # Delete all existing login history first (due to foreign key constraint)
        LoginHistory.query.delete()
        db.session.flush()
        print("Cleared all existing login history")
        
        # Delete all existing users
        User.query.delete()
        db.session.flush()
        print("Cleared all existing users")

        # Create 1 student user (active)
        student = User(
            name='Student User',
            email='student@mmcc.edu',
            user_type='student',
            is_active=True
        )
        student.set_password('password123')
        db.session.add(student)
        db.session.flush()
        
        # Add login history for student (to make them show in total logins)
        from datetime import datetime, timezone
        login = LoginHistory(
            user_id=student.id,
            login_at=datetime.now(timezone.utc),
            ip_address='192.168.1.100'
        )
        db.session.add(login)
        print("Created: 1 Student (active)")

        # Create 1 visitor user (inactive to match active=1)
        visitor = User(
            name='Visitor User',
            email='visitor@guest.com',
            user_type='visitor',
            is_active=False  # Inactive so active_users = 1
        )
        visitor.set_password('password123')
        db.session.add(visitor)
        print("Created: 1 Visitor (inactive)")

        # Create admin user
        admin = User(
            name='Admin User',
            email='admin@mmcc.edu',
            user_type='admin',
            is_active=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        print("Created: 1 Admin (active)")

        db.session.flush()
        print(f"\nUser Stats:")
        print(f"  Total Users: {User.query.count()}")
        print(f"  Active Users: {User.query.filter_by(is_active=True).count()}")
        print(f"  Students: {User.query.filter_by(user_type='student').count()}")
        print(f"  Visitors: {User.query.filter_by(user_type='visitor').count()}")

        # ===== UPDATE LOCATIONS =====
        print("\n--- Updating Locations ---")
        
        # Delete all existing locations
        Location.query.delete()
        db.session.flush()
        print("Cleared all existing locations")

        # Create 2 Buildings
        buildings = [
            Location(
                name='Commerce Building',
                description='Commerce department building with classrooms',
                location_type='building',
                floor='Ground - 2nd Floor',
                building='Block A',
                latitude=18.52043000,
                longitude=73.85674000,
                is_active=True
            ),
            Location(
                name='Architecture Block',
                description='Architecture department building',
                location_type='building',
                floor='Ground - 4th Floor',
                building='Block C',
                latitude=18.52060000,
                longitude=73.85690000,
                is_active=True
            ),
        ]
        for building in buildings:
            db.session.add(building)
        print(f"Created: 2 Buildings")

        # Create 25 Laboratories
        for i in range(1, 26):
            lab = Location(
                name=f'Laboratory {i}',
                description=f'Computer and science laboratory {i}',
                location_type='lab',
                floor=f'{(i % 4) + 1}st Floor' if i % 4 == 1 else f'{(i % 4) + 1}nd Floor' if i % 4 == 2 else f'{(i % 4) + 1}rd Floor' if i % 4 == 3 else f'{(i % 4) + 1}th Floor',
                building=f'Block {chr(65 + (i % 3))}',
                latitude=18.52040000 + (i * 0.00001),
                longitude=73.85670000 + (i * 0.00001),
                is_active=True
            )
            db.session.add(lab)
        print(f"Created: 25 Laboratories")

        # Create 25 Classrooms
        for i in range(1, 26):
            classroom = Location(
                name=f'Classroom {i}',
                description=f'Standard classroom with 60 seating capacity',
                location_type='classroom',
                floor=f'{(i % 4) + 1}st Floor' if i % 4 == 1 else f'{(i % 4) + 1}nd Floor' if i % 4 == 2 else f'{(i % 4) + 1}rd Floor' if i % 4 == 3 else f'{(i % 4) + 1}th Floor',
                building=f'Block {chr(65 + (i % 3))}',
                latitude=18.52050000 + (i * 0.00001),
                longitude=73.85680000 + (i * 0.00001),
                is_active=True
            )
            db.session.add(classroom)
        print(f"Created: 25 Classrooms")

        db.session.commit()
        
        # Print final stats
        print("\n" + "=" * 50)
        print("Final Database Statistics")
        print("=" * 50)
        
        total_users = User.query.count()
        active_users = User.query.filter_by(is_active=True).count()
        student_count = User.query.filter_by(user_type='student').count()
        visitor_count = User.query.filter_by(user_type='visitor').count()
        
        total_locations = Location.query.count()
        building_count = Location.query.filter_by(location_type='building').count()
        lab_count = Location.query.filter_by(location_type='lab').count()
        classroom_count = Location.query.filter_by(location_type='classroom').count()
        
        total_logins = LoginHistory.query.count()

        print(f"\n📊 Users:")
        print(f"  Total Users: {total_users}")
        print(f"  Active Users: {active_users}")
        print(f"  Students: {student_count}")
        print(f"  Visitors: {visitor_count}")
        
        print(f"\n📍 Locations:")
        print(f"  Total Locations: {total_locations}")
        print(f"  Buildings: {building_count}")
        print(f"  Laboratories: {lab_count}")
        print(f"  Classrooms: {classroom_count}")
        
        print(f"\n🔐 Login History:")
        print(f"  Total Logins: {total_logins}")
        
        print("\n" + "=" * 50)
        print("Database update complete!")
        print("=" * 50)
        print("\nLogin credentials:")
        print("  Student: student@mmcc.edu / password123")
        print("  Visitor: visitor@guest.com / password123")


if __name__ == '__main__':
    update_database()
