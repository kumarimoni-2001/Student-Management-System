from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Student, Subject, Marks

# Home page view
def home(request):
    # Get statistics for the home page
    total_students = Student.objects.count()
    total_subjects = Subject.objects.count()
    total_marks = Marks.objects.count()
    
    # Get top performing students
    results = Marks.objects.select_related('student', 'subject').all()
    
    # Calculate percentages for each student
    student_data = {}
    for mark in results:
        if mark.student.id not in student_data:
            student_data[mark.student.id] = {
                'student': mark.student,
                'total_marks': 0,
                'subject_count': 0,
                'subjects': []
            }
        student_data[mark.student.id]['total_marks'] += mark.marks_obtained
        student_data[mark.student.id]['subject_count'] += 1
        student_data[mark.student.id]['subjects'].append({
            'subject': mark.subject,
            'marks': mark.marks_obtained
        })
    
    # Calculate percentages and grades
    student_results = []
    for student_id, data in student_data.items():
        if data['subject_count'] > 0:
            data['percentage'] = data['total_marks'] / data['subject_count']
            # Determine grade
            if data['percentage'] >= 90:
                data['grade'] = 'A+'
            elif data['percentage'] >= 80:
                data['grade'] = 'A'
            elif data['percentage'] >= 70:
                data['grade'] = 'B'
            elif data['percentage'] >= 60:
                data['grade'] = 'C'
            elif data['percentage'] >= 50:
                data['grade'] = 'D'
            else:
                data['grade'] = 'F'
            student_results.append(data)
    
    # Sort by percentage (highest first) and get top 4
    student_results.sort(key=lambda x: x.get('percentage', 0), reverse=True)
    top_students = student_results[:4]
    
    context = {
        'total_students': total_students,
        'total_subjects': total_subjects,
        'total_marks': total_marks,
        'student_results': top_students
    }
    return render(request, 'home.html', context)

# Add student view
def add_student(request):
    if request.method == "POST":
        # Get data from form
        name = request.POST.get('name')
        roll_number = request.POST.get('roll_number')
        student_id = request.POST.get('student_id')
        email = request.POST.get('email')
        
        # Check for duplicates
        if Student.objects.filter(roll_number=roll_number).exists():
            messages.error(request, 'Student with this roll number already exists!')
        elif Student.objects.filter(student_id=student_id).exists():
            messages.error(request, 'Student with this ID already exists!')
        elif Student.objects.filter(email=email).exists():
            messages.error(request, 'Student with this email already exists!')
        else:
            # Save to database
            Student.objects.create(
                name=name,
                roll_number=roll_number,
                student_id=student_id,
                email=email
            )
            messages.success(request, f'Student {name} added successfully!')
            return redirect('home')
    
    return render(request, 'add_student.html')

# Add marks view
def add_marks(request):
    if request.method == "POST":
        student_name = request.POST.get('student_name')
        subject_name = request.POST.get('subject')
        marks_value = request.POST.get('marks')
        
        # Check if student exists
        try:
            student = Student.objects.get(name=student_name)
        except Student.DoesNotExist:
            messages.error(request, f'Student "{student_name}" does not exist! Please add student first.')
            return redirect('add_student')
        
        # Get or create subject
        subject, created = Subject.objects.get_or_create(name=subject_name)
        
        # Save marks
        Marks.objects.create(
            student=student,
            subject=subject,
            marks_obtained=marks_value
        )
        messages.success(request, f'Marks added successfully for {student_name}!')
        return redirect('view_results')
    
    # Get all students and subjects for dropdown
    students = Student.objects.all()
    subjects = Subject.objects.all()
    context = {
        'students': students,
        'subjects': subjects
    }
    return render(request, 'add_marks.html', context)

# View results - FIXED function name to match urls.py
def view_results(request):
    # Get all marks with student and subject info
    results = Marks.objects.select_related('student', 'subject').all()
    
    # Calculate total and percentage for each student
    student_results = {}
    for mark in results:
        if mark.student.id not in student_results:
            student_results[mark.student.id] = {
                'student': mark.student,
                'total_marks': 0,
                'subject_count': 0,
                'subjects': []
            }
        student_results[mark.student.id]['total_marks'] += mark.marks_obtained
        student_results[mark.student.id]['subject_count'] += 1
        student_results[mark.student.id]['subjects'].append({
            'subject': mark.subject,
            'marks': mark.marks_obtained
        })
    
    # Calculate percentage and grade
    for student_id, data in student_results.items():
        if data['subject_count'] > 0:
            data['percentage'] = data['total_marks'] / data['subject_count']
            # Determine grade
            if data['percentage'] >= 90:
                data['grade'] = 'A+'
            elif data['percentage'] >= 80:
                data['grade'] = 'A'
            elif data['percentage'] >= 70:
                data['grade'] = 'B'
            elif data['percentage'] >= 60:
                data['grade'] = 'C'
            elif data['percentage'] >= 50:
                data['grade'] = 'D'
            else:
                data['grade'] = 'F'
    
    context = {
        'student_results': student_results.values()
    }
    return render(request, 'results.html', context)

# Calculate results
def calculate_result(request):
    # Get all students and subjects for dropdown
    students = Student.objects.all()
    subjects = Subject.objects.all()
    
    calculation = None
    if request.method == "POST":
        student_name = request.POST.get('student_name')
        subject_name = request.POST.get('subject')
        marks = request.POST.get('marks')
        
        # Check if student exists
        try:
            student = Student.objects.get(name=student_name)
        except Student.DoesNotExist:
            messages.error(request, f'Student "{student_name}" does not exist! Please add student first.')
            return redirect('add_student')
        
        # Calculate grade
        percentage = float(marks)
        
        if percentage >= 90:
            grade = 'A+'
        elif percentage >= 80:
            grade = 'A'
        elif percentage >= 70:
            grade = 'B'
        elif percentage >= 60:
            grade = 'C'
        elif percentage >= 50:
            grade = 'D'
        else:
            grade = 'F'
        
        calculation = f"Grade: {grade}"
        messages.success(request, f'Result calculated! Grade: {grade}')
        
        # Save to database
        subject, _ = Subject.objects.get_or_create(name=subject_name)
        Marks.objects.create(
            student=student,
            subject=subject,
            marks_obtained=marks
        )
        
    context = {
        'calculation': calculation,
        'students': students,
        'subjects': subjects
    }
    return render(request, 'calculate_result.html', context)