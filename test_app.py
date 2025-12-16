import unittest
from app import app, db, Parent, Child, Activity, Booking
from datetime import datetime, date
import tempfile
import os
import time
import sys

class ColoredTestResult(unittest.TextTestResult):
    """Custom test result class with colored output and delays"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_count = 0
        self.success_count = 0
    
    def startTest(self, test):
        super().startTest(test)
        self.test_count += 1
        test_name = str(test).split()[0]
        print("\n" + "="*70)
        print("🧪 TEST #{}: {}".format(self.test_count, test_name))
        print("="*70)
        time.sleep(0.3)
    
    def addSuccess(self, test):
        super().addSuccess(test)
        self.success_count += 1
        print("✅ TEST PASSED: {}".format(str(test).split()[0]))
        time.sleep(0.5)
    
    def addError(self, test, err):
        super().addError(test, err)
        print("❌ TEST ERROR: {}".format(str(test).split()[0]))
        time.sleep(0.5)
    
    def addFailure(self, test, err):
        super().addFailure(test, err)
        print("❌ TEST FAILED: {}".format(str(test).split()[0]))
        time.sleep(0.5)
    
    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        print("⏭️ TEST SKIPPED: {} - {}".format(str(test).split()[0], reason))
        time.sleep(0.5)

class ColoredTestRunner(unittest.TextTestRunner):
    """Custom test runner with colored output"""
    resultclass = ColoredTestResult
    
    def run(self, test):
        print("\n" + "="*70)
        print("🚀 SCHOOL ACTIVITY BOOKING SYSTEM - TEST SUITE")
        print("="*70)
        result = super().run(test)
        
        # Print summary
        print("\n" + "="*70)
        print("📊 TEST SUMMARY")
        print("="*70)
        print(f"Total Tests Run: {result.testsRun}")
        print(f"✅ Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
        print(f"❌ Failed: {len(result.failures)}")
        print(f"⚠️  Errors: {len(result.errors)}")
        print(f"⏭️  Skipped: {len(result.skipped)}")
        print("="*70)
        
        if result.wasSuccessful():
            print("🎉 ALL TESTS PASSED! System is ready for deployment.\n")
        else:
            print("⚠️  Some tests failed. Please review the errors above.\n")
        
        time.sleep(0.5)
        return result

class SchoolBookingSystemTestCase(unittest.TestCase):
    """Test suite for School Activity Booking System"""

    def setUp(self):
        """Set up test client and database"""
        self.db_fd, self.db_path = tempfile.mkstemp()
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{self.db_path}'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_ECHO'] = False
        
        self.app = app
        self.client = app.test_client()
        
        with app.app_context():
            db.create_all()
            self._seed_database()

    def tearDown(self):
        """Clean up test database"""
        with app.app_context():
            db.session.remove()
            db.drop_all()
        os.close(self.db_fd)
        os.unlink(self.db_path)

    def _seed_database(self):
        """Seed test database with sample data"""
        # Create parent
        parent = Parent(email='testparent@example.com', full_name='Test Parent', phone='1234567890')
        parent.set_password('password123')
        db.session.add(parent)
        db.session.flush()
        
        # Create child
        child = Child(parent_id=parent.id, name='Test Child', age=10, grade='5th')
        db.session.add(child)
        db.session.flush()
        
        # Create activities
        activity = Activity(
            name='Soccer',
            description='Soccer Training',
            price=20.0,
            max_capacity=15,
            day_of_week='Monday',
            start_time='15:00',
            end_time='16:30'
        )
        db.session.add(activity)
        db.session.commit()

    # ==================== Authentication Tests ====================
    
    def test_parent_registration(self):
        """Test parent registration"""
        response = self.client.post('/register', data={
            'full_name': 'New Parent',
            'email': 'newparent@example.com',
            'phone': '9876543210',
            'password': 'password123',
            'confirm_password': 'password123'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        
        # Verify parent was created
        with app.app_context():
            parent = Parent.query.filter_by(email='newparent@example.com').first()
            self.assertIsNotNone(parent)
            self.assertEqual(parent.full_name, 'New Parent')

    def test_parent_login(self):
        """Test parent login"""
        response = self.client.post('/login', data={
            'email': 'testparent@example.com',
            'password': 'password123'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)

    def test_invalid_login(self):
        """Test login with wrong credentials"""
        response = self.client.post('/login', data={
            'email': 'testparent@example.com',
            'password': 'wrongpassword'
        })
        
        self.assertIn(b'Invalid email or password', response.data)

    def test_duplicate_email_registration(self):
        """Test registration with duplicate email"""
        response = self.client.post('/register', data={
            'full_name': 'Another Parent',
            'email': 'testparent@example.com',
            'phone': '1111111111',
            'password': 'password123',
            'confirm_password': 'password123'
        })
        
        self.assertIn(b'Email already registered', response.data)

    def test_password_mismatch(self):
        """Test registration with mismatched passwords"""
        response = self.client.post('/register', data={
            'full_name': 'Test Parent 2',
            'email': 'test2@example.com',
            'phone': '1234567890',
            'password': 'password123',
            'confirm_password': 'differentpassword'
        })
        
        self.assertIn(b'Passwords do not match', response.data)

    # ==================== Child Management Tests ====================
    
    def test_add_child(self):
        """Test adding a child"""
        with self.client:
            # Login first
            self.client.post('/login', data={
                'email': 'testparent@example.com',
                'password': 'password123'
            })
            
            response = self.client.post('/add_child', data={
                'name': 'New Child',
                'age': 8,
                'grade': '3rd'
            })
            
            self.assertEqual(response.status_code, 200)

    def test_add_child_without_login(self):
        """Test adding child without authentication"""
        response = self.client.post('/add_child', data={
            'name': 'New Child',
            'age': 8,
            'grade': '3rd'
        }, follow_redirects=True)
        
        # Should redirect to login
        self.assertEqual(response.status_code, 200)

    def test_remove_child(self):
        """Test removing a child"""
        with self.client:
            # Login first
            self.client.post('/login', data={
                'email': 'testparent@example.com',
                'password': 'password123'
            })
            
            with app.app_context():
                parent = Parent.query.filter_by(email='testparent@example.com').first()
                child = parent.children[0]
                child_id = child.id
            
            response = self.client.post(f'/remove_child/{child_id}')
            
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertTrue(data.get('success'))
            
            # Verify child was deleted
            with app.app_context():
                deleted_child = Child.query.get(child_id)
                self.assertIsNone(deleted_child)

    def test_remove_child_cascades_bookings(self):
        """Test that removing a child also removes associated bookings"""
        with self.client:
            self.client.post('/login', data={
                'email': 'testparent@example.com',
                'password': 'password123'
            })
            
            with app.app_context():
                parent = Parent.query.filter_by(email='testparent@example.com').first()
                child = parent.children[0]
                activity = Activity.query.first()
                
                # Create a booking
                booking = Booking(
                    parent_id=parent.id,
                    child_id=child.id,
                    activity_id=activity.id,
                    booking_date=date(2025, 12, 15),
                    cost=20.0
                )
                db.session.add(booking)
                db.session.commit()
                booking_id = booking.id
                child_id = child.id
            
            # Remove the child
            response = self.client.post(f'/remove_child/{child_id}')
            
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertTrue(data.get('success'))
            
            # Verify booking was deleted
            with app.app_context():
                deleted_booking = Booking.query.get(booking_id)
                self.assertIsNone(deleted_booking)

    # ==================== Booking Tests ====================
    
    def test_book_activity(self):
        """Test booking an activity"""
        with self.client:
            # Login
            self.client.post('/login', data={
                'email': 'testparent@example.com',
                'password': 'password123'
            })
            
            # Get IDs
            with app.app_context():
                parent = Parent.query.filter_by(email='testparent@example.com').first()
                child = parent.children[0]
                activity = Activity.query.first()
            
            response = self.client.post('/book_activity', data={
                'child_id': child.id,
                'activity_id': activity.id,
                'booking_date': '2025-12-15'
            })
            
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertTrue(data.get('success'))

    def test_prevent_double_booking(self):
        """Test prevention of double bookings on same day"""
        with self.client:
            # Login
            self.client.post('/login', data={
                'email': 'testparent@example.com',
                'password': 'password123'
            })
            
            with app.app_context():
                parent = Parent.query.filter_by(email='testparent@example.com').first()
                child = parent.children[0]
                activity = Activity.query.first()
            
            # First booking
            self.client.post('/book_activity', data={
                'child_id': child.id,
                'activity_id': activity.id,
                'booking_date': '2025-12-15'
            })
            
            # Try second booking same day
            response = self.client.post('/book_activity', data={
                'child_id': child.id,
                'activity_id': activity.id,
                'booking_date': '2025-12-15'
            })
            
            data = response.get_json()
            self.assertFalse(data.get('success'))
            self.assertIn('already has a booking', data.get('error'))

    def test_booking_with_invalid_child(self):
        """Test booking with invalid child ID"""
        with self.client:
            self.client.post('/login', data={
                'email': 'testparent@example.com',
                'password': 'password123'
            })
            
            with app.app_context():
                activity = Activity.query.first()
            
            response = self.client.post('/book_activity', data={
                'child_id': 9999,
                'activity_id': activity.id,
                'booking_date': '2025-12-15'
            })
            
            self.assertEqual(response.status_code, 400)

    def test_cancel_booking(self):
        """Test canceling a booking"""
        with self.client:
            self.client.post('/login', data={
                'email': 'testparent@example.com',
                'password': 'password123'
            })
            
            with app.app_context():
                parent = Parent.query.filter_by(email='testparent@example.com').first()
                child = parent.children[0]
                activity = Activity.query.first()
                
                # Create booking
                booking = Booking(
                    parent_id=parent.id,
                    child_id=child.id,
                    activity_id=activity.id,
                    booking_date=date(2025, 12, 15),
                    cost=20.0
                )
                db.session.add(booking)
                db.session.commit()
                booking_id = booking.id
            
            response = self.client.post(f'/cancel_booking/{booking_id}')
            
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertTrue(data.get('success'))

    # ==================== Database Tests ====================
    
    def test_parent_model(self):
        """Test Parent model"""
        with app.app_context():
            parent = Parent.query.filter_by(email='testparent@example.com').first()
            self.assertIsNotNone(parent)
            self.assertTrue(parent.check_password('password123'))
            self.assertFalse(parent.check_password('wrongpassword'))

    def test_child_model(self):
        """Test Child model"""
        with app.app_context():
            parent = Parent.query.filter_by(email='testparent@example.com').first()
            child = parent.children[0]
            self.assertEqual(child.name, 'Test Child')
            self.assertEqual(child.age, 10)

    def test_activity_model(self):
        """Test Activity model"""
        with app.app_context():
            activity = Activity.query.filter_by(name='Soccer').first()
            self.assertIsNotNone(activity)
            self.assertEqual(activity.price, 20.0)
            self.assertEqual(activity.day_of_week, 'Monday')

    def test_booking_model(self):
        """Test Booking model"""
        with app.app_context():
            parent = Parent.query.filter_by(email='testparent@example.com').first()
            child = parent.children[0]
            activity = Activity.query.first()
            
            booking = Booking(
                parent_id=parent.id,
                child_id=child.id,
                activity_id=activity.id,
                booking_date=date(2025, 12, 15),
                cost=20.0
            )
            db.session.add(booking)
            db.session.commit()
            
            retrieved_booking = Booking.query.filter_by(id=booking.id).first()
            self.assertIsNotNone(retrieved_booking)
            self.assertEqual(retrieved_booking.status, 'confirmed')

    # ==================== View Tests ====================
    
    def test_index_page(self):
        """Test index page loads"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Greenwood International', response.data)

    def test_dashboard_requires_login(self):
        """Test dashboard requires authentication"""
        response = self.client.get('/dashboard', follow_redirects=True)
        self.assertIn(b'Login', response.data)

    def test_dashboard_loads_for_authenticated_user(self):
        """Test dashboard loads for authenticated user"""
        with self.client:
            self.client.post('/login', data={
                'email': 'testparent@example.com',
                'password': 'password123'
            })
            
            response = self.client.get('/dashboard')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Welcome', response.data)

    # ==================== API Tests ====================
    
    def test_api_activities(self):
        """Test activities API"""
        response = self.client.get('/api/activities')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(len(data) > 0)
        self.assertIn('name', data[0])
        self.assertIn('price', data[0])

    def test_check_availability(self):
        """Test availability checking"""
        with app.app_context():
            activity = Activity.query.first()
        
        response = self.client.post('/api/check_availability', json={
            'activity_id': activity.id,
            'booking_date': '2025-12-15'
        })
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('available', data)
        self.assertIn('spots_left', data)


if __name__ == '__main__':
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(SchoolBookingSystemTestCase)
    runner = ColoredTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
