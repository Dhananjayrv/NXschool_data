from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired, Email
from flask_wtf.file import FileField, FileAllowed
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from datetime import datetime
import os
import uuid
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school.db'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

owner_credentials = {'rv': 'rv@82102'}


# Define School and Student models
class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    students = db.relationship('Student', backref='school', lazy=True)
    teachers = db.relationship('Teacher', backref='school', lazy=True)
    non_students = db.relationship('NonStudent', backref='school', lazy=True)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    middle_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    father_first_name = db.Column(db.String(100), nullable=False)
    father_last_name = db.Column(db.String(100), nullable=False)
    father_occupation = db.Column(db.String(100), nullable=False)
    father_dob = db.Column(db.Date, nullable=False)
    father_wedding_date = db.Column(db.Date, nullable=False)
    address_line1 = db.Column(db.String(100), nullable=False)
    address_line2 = db.Column(db.String(100))
    address_line3 = db.Column(db.String(100))
    pin_code = db.Column(db.String(20), nullable=False)
    student_image = db.Column(db.String(100))
    father_image = db.Column(db.String(100))
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'), nullable=False)

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    middle_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    father_first_name = db.Column(db.String(100), nullable=False)
    father_last_name = db.Column(db.String(100), nullable=False)
    father_occupation = db.Column(db.String(100), nullable=False)
    father_dob = db.Column(db.Date, nullable=False)
    father_wedding_date = db.Column(db.Date, nullable=False)
    address_line1 = db.Column(db.String(100), nullable=False)
    address_line2 = db.Column(db.String(100))
    address_line3 = db.Column(db.String(100))
    pin_code = db.Column(db.String(20), nullable=False)
    teacher_image = db.Column(db.String(100))
    teacher_father_image = db.Column(db.String(100))
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'), nullable=False)

class NonStudent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    middle_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    father_first_name = db.Column(db.String(100), nullable=False)
    father_last_name = db.Column(db.String(100), nullable=False)
    father_occupation = db.Column(db.String(100), nullable=False)
    father_dob = db.Column(db.Date, nullable=False)
    father_wedding_date = db.Column(db.Date, nullable=False)
    address_line1 = db.Column(db.String(100), nullable=False)
    address_line2 = db.Column(db.String(100))
    address_line3 = db.Column(db.String(100))
    pin_code = db.Column(db.String(20), nullable=False)
    non_student_image = db.Column(db.String(100))
    non_student_father_image = db.Column(db.String(100))
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'), nullable=False)

# Define a function to create tables within the application context
def create_tables():
    with app.app_context():
        db.create_all()

# Call the function to create tables
create_tables()

# Routes
@app.route('/')
def index():
    schools = School.query.all()
    return render_template('index.html', schools=schools)

@app.route('/admin/dashboard')
def admin_dashboard():
    schools = School.query.all()
    return render_template('admin/dashboard.html', schools=schools)

@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'rv' and password == owner_credentials['rv']:
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials. Please try again.', 'error')

    return render_template('login.html')

@app.route('/school/<int:school_id>')
def school_detail(school_id):
    school = School.query.get_or_404(school_id)
    students = school.students
    non_students = school.non_students
    teachers = school.teachers
    
    # Construct URLs for images
    for student in students:
        student.student_image_url = url_for('static', filename=f'uploads/{school.name}/student/{student.student_image}')
        student.father_image_url = url_for('static', filename=f'uploads/{school.name}/student/{student.father_image}')
    
    for teacher in teachers:
        teacher.teacher_image_url = url_for('static', filename=f'uploads/{school.name}/teacher/{teacher.teacher_image}')
        teacher.teacher_father_image_url = url_for('static', filename=f'uploads/{school.name}/teacher/{teacher.teacher_father_image}')
    
    for non_student in non_students:
        non_student.non_student_image_url = url_for('static', filename=f'uploads/{school.name}/non_student/{non_student.non_student_image}')
        non_student.non_student_father_image_url = url_for('static', filename=f'uploads/{school.name}/non_student/{non_student.non_student_father_image}')
    
    return render_template('details.html', school=school, students=students, non_students=non_students, teachers=teachers)


