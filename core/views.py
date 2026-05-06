from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Student, Announcement, Attendance, Marks, Timetable
import csv
import io

# Login View
def login_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            error = 'Invalid username or password'
    return render(request, 'login.html', {'error': error})

# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')

# Dashboard View
@login_required(login_url='login')
def dashboard(request):
    # If admin, redirect to upload page
    if request.user.is_superuser:
        return redirect('upload_students')
    
    student = Student.objects.get(user=request.user)
    announcements = Announcement.objects.order_by('-date')[:3]
    return render(request, 'dashboard.html', {
        'student': student,
        'announcements': announcements
    })

# Announcements View
@login_required(login_url='login')
def announcements(request):
    all_announcements = Announcement.objects.order_by('-date')
    return render(request, 'announcements.html', {
        'announcements': all_announcements
    })

# Attendance View
@login_required(login_url='login')
def attendance(request):
    student = Student.objects.get(user=request.user)
    attendance_data = Attendance.objects.filter(student=student)
    return render(request, 'attendance.html', {
        'attendance_data': attendance_data
    })

# Marks View
@login_required(login_url='login')
def marks(request):
    student = Student.objects.get(user=request.user)
    marks_data = Marks.objects.filter(student=student)
    return render(request, 'marks.html', {
        'marks_data': marks_data
    })

# Timetable View
@login_required(login_url='login')
def timetable(request):
    timetable_data = Timetable.objects.all().order_by('day')
    return render(request, 'timetable.html', {
        'timetable_data': timetable_data
    })


import csv
import io
from django.contrib.auth.models import User
from django.contrib import messages

# CSV Upload View — only for admin
def upload_students(request):
    if not request.user.is_superuser:
        return redirect('dashboard')

    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']

        # Read the file
        data = csv_file.read().decode('utf-8')
        reader = csv.DictReader(io.StringIO(data))

        success = 0
        skipped = 0

        for row in reader:
            usn = row['usn'].strip()
            dob = row['dob'].strip()

            # Skip if student with this USN already exists
            if User.objects.filter(username=usn).exists():
                skipped += 1
                continue

            # Create login account
            user = User.objects.create_user(
                username=usn,
                password=dob
            )

            # Create student profile
            Student.objects.create(
                user=user,
                name=row['name'].strip(),
                usn=usn,
                department=row['department'].strip(),
                semester=int(row['semester'].strip()),
                dob=dob
            )
            success += 1

        messages.success(request, f"✅ {success} students added successfully! {skipped} skipped (already exist).")
        return redirect('upload_students')

    return render(request, 'upload_students.html')

# Marks CSV Upload View — only for admin
def upload_marks(request):
    if not request.user.is_superuser:
        return redirect('dashboard')

    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        data = csv_file.read().decode('utf-8')
        reader = csv.DictReader(io.StringIO(data))

        success = 0
        skipped = 0

        for row in reader:
            usn = row['usn'].strip()
            subject = row['subject'].strip()
            marks = row['marks'].strip()

            try:
                student = Student.objects.get(usn=usn)
            except Student.DoesNotExist:
                skipped += 1
                continue

            Marks.objects.update_or_create(
                student=student,
                subject=subject,
                defaults={'marks': float(marks)}
            )
            success += 1

        messages.success(request, f"✅ {success} marks entries added! {skipped} skipped (USN not found).")
        return redirect('upload_marks')

    return render(request, 'upload_marks.html')