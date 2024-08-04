import os
import django
from datetime import date

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Student


def add_students():
    Student.objects.create(
        student_id='FC5204',
        first_name='John',
        last_name='Doe',
        birth_date='1995-05-15',
        email='john.doe@university.com')

    new_student = Student(
        student_id='FE0054',
        first_name='Jane',
        last_name='Smith',
        email='jane.smith@university.com')
    new_student.save()

    Student.objects.create(
        student_id='FH2014',
        first_name='Alice',
        last_name='Johnson',
        birth_date='1998-02-10',
        email='alice.johnson@university.com')

    Student.objects.create(
        student_id='FH2015',
        first_name='Bob',
        last_name='Wilson',
        birth_date='1996-11-25',
        email='bob.wilson@university.com')

def get_students_info():
    all_students = Student.objects.all()
    students_info_lst = []
    for student_obj in all_students:
        students_info_lst.append(
            f'Student №{student_obj.student_id}: '
            f'{student_obj.first_name} {student_obj.last_name}; '
            f'Email: {student_obj.email}'
        )
    return "\n".join(students_info_lst)

def update_students_emails():
    all_students_obj = Student.objects.all()

    for student_obj in all_students_obj:
        student_obj.email = student_obj.email.replace('university.com', 'uni-students.com')
        # print(student_obj.email)
        student_obj.save()

def truncate_students():
    all_students_obj = Student.objects.all()
    all_students_obj.delete()