@app.route('/school/add', methods=['POST'])
def add_school():
    name = request.form['name']
    new_school = School(name=name)
    db.session.add(new_school)
    db.session.commit()
    
    # Create directory for the school
    school_folder_path = os.path.join(app.config['UPLOAD_FOLDER'], name)
    os.makedirs(school_folder_path, exist_ok=True)
    
    # Create subdirectories for student, non-student, and teacher
    for folder in ['student', 'non_student', 'teacher']:
        folder_path = os.path.join(school_folder_path, folder)
        os.makedirs(folder_path, exist_ok=True)
    
    flash('School added successfully!', 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/school/delete/<int:school_id>', methods=['POST'])
def delete_school(school_id):
    school = School.query.get_or_404(school_id)
    db.session.delete(school)
    db.session.commit()
    flash('School deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/submit', methods=['POST'])
def submit_form():
    school_name = request.form['school_name']
    role = request.form['role']
    
    # Retrieve form data based on role
    if role == 'student':
        # Retrieve student form data
        first_name = request.form['first_name']
        middle_name = request.form['middle_name']
        last_name = request.form['last_name']
        phone_number = request.form.get('phone_number_student')  # Use .get() method to handle missing keys gracefully
        if not phone_number:
            flash('Phone number is required for students', 'error')
            return redirect(url_for('index'))
        email = request.form['email']
        dob_str = request.form.get('dob')  # Check if key exists before accessing
        if dob_str:
            dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
        else:
            dob = None
        father_first_name = request.form['father_first_name']
        father_last_name = request.form['father_last_name']
        father_occupation = request.form['father_occupation']
        father_dob = datetime.strptime(request.form['father_dob'], '%Y-%m-%d').date()
        father_wedding_date = datetime.strptime(request.form['father_wedding_date'], '%Y-%m-%d').date()
        address_line1 = request.form['address_line1']
        address_line2 = request.form['address_line2']
        address_line3 = request.form['address_line3']
        pin_code = request.form['pin_code']
        student_image = request.files['student_image']
        father_image = request.files['father_image']
        
        # Create directory path
        school_folder_path = os.path.join(app.config['UPLOAD_FOLDER'], school_name, 'student')
        os.makedirs(school_folder_path, exist_ok=True)
        
        # Save images
        student_image.save(os.path.join(school_folder_path, secure_filename(student_image.filename)))
        father_image.save(os.path.join(school_folder_path, secure_filename(father_image.filename)))

        school = School.query.filter_by(name=school_name).first()
        new_student = Student(
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            phone_number=phone_number,
            email=email,
            dob=dob,
            father_first_name=father_first_name,
            father_last_name=father_last_name,
            father_occupation=father_occupation,
            father_dob=father_dob,
            father_wedding_date=father_wedding_date,
            address_line1=address_line1,
            address_line2=address_line2,
            address_line3=address_line3,
            pin_code=pin_code,
            student_image=student_image.filename,
            father_image=father_image.filename,
            school_id=school.id
        )
        db.session.add(new_student)
        
    
    elif role == 'teacher':
        # Retrieve teacher form data
        first_name = request.form['first_name_teacher']
        middle_name = request.form['middle_name_teacher']
        last_name = request.form['last_name_teacher']
        phone_number = request.form.get('phone_number_teacher')  # Use .get() method to handle missing keys gracefully
        if not phone_number:
            flash('Phone number is required for teachers', 'error')
            return redirect(url_for('index'))
        email = request.form['email_teacher']
        dob_teacher_str = request.form.get('dob_teacher')  # Check if key exists before accessing
        if dob_teacher_str:
            dob_teacher = datetime.strptime(dob_teacher_str, '%Y-%m-%d').date()
        else:
            dob_teacher = None
        father_first_name = request.form['father_first_name_teacher']
        father_last_name = request.form['father_last_name_teacher']
        father_occupation = request.form['father_occupation_teacher']
        father_dob = datetime.strptime(request.form['father_dob_teacher'], '%Y-%m-%d').date()
        father_wedding_date = datetime.strptime(request.form['father_wedding_date_teacher'], '%Y-%m-%d').date()
        address_line1 = request.form['address_line1_teacher']
        address_line2 = request.form['address_line2_teacher']
        address_line3 = request.form['address_line3_teacher']
        pin_code = request.form['pin_code_teacher']
        teacher_image = request.files['teacher_image']
        teacher_father_image = request.files['teacher_father_image']
        
        # Create directory path
        school_folder_path = os.path.join(app.config['UPLOAD_FOLDER'], school_name, 'teacher')
        os.makedirs(school_folder_path, exist_ok=True)
        
        # Save images
        teacher_image.save(os.path.join(school_folder_path, secure_filename(teacher_image.filename)))
        teacher_father_image.save(os.path.join(school_folder_path, secure_filename(teacher_father_image.filename)))
        
        subject = request.form['subject_teacher']

        school = School.query.filter_by(name=school_name).first()
        new_teacher = Teacher(
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            phone_number=phone_number,
            email=email,
            dob=dob_teacher,
            father_first_name=father_first_name,
            father_last_name=father_last_name,
            father_occupation=father_occupation,
            father_dob=father_dob,
            father_wedding_date=father_wedding_date,
            address_line1=address_line1,
            address_line2=address_line2,
            address_line3=address_line3,
            pin_code=pin_code,
            teacher_image=teacher_image.filename,
            teacher_father_image=teacher_father_image.filename,
            school_id=school.id,
            subject=subject
        )
        db.session.add(new_teacher)
    
    elif role == 'non_student':
        # Retrieve non-student form data
        first_name = request.form['first_name_non_student']
        middle_name = request.form['middle_name_non_student']
        last_name = request.form['last_name_non_student']
        phone_number = request.form.get('phone_number_non_student')  # Use .get() method to handle missing keys gracefully
        if not phone_number:
            flash('Phone number is required for non-students', 'error')
            return redirect(url_for('index'))
        email = request.form['email_non_student']
        dob_non_student_str = request.form.get('dob_non_student')  # Check if key exists before accessing
        if dob_non_student_str:
            dob_non_student = datetime.strptime(dob_non_student_str, '%Y-%m-%d').date()
        else:
            dob_non_student = None
        father_first_name = request.form['father_first_name_non_student']
        father_last_name = request.form['father_last_name_non_student']
        father_occupation = request.form['father_occupation_non_student']
        father_dob = datetime.strptime(request.form['father_dob_non_student'], '%Y-%m-%d').date()
        father_wedding_date = datetime.strptime(request.form['father_wedding_date_non_student'], '%Y-%m-%d').date()
        address_line1 = request.form['address_line1_non_student']
        address_line2 = request.form['address_line2_non_student']
        address_line3 = request.form['address_line3_non_student']
        pin_code = request.form['pin_code_non_student']
        non_student_image = request.files['non_student_image']
        non_student_father_image = request.files['non_student_father_image']
        
        # Create directory path
        school_folder_path = os.path.join(app.config['UPLOAD_FOLDER'], school_name, 'non_student')
        os.makedirs(school_folder_path, exist_ok=True)
        
        # Save images
        non_student_image.save(os.path.join(school_folder_path, secure_filename(non_student_image.filename)))
        non_student_father_image.save(os.path.join(school_folder_path, secure_filename(non_student_father_image.filename)))

        school = School.query.filter_by(name=school_name).first()
        new_non_student = NonStudent(
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            phone_number=phone_number,
            email=email,
            dob=dob_non_student,
            father_first_name=father_first_name,
            father_last_name=father_last_name,
            father_occupation=father_occupation,
            father_dob=father_dob,
            father_wedding_date=father_wedding_date,
            address_line1=address_line1,
            address_line2=address_line2,
            address_line3=address_line3,
            pin_code=pin_code,
            non_student_image=non_student_image.filename,
            non_student_father_image=non_student_father_image.filename,
            school_id=school.id
        )
        db.session.add(new_non_student)
    
    db.session.commit()
    flash('Data submitted successfully!', 'success')
    return redirect(url_for('index'))



@app.route('/dashboard')
def dashboard():
    schools = School.query.all()
    return render_template('admin/dashboard.html', schools=schools)


if __name__ == '__main__':
    app.run(debug=True)

