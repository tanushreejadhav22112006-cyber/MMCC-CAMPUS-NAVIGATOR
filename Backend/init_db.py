"""
Database initialization script for Campus Navigator
Creates tables and seeds initial data including admin user
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db, User, Location
from dotenv import load_dotenv

load_dotenv()


def init_db():
    """Initialize database with tables and seed data"""
    app = create_app()
    
    with app.app_context():
        # Create all tables
        print("Creating database tables...")
        print(f"Database: navigator")
        db.create_all()
        print("Database tables created successfully!")
        
        # Check if admin user exists
        admin = User.query.filter_by(user_type='admin').first()
        
        if not admin:
            # Create default admin user
            print("Creating default admin user...")
            admin_user = User(
                name='Admin User',
                email='admin@campus.edu',
                user_type='admin'
            )
            admin_user.set_password('admin123')
            
            db.session.add(admin_user)
            db.session.commit()
            print("Default admin user created!")
            print("  Email: admin@campus.edu")
            print("  Password: admin123")
            print("  ⚠️  Please change the password after first login!")
        else:
            print("Admin user already exists.")
        
        # Seed sample locations
        seed_locations()

        # Seed sample users
        seed_sample_users()

        print("\nDatabase initialization complete!")


def seed_locations():
    """Seed MMCC Pune campus locations"""
    # Check if locations already exist
    if Location.query.count() > 0:
        print("Locations already seeded.")
        return

    print("Seeding MMCC Pune campus locations...")

    sample_locations = [
        # Buildings (3)
        Location(
            name='Commerce Building',
            description='Commerce department building with classrooms for B.Com, BBA, and M.Com courses at MMCC Pune',
            location_type='building',
            floor='Ground - 2nd Floor',
            building='Block A',
            latitude=18.52043000,
            longitude=73.85674000
        ),
        Location(
            name='Science & Commerce Block',
            description='Science and Commerce department building with laboratories and lecture halls at MMCC Pune',
            location_type='building',
            floor='Ground - 3rd Floor',
            building='Block B',
            latitude=18.52050000,
            longitude=73.85680000
        ),
        Location(
            name='Architecture Block',
            description='Architecture department building with design studios and drafting rooms at MMCC Pune',
            location_type='building',
            floor='Ground - 4th Floor',
            building='Block C',
            latitude=18.52060000,
            longitude=73.85690000
        ),
        
        # Laboratories (11)
        Location(
            name='Computer Science Laboratory',
            description='Modern computer lab with 50+ systems for programming and practical sessions',
            location_type='lab',
            floor='2nd Floor',
            building='Block A',
            latitude=18.52045000,
            longitude=73.85676000
        ),
        Location(
            name='Physics Laboratory',
            description='Well-equipped physics lab for undergraduate practical experiments',
            location_type='lab',
            floor='1st Floor',
            building='Block B',
            latitude=18.52052000,
            longitude=73.85682000
        ),
        Location(
            name='Chemistry Laboratory',
            description='Fully furnished chemistry lab with modern equipment for practical sessions',
            location_type='lab',
            floor='1st Floor',
            building='Block B',
            latitude=18.52053000,
            longitude=73.85683000
        ),
        Location(
            name='Language Laboratory',
            description='Audio-visual language lab for communication skills development',
            location_type='lab',
            floor='Ground Floor',
            building='Block A',
            latitude=18.52044000,
            longitude=73.85675000
        ),
        Location(
            name='Computer Application Laboratory',
            description='Advanced computer application lab with latest software for BCA and MCA students',
            location_type='lab',
            floor='2nd Floor',
            building='Block B',
            latitude=18.52054000,
            longitude=73.85684000
        ),
        Location(
            name='NASSCOM Laboratory',
            description='Industry-sponsored lab for IT training and certification programs',
            location_type='lab',
            floor='3rd Floor',
            building='Block B',
            latitude=18.52055000,
            longitude=73.85685000
        ),
        Location(
            name='Statistics Laboratory',
            description='Computer-aided statistics lab with statistical software and data analysis tools',
            location_type='lab',
            floor='2nd Floor',
            building='Block A',
            latitude=18.52046000,
            longitude=73.85677000
        ),
        Location(
            name='NASA Laboratory',
            description='Specialized research lab for astronomy and space science studies',
            location_type='lab',
            floor='3rd Floor',
            building='Block C',
            latitude=18.52062000,
            longitude=73.85692000
        ),
        Location(
            name='ALPHA Laboratory',
            description='Advanced learning and programming hub for automation and software development',
            location_type='lab',
            floor='1st Floor',
            building='Block C',
            latitude=18.52061000,
            longitude=73.85691000
        ),
        Location(
            name='Electronics Laboratory',
            description='Electronics and embedded systems lab with circuit design and testing equipment',
            location_type='lab',
            floor='2nd Floor',
            building='Block B',
            latitude=18.52056000,
            longitude=73.85686000
        ),
        Location(
            name='Statistics Lab',
            description='Dedicated statistics lab for data analysis and research with modern computational tools',
            location_type='lab',
            floor='1st Floor',
            building='Block A',
            latitude=18.52047000,
            longitude=73.85678000
        ),
        
        # Classrooms (43)
        Location(name='Classroom 1', description='Standard classroom with 60 seating capacity', location_type='classroom', floor='Ground Floor', building='Block A', latitude=18.52041000, longitude=73.85673000),
        Location(name='Classroom 2', description='Standard classroom with 60 seating capacity', location_type='classroom', floor='Ground Floor', building='Block A', latitude=18.52042000, longitude=73.85674000),
        Location(name='Classroom 3', description='Standard classroom with 60 seating capacity', location_type='classroom', floor='Ground Floor', building='Block A', latitude=18.52043000, longitude=73.85675000),
        Location(name='Classroom 4', description='Standard classroom with 60 seating capacity', location_type='classroom', floor='Ground Floor', building='Block A', latitude=18.52044000, longitude=73.85676000),
        Location(name='Classroom 5', description='Standard classroom with 60 seating capacity', location_type='classroom', floor='Ground Floor', building='Block A', latitude=18.52045000, longitude=73.85677000),
        Location(name='Classroom 6', description='Standard classroom with 60 seating capacity', location_type='classroom', floor='1st Floor', building='Block A', latitude=18.52041000, longitude=73.85673000),
        Location(name='Classroom 7', description='Standard classroom with 60 seating capacity', location_type='classroom', floor='1st Floor', building='Block A', latitude=18.52042000, longitude=73.85674000),
        Location(name='Classroom 8', description='Standard classroom with 60 seating capacity', location_type='classroom', floor='1st Floor', building='Block A', latitude=18.52043000, longitude=73.85675000),
        Location(name='Classroom 9', description='Standard classroom with 60 seating capacity', location_type='classroom', floor='1st Floor', building='Block A', latitude=18.52044000, longitude=73.85676000),
        Location(name='Classroom 10', description='Standard classroom with 60 seating capacity', location_type='classroom', floor='1st Floor', building='Block A', latitude=18.52045000, longitude=73.85677000),
        Location(name='Classroom 11', description='Standard classroom with 60 seating capacity', location_type='classroom', floor='2nd Floor', building='Block A', latitude=18.52041000, longitude=73.85673000),
        Location(name='Classroom 14', description='Standard classroom with 60 seating capacity', location_type='classroom', floor='2nd Floor', building='Block A', latitude=18.52042000, longitude=73.85674000),
        Location(name='Classroom 15', description='Standard classroom with 60 seating capacity', location_type='classroom', floor='2nd Floor', building='Block A', latitude=18.52043000, longitude=73.85675000),
        Location(name='Classroom 101', description='Standard classroom with 60 seating capacity', location_type='classroom', floor='Ground Floor', building='Block A', latitude=18.52041000, longitude=73.85673000),
        Location(name='Classroom 102', description='Standard classroom with 60 seating capacity', location_type='classroom', floor='Ground Floor', building='Block A', latitude=18.52042000, longitude=73.85674000),
        Location(name='Classroom 103', description='Standard classroom with 60 seating capacity', location_type='classroom', floor='Ground Floor', building='Block A', latitude=18.52043000, longitude=73.85675000),
        Location(name='Classroom 104', description='Standard classroom with 60 seating capacity', location_type='classroom', floor='Ground Floor', building='Block A', latitude=18.52044000, longitude=73.85676000),
        Location(name='Classroom 105', description='Standard classroom with 60 seating capacity', location_type='classroom', floor='Ground Floor', building='Block A', latitude=18.52045000, longitude=73.85677000),
        Location(name='Classroom 201', description='Standard classroom with 60 seating capacity', location_type='classroom', floor='1st Floor', building='Block A', latitude=18.52041000, longitude=73.85673000),
        Location(name='Classroom 202', description='Standard classroom with 60 seating capacity', location_type='classroom', floor='1st Floor', building='Block A', latitude=18.52042000, longitude=73.85674000),
        Location(name='Classroom 203', description='Standard classroom with 60 seating capacity', location_type='classroom', floor='1st Floor', building='Block A', latitude=18.52043000, longitude=73.85675000),
        Location(name='Classroom 204', description='Standard classroom with 60 seating capacity', location_type='classroom', floor='1st Floor', building='Block A', latitude=18.52044000, longitude=73.85676000),
        Location(name='Classroom 205', description='Standard classroom with 60 seating capacity', location_type='classroom', floor='1st Floor', building='Block A', latitude=18.52045000, longitude=73.85677000),
        Location(name='Classroom 301', description='Standard classroom with 60 seating capacity', location_type='classroom', floor='2nd Floor', building='Block A', latitude=18.52041000, longitude=73.85673000),
        Location(name='Classroom 302', description='Standard classroom with 60 seating capacity', location_type='classroom', floor='2nd Floor', building='Block A', latitude=18.52042000, longitude=73.85674000),
        Location(name='Classroom 303', description='Standard classroom with 60 seating capacity', location_type='classroom', floor='2nd Floor', building='Block A', latitude=18.52043000, longitude=73.85675000),
        Location(name='Classroom 304', description='Standard classroom with 60 seating capacity', location_type='classroom', floor='2nd Floor', building='Block A', latitude=18.52044000, longitude=73.85676000),
        Location(name='Classroom 305', description='Standard classroom with 60 seating capacity', location_type='classroom', floor='2nd Floor', building='Block A', latitude=18.52045000, longitude=73.85677000),
        Location(name='Classroom 401', description='Standard classroom with 60 seating capacity', location_type='classroom', floor='Ground Floor', building='Block B', latitude=18.52051000, longitude=73.85681000),
        Location(name='Classroom 402', description='Standard classroom with 60 seating capacity', location_type='classroom', floor='Ground Floor', building='Block B', latitude=18.52052000, longitude=73.85682000),
        Location(name='Classroom 403', description='Standard classroom with 60 seating capacity', location_type='classroom', floor='Ground Floor', building='Block B', latitude=18.52053000, longitude=73.85683000),
        Location(name='Classroom 404', description='Standard classroom with 60 seating capacity', location_type='classroom', floor='Ground Floor', building='Block B', latitude=18.52054000, longitude=73.85684000),
        Location(name='Classroom 405', description='Standard classroom with 60 seating capacity', location_type='classroom', floor='Ground Floor', building='Block B', latitude=18.52055000, longitude=73.85685000),
        Location(name='Classroom 501', description='Standard classroom with 60 seating capacity', location_type='classroom', floor='1st Floor', building='Block B', latitude=18.52051000, longitude=73.85681000),
        Location(name='Classroom 502', description='Standard classroom with 60 seating capacity', location_type='classroom', floor='1st Floor', building='Block B', latitude=18.52052000, longitude=73.85682000),
        Location(name='Classroom 503', description='Standard classroom with 60 seating capacity', location_type='classroom', floor='1st Floor', building='Block B', latitude=18.52053000, longitude=73.85683000),
        Location(name='Classroom 504', description='Standard classroom with 60 seating capacity', location_type='classroom', floor='1st Floor', building='Block B', latitude=18.52054000, longitude=73.85684000),
        Location(name='Classroom 505', description='Standard classroom with 60 seating capacity', location_type='classroom', floor='1st Floor', building='Block B', latitude=18.52055000, longitude=73.85685000),
        Location(name='Classroom 601', description='Standard classroom with 60 seating capacity', location_type='classroom', floor='2nd Floor', building='Block B', latitude=18.52051000, longitude=73.85681000),
        Location(name='Classroom 602', description='Standard classroom with 60 seating capacity', location_type='classroom', floor='2nd Floor', building='Block B', latitude=18.52052000, longitude=73.85682000),
        Location(name='Classroom 603', description='Standard classroom with 60 seating capacity', location_type='classroom', floor='2nd Floor', building='Block B', latitude=18.52053000, longitude=73.85683000),
        Location(name='Seminar Hall A', description='Large seminar hall with 100 seating capacity for events', location_type='classroom', floor='3rd Floor', building='Block B', latitude=18.52054000, longitude=73.85684000),
        Location(name='Conference Room', description='Conference room for meetings and presentations', location_type='classroom', floor='3rd Floor', building='Block B', latitude=18.52055000, longitude=73.85685000)
    ]

    for location in sample_locations:
        db.session.add(location)

    db.session.commit()
    print(f"Seeded {len(sample_locations)} MMCC Pune locations (3 Buildings, 11 Labs, 43 Classrooms).")


def seed_sample_users():
    """Seed sample users of different types for testing"""
    # Check if there are already non-admin users
    existing_users = User.query.filter(User.user_type != 'admin').count()
    
    # Only skip if we already have 10+ sample users (not counting the one we might have created during testing)
    if existing_users >= 10:
        print(f"Sample users already exist ({existing_users} users).")
        return

    print(f"Seeding sample users (existing non-admin users: {existing_users})...")

    sample_users = [
        # Students
        {'name': 'Rahul Sharma', 'email': 'student1@mmcc.edu', 'user_type': 'student'},
        {'name': 'Priya Patel', 'email': 'student2@mmcc.edu', 'user_type': 'student'},
        {'name': 'Amit Kumar', 'email': 'student3@mmcc.edu', 'user_type': 'student'},
        {'name': 'Sneha Desai', 'email': 'student4@mmcc.edu', 'user_type': 'student'},
        {'name': 'Vikram Singh', 'email': 'student5@mmcc.edu', 'user_type': 'student'},
        
        # Faculty
        {'name': 'Dr. Suresh Menon', 'email': 'faculty1@mmcc.edu', 'user_type': 'faculty'},
        {'name': 'Prof. Anita Rao', 'email': 'faculty2@mmcc.edu', 'user_type': 'faculty'},
        {'name': 'Prof. Rajesh Gupta', 'email': 'faculty3@mmcc.edu', 'user_type': 'faculty'},
        {'name': 'Dr. Meera Iyer', 'email': 'faculty4@mmcc.edu', 'user_type': 'faculty'},
        
        # Visitors
        {'name': 'Guest User 1', 'email': 'visitor1@guest.com', 'user_type': 'visitor'},
        {'name': 'Guest User 2', 'email': 'visitor2@guest.com', 'user_type': 'visitor'},
        {'name': 'Guest User 3', 'email': 'visitor3@guest.com', 'user_type': 'visitor'},
    ]

    for user_data in sample_users:
        # Check if user already exists
        existing = User.query.filter_by(email=user_data['email']).first()
        if not existing:
            user = User(
                name=user_data['name'],
                email=user_data['email'],
                user_type=user_data['user_type']
            )
            user.set_password('password123')  # Default password for all sample users
            db.session.add(user)
            db.session.flush()  # Flush to get user ID before adding login history
            
            # Add some login history for realistic data
            from models import LoginHistory
            from datetime import datetime, timedelta, timezone
            import random
            
            # Add 1-5 login records per user
            login_count = random.randint(1, 5)
            for i in range(login_count):
                login_date = datetime.now(timezone.utc) - timedelta(days=random.randint(0, 30))
                login = LoginHistory(
                    user_id=user.id,
                    login_at=login_date,
                    ip_address=f'192.168.1.{random.randint(1, 254)}'
                )
                db.session.add(login)

    db.session.commit()
    total_users = User.query.count()
    print(f"Seeded {len(sample_users)} sample users (5 students, 4 faculty, 3 visitors)")
    print(f"  Total users in database: {total_users}")
    print("  Default password for all users: password123")


if __name__ == '__main__':
    init_db()
