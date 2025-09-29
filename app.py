from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from dotenv import load_dotenv
import os
import json
from datetime import datetime, timedelta
import hashlib
import secrets

load_dotenv()

app = Flask(__name__, template_folder="templates")

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/tech_stack')
def tech_stack():
    return render_template("tech_stack.html")

@app.route('/curriculum')
def curriculum():
    return render_template("curriculum.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/teaching_approach')
def teaching_approach():
    return render_template("teaching_approach.html")

@app.route('/unplugged_activities')
def unplugged_activities():
    return render_template("unplugged_activities.html")

@app.route('/projects')
def projects():
    return render_template("projects.html")

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        # Handle form submission
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        remember_me = request.form.get('rememberMe') == 'on'
        
        print(f"Server-side sign-in attempt: {email}")
        
        if not email or not password:
            return render_template("signin.html", error="Email and password are required")
        
        users = load_users()
        user = None
        
        # Find user by email
        for u in users:
            if u['email'] == email:
                user = u
                break
        
        if not user:
            return render_template("signin.html", error="Invalid email or password")
        
        # Verify password
        if not verify_password(password, user['password_hash'], user['salt']):
            return render_template("signin.html", error="Invalid email or password")
        
        # Set session
        session['authenticated'] = True
        session['user_id'] = user['id']
        session['parent_name'] = user['parent_name']
        session['email'] = user['email']
        
        # Check if user is admin
        if user.get('role') == 'admin':
            session['role'] = 'admin'
            print(f"Admin signed in: {user['email']}")
            return redirect(url_for('admin_dashboard'))
        
        if remember_me:
            session.permanent = True
        
        print(f"Server-side session set: {dict(session)}")
        
        # Redirect to parent dashboard
        return redirect(url_for('parent_dashboard'))
    
    return render_template("signin.html")

@app.route('/test-signin')
def test_signin():
    return app.send_static_file('test_signin.html')

@app.route('/test-session')
def test_session():
    """Test route to check session status"""
    return jsonify({
        'session_data': dict(session),
        'authenticated': session.get('authenticated', False),
        'user_id': session.get('user_id'),
        'parent_name': session.get('parent_name'),
        'email': session.get('email')
    })

@app.route('/test-session-page')
def test_session_page():
    """Test page to check session functionality"""
    return app.send_static_file('test_session.html')

@app.route('/parent-dashboard')
def parent_dashboard():
    # Check if user is authenticated
    print(f"Parent dashboard access attempt. Session data: {dict(session)}")
    print(f"Authenticated status: {session.get('authenticated')}")
    
    if not session.get('authenticated'):
        print("User not authenticated, redirecting to sign-in")
        return redirect(url_for('signin'))
    
    print("User authenticated, rendering dashboard")
    return render_template("parent_dashboard.html")

@app.route('/api/signup', methods=['POST'])
def signup():
    try:
        # Get form data
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['parentName', 'parentEmail', 'parentPhone', 'parentRelation', 
                          'childName', 'childAge', 'experienceLevel', 'schedulePreference']
        
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Create registration record
        registration = {
            'id': f"REG_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'timestamp': datetime.now().isoformat(),
            'parent_info': {
                'name': data['parentName'],
                'email': data['parentEmail'],
                'phone': data['parentPhone'],
                'relation': data['parentRelation']
            },
            'child_info': {
                'name': data['childName'],
                'age': data['childAge'],
                'grade': data.get('childGrade', ''),
                'experience_level': data['experienceLevel']
            },
            'preferences': {
                'learning_goals': data.get('learningGoals', []),
                'schedule_preference': data['schedulePreference'],
                'session_length': data.get('sessionLength', ''),
                'additional_info': data.get('additionalInfo', ''),
                'newsletter': data.get('newsletter', False)
            },
            'status': 'pending'
        }
        
        # In a real application, you would save this to a database
        # For now, we'll just log it or save to a file
        print(f"New registration: {json.dumps(registration, indent=2)}")
        
        # Save to file (for demo purposes)
        registrations_file = 'registrations.json'
        try:
            with open(registrations_file, 'r') as f:
                registrations = json.load(f)
        except FileNotFoundError:
            registrations = []
        
        registrations.append(registration)
        
        with open(registrations_file, 'w') as f:
            json.dump(registrations, f, indent=2)
        
        return jsonify({
            'success': True,
            'message': 'Registration submitted successfully!',
            'registration_id': registration['id']
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Helper functions for authentication
def hash_password(password):
    """Hash a password using SHA-256 with salt"""
    salt = secrets.token_hex(16)
    password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
    return password_hash, salt

def verify_password(password, stored_hash, salt):
    """Verify a password against stored hash and salt"""
    password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
    return password_hash == stored_hash

def load_users():
    """Load users from file"""
    try:
        with open('users.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_users(users):
    """Save users to file"""
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=2)

def create_demo_user():
    """Create a demo user for testing"""
    users = load_users()
    
    # Check if demo user already exists
    for user in users:
        if user['email'] == 'demo@cyberstudy.com':
            print("Demo user already exists")
            return
    
    # Create demo user
    password_hash, salt = hash_password('demo123')
    demo_user = {
        'id': 'user_demo_001',
        'email': 'demo@cyberstudy.com',
        'password_hash': password_hash,
        'salt': salt,
        'parent_name': 'Demo Parent',
        'created_at': datetime.now().isoformat(),
        'students': [
            {
                'id': 'student_001',
                'name': 'Alex Johnson',
                'age': 10,
                'grade': '5th',
                'level': 'Beginner',
                'enrolled_date': '2024-01-15'
            }
        ]
    }
    
    users.append(demo_user)
    save_users(users)
    print("Demo user created successfully")

def create_admin_user():
    """Create admin user"""
    users = load_users()
    
    # Check if admin user already exists
    for user in users:
        if user['email'] == 'admin@cyberstudy.com':
            print("Admin user already exists")
            return
    
    # Create admin user
    password_hash, salt = hash_password('admin123')
    admin_user = {
        'id': 'admin_001',
        'email': 'admin@cyberstudy.com',
        'password_hash': password_hash,
        'salt': salt,
        'parent_name': 'Admin',
        'role': 'admin',
        'created_at': datetime.now().isoformat(),
        'students': []
    }
    
    users.append(admin_user)
    save_users(users)
    print("Admin user created successfully")

def is_admin(user_id):
    """Check if user is admin"""
    users = load_users()
    for user in users:
        if user['id'] == user_id and user.get('role') == 'admin':
            return True
    return False

# Authentication API endpoints
@app.route('/api/signin', methods=['POST'])
def api_signin():
    try:
        data = request.get_json()
        print(f"Sign-in attempt with data: {data}")
        
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        remember_me = data.get('rememberMe', False)
        
        if not email or not password:
            print("Missing email or password")
            return jsonify({'error': 'Email and password are required'}), 400
        
        users = load_users()
        print(f"Loaded {len(users)} users from database")
        
        user = None
        
        # Find user by email
        for u in users:
            if u['email'] == email:
                user = u
                break
        
        if not user:
            print(f"User not found for email: {email}")
            return jsonify({'error': 'Invalid email or password'}), 401
        
        print(f"Found user: {user['email']}")
        
        # Verify password
        if not verify_password(password, user['password_hash'], user['salt']):
            print("Password verification failed")
            return jsonify({'error': 'Invalid email or password'}), 401
        
        print("Password verified successfully")
        
        # Set session
        session['authenticated'] = True
        session['user_id'] = user['id']
        session['parent_name'] = user['parent_name']
        session['email'] = user['email']
        
        # Check if user is admin
        if user.get('role') == 'admin':
            session['role'] = 'admin'
            print(f"Admin signed in via API: {user['email']}")
            return jsonify({
                'success': True,
                'message': 'Admin sign in successful',
                'parent_name': user['parent_name'],
                'role': 'admin',
                'redirect_url': '/admin'
            })
        
        if remember_me:
            session.permanent = True
        
        print("Session set successfully")
        print(f"Session data after setting: {dict(session)}")
        print(f"Session permanent: {session.permanent}")
        
        return jsonify({
            'success': True,
            'message': 'Sign in successful',
            'parent_name': user['parent_name']
        })
        
    except Exception as e:
        print(f"Sign-in error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/logout', methods=['POST'])
def api_logout():
    try:
        session.clear()
        return jsonify({'success': True, 'message': 'Logged out successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/forgot-password', methods=['POST'])
def api_forgot_password():
    """Handle forgot password requests"""
    try:
        data = request.get_json()
        email = data.get('email', '').strip().lower()
        
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        
        # Validate email format
        import re
        email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        if not re.match(email_regex, email):
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Check if user exists
        users = load_users()
        user_exists = False
        for user in users:
            if user['email'] == email:
                user_exists = True
                break
        
        # Always return success for security (don't reveal if email exists)
        # In a real application, you would:
        # 1. Generate a secure reset token
        # 2. Store it in database with expiration
        # 3. Send email with reset link
        # 4. Log the request for security monitoring
        
        print(f"Password reset requested for email: {email}")
        
        return jsonify({
            'success': True,
            'message': 'If an account with that email exists, a password reset link has been sent.'
        })
        
    except Exception as e:
        print(f"Forgot password error: {str(e)}")
        return jsonify({'error': 'An error occurred processing your request'}), 500

@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    """Password reset page"""
    if request.method == 'POST':
        token = request.form.get('token', '')
        new_password = request.form.get('newPassword', '')
        confirm_password = request.form.get('confirmPassword', '')
        
        # Validate inputs
        if not new_password or not confirm_password:
            return render_template("reset_password.html", 
                                 error="All fields are required", 
                                 token=token)
        
        if new_password != confirm_password:
            return render_template("reset_password.html", 
                                 error="Passwords do not match", 
                                 token=token)
        
        if len(new_password) < 6:
            return render_template("reset_password.html", 
                                 error="Password must be at least 6 characters", 
                                 token=token)
        
        # In a real application, you would:
        # 1. Validate the reset token
        # 2. Check if token is expired
        # 3. Find the user associated with the token
        # 4. Update their password
        # 5. Invalidate the token
        
        # For demo purposes, we'll just show a success message
        print(f"Password reset attempted with token: {token}")
        
        return render_template("reset_password.html", 
                             success="Password has been reset successfully! You can now sign in with your new password.",
                             token=token)
    
    # GET request - show reset form
    token = request.args.get('token', 'demo-token-123')
    return render_template("reset_password.html", token=token)

@app.route('/api/dashboard-data')
def api_dashboard_data():
    try:
        # Check authentication
        print(f"Dashboard data request. Session data: {dict(session)}")
        print(f"Authenticated status: {session.get('authenticated')}")
        
        if not session.get('authenticated'):
            print("User not authenticated for dashboard data")
            return jsonify({'error': 'Not authenticated'}), 401
        
        # Load user data
        users = load_users()
        user = None
        for u in users:
            if u['id'] == session['user_id']:
                user = u
                break
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Generate demo dashboard data
        dashboard_data = {
            'parent_name': user['parent_name'],
            'stats': {
                'total_projects': 12,
                'total_hours': 45,
                'achievements': 8,
                'days_to_next_class': 3
            },
            'progress': {
                'percentage': 75,
                'current_level': 'Intermediate',
                'next_level': 'Advanced'
            },
            'recent_projects': [
                {
                    'name': 'Space Adventure Game',
                    'description': 'Created a 2D platformer using Scratch',
                    'status': 'completed',
                    'date': '2024-01-20'
                },
                {
                    'name': 'Weather App',
                    'description': 'Built a weather display app with Python',
                    'status': 'in_progress',
                    'date': '2024-01-18'
                },
                {
                    'name': 'Robot Dance',
                    'description': 'Programmed robot movements with block coding',
                    'status': 'completed',
                    'date': '2024-01-15'
                }
            ],
            'upcoming_classes': [
                {
                    'title': 'Python Fundamentals',
                    'instructor': 'Ms. Sarah',
                    'date': '2024-01-25',
                    'time': '4:00 PM'
                },
                {
                    'title': 'Game Development Workshop',
                    'instructor': 'Mr. Mike',
                    'date': '2024-01-27',
                    'time': '2:00 PM'
                }
            ],
            'achievements': [
                {
                    'title': 'First Game Complete',
                    'description': 'Successfully created your first video game',
                    'icon': 'gamepad',
                    'date': '2024-01-20'
                },
                {
                    'title': 'Code Debugger',
                    'description': 'Fixed 10 bugs in your programs',
                    'icon': 'bug',
                    'date': '2024-01-18'
                },
                {
                    'title': 'Loop Master',
                    'description': 'Mastered the concept of loops and repetition',
                    'icon': 'sync',
                    'date': '2024-01-15'
                }
            ],
            'messages': [
                {
                    'from': 'Ms. Sarah (Instructor)',
                    'subject': 'Great progress on the weather app!',
                    'preview': 'Alex is doing excellent work on the weather app project...',
                    'date': '2024-01-22',
                    'unread': True
                },
                {
                    'from': 'CyberStudy Team',
                    'subject': 'New coding challenges available',
                    'preview': 'Check out the new coding challenges in your dashboard...',
                    'date': '2024-01-20',
                    'unread': False
                }
            ]
        }
        
        return jsonify(dashboard_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Admin routes
@app.route('/admin')
def admin_dashboard():
    """Admin dashboard - requires admin authentication"""
    if not session.get('authenticated') or not is_admin(session.get('user_id')):
        return redirect(url_for('signin'))
    
    return render_template("admin_dashboard.html")

@app.route('/admin/signin', methods=['GET', 'POST'])
def admin_signin():
    """Redirect to main signin page - admin credentials now handled there"""
    return redirect(url_for('signin'))

@app.route('/admin/logout')
def admin_logout():
    """Admin logout"""
    session.clear()
    return redirect(url_for('signin'))

# Admin API endpoints
@app.route('/api/admin/students')
def api_admin_students():
    """Get all students for admin"""
    if not session.get('authenticated') or not is_admin(session.get('user_id')):
        return jsonify({'error': 'Admin access required'}), 403
    
    users = load_users()
    all_students = []
    
    for user in users:
        if user.get('role') != 'admin':  # Skip admin users
            for student in user.get('students', []):
                student_data = student.copy()
                student_data['parent_name'] = user['parent_name']
                student_data['parent_email'] = user['email']
                student_data['parent_id'] = user['id']
                all_students.append(student_data)
    
    return jsonify({'students': all_students})

@app.route('/api/admin/students/<student_id>/progress', methods=['POST'])
def api_update_student_progress(student_id):
    """Update student progress"""
    if not session.get('authenticated') or not is_admin(session.get('user_id')):
        return jsonify({'error': 'Admin access required'}), 403
    
    try:
        data = request.get_json()
        
        # Load users and find the student
        users = load_users()
        student_found = False
        
        for user in users:
            if user.get('role') != 'admin':
                for student in user.get('students', []):
                    if student['id'] == student_id:
                        # Update student progress
                        if 'progress' not in student:
                            student['progress'] = {}
                        
                        student['progress'].update({
                            'last_updated': datetime.now().isoformat(),
                            'current_level': data.get('current_level', student['progress'].get('current_level', 'Beginner')),
                            'completed_projects': data.get('completed_projects', student['progress'].get('completed_projects', 0)),
                            'total_hours': data.get('total_hours', student['progress'].get('total_hours', 0)),
                            'achievements': data.get('achievements', student['progress'].get('achievements', 0)),
                            'next_class_date': data.get('next_class_date', student['progress'].get('next_class_date')),
                            'notes': data.get('notes', student['progress'].get('notes', ''))
                        })
                        student_found = True
                        break
                if student_found:
                    break
        
        if not student_found:
            return jsonify({'error': 'Student not found'}), 404
        
        # Save updated users
        save_users(users)
        
        return jsonify({'success': True, 'message': 'Student progress updated successfully'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/parents')
def api_admin_parents():
    """Get all parent accounts for admin"""
    if not session.get('authenticated') or not is_admin(session.get('user_id')):
        return jsonify({'error': 'Admin access required'}), 403
    
    users = load_users()
    parents = []
    
    for user in users:
        if user.get('role') != 'admin':  # Skip admin users
            parent_data = {
                'id': user['id'],
                'name': user['parent_name'],
                'email': user['email'],
                'created_at': user['created_at'],
                'student_count': len(user.get('students', [])),
                'students': user.get('students', [])
            }
            parents.append(parent_data)
    
    return jsonify({'parents': parents})

@app.route('/api/admin/parents/<parent_id>', methods=['PUT', 'DELETE'])
def api_manage_parent(parent_id):
    """Update or delete parent account"""
    if not session.get('authenticated') or not is_admin(session.get('user_id')):
        return jsonify({'error': 'Admin access required'}), 403
    
    users = load_users()
    parent_found = False
    
    if request.method == 'DELETE':
        # Delete parent account
        users = [user for user in users if user['id'] != parent_id]
        save_users(users)
        return jsonify({'success': True, 'message': 'Parent account deleted successfully'})
    
    elif request.method == 'PUT':
        # Update parent account
        data = request.get_json()
        
        for user in users:
            if user['id'] == parent_id and user.get('role') != 'admin':
                user['parent_name'] = data.get('parent_name', user['parent_name'])
                user['email'] = data.get('email', user['email'])
                parent_found = True
                break
        
        if not parent_found:
            return jsonify({'error': 'Parent not found'}), 404
        
        save_users(users)
        return jsonify({'success': True, 'message': 'Parent account updated successfully'})

# Initialize demo user and admin on startup
create_demo_user()
create_admin_user()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=port)