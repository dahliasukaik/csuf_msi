import csv
import chardet
from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import FileSystemStorage
from .models import Attendance, Event, Student
from .forms import AttendanceForm, EventForm, StudentForm, BulkUploadForm
from django.contrib import messages



def edit_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully.')
            return redirect('manage_events')
    else:
        form = EventForm(instance=event)
    return render(request, 'main/edit_event.html', {'form': form})

def delete_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted successfully.')
        return redirect('manage_events')
    return render(request, 'main/delete_event.html', {'event': event})
    
def edit_student(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student information updated successfully.')
            return redirect('manage_students')
    else:
        form = StudentForm(instance=student)
    return render(request, 'main/edit_student.html', {'form': form})

def delete_student(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student deleted successfully.')
        return redirect('manage_students')
    return render(request, 'main/delete_student.html', {'student': student})

def manage_students(request):
    if request.method == 'POST':
        form = BulkUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['file']
            fs = FileSystemStorage()
            filename = fs.save(csv_file.name, csv_file)
            file_path = fs.path(filename)

            try:
                # Detect encoding
                with open(file_path, 'rb') as rawfile:
                    rawdata = rawfile.read(1000)
                    result = chardet.detect(rawdata)
                    encoding = result['encoding']

                # Attempt to open with detected encoding
                try:
                    with open(file_path, newline='', encoding=encoding) as csvfile:
                        reader = csv.reader(csvfile)
                        next(reader, None)  # Skip header row if present
                        for row in reader:
                            first_name, last_name, email = row
                            if not Student.objects.filter(email=email).exists():
                                Student.objects.create(
                                    first_name=first_name,
                                    last_name=last_name,
                                    email=email
                                )
                            else:
                                messages.warning(request, f"Student with email {email} already exists.")
                    messages.success(request, "The students have been successfully uploaded.")
                
                # Fallback to common encodings if the detected one fails
                except UnicodeDecodeError:
                    with open(file_path, newline='', encoding='ISO-8859-1') as csvfile:
                        reader = csv.reader(csvfile)
                        next(reader, None)  # Skip header row if present
                        for row in reader:
                            first_name, last_name, email = row
                            if not Student.objects.filter(email=email).exists():
                                Student.objects.create(
                                    first_name=first_name,
                                    last_name=last_name,
                                    email=email
                                )
                            else:
                                messages.warning(request, f"Student with email {email} already exists.")
                    messages.success(request, "The students have been successfully uploaded with a fallback encoding.")
            except Exception as e:
                messages.error(request, f"An error occurred while processing the file: {e}")
            
            return redirect('manage_students')
    else:
        form = BulkUploadForm()

    students = Student.objects.all()
    return render(request, 'main/manage_students.html', {'form': form, 'students': students})



def view_attendees(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    attendees = Attendance.objects.filter(event=event)
    return render(request, 'main/view_attendees.html', {'event': event, 'attendees': attendees})


def dashboard(request):
    return render(request, 'main/dashboard.html')


def take_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            event = form.cleaned_data['event']
            event_date = event.event_date
            first_names = request.POST.getlist('first_name')
            last_names = request.POST.getlist('last_name')
            emails = request.POST.getlist('email')
            statuses = request.POST.getlist('status')

            for first_name, last_name, email, status in zip(first_names, last_names, emails, statuses):
                try:
                    student = Student.objects.get(first_name=first_name, last_name=last_name, email=email)
                    attendance, created = Attendance.objects.get_or_create(
                        student=student,
                        event=event,
                        defaults={'status': status, 'attendance_date': event_date}
                    )
                    if not created:
                        attendance.status = status
                        attendance.attendance_date = event_date
                        attendance.save()
                except Student.DoesNotExist:
                    form.add_error(None, f'Student {first_name} {last_name} not found.')
                except Student.MultipleObjectsReturned:
                    form.add_error(None, f'Multiple students found for {first_name} {last_name}. Please refine your search.')
            if not form.errors:
                return redirect('attendance_success')
    else:
        form = AttendanceForm()

    return render(request, 'main/take_attendance.html', {'form': form})


def attendance_success(request):
    return render(request, 'main/attendance_success.html')


def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_events')
    else:
        form = EventForm()
    return render(request, 'main/add_event.html', {'form': form})


def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_students')
    else:
        form = StudentForm()
    return render(request, 'main/add_student.html', {'form': form})


def manage_events(request):
    events = Event.objects.all()
    return render(request, 'main/manage_events.html', {'events': events})


def edit_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('manage_events')
    else:
        form = EventForm(instance=event)
    return render(request, 'main/edit_event.html', {'form': form})


def delete_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        event.delete()
        return redirect('manage_events')
    return render(request, 'main/delete_event.html', {'event': event})


