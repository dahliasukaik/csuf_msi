
# main/views.py
import csv
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from .models import Attendance, Event, Student
from .forms import AttendanceForm, EventForm, StudentForm, BulkUploadForm
from django.contrib import messages

def bulk_upload_students(request):
    if request.method == 'POST':
        form = BulkUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['file']
            fs = FileSystemStorage()
            filename = fs.save(csv_file.name, csv_file)
            file_path = fs.path(filename)

            try:
                with open(file_path, newline='', encoding='utf-8') as csvfile:
                    reader = csv.reader(csvfile)
                    # Skip the header row if your file has one
                    next(reader, None)
                    for row in reader:
                        first_name, last_name, email = row
                        # Check for existing email to prevent duplicates
                        if not Student.objects.filter(email=email).exists():
                            Student.objects.create(
                                first_name=first_name,
                                last_name=last_name,
                                email=email
                            )
                        else:
                            messages.warning(request, f"Student with email {email} already exists.")
                messages.success(request, "The students have been successfully uploaded.")
            except Exception as e:
                messages.error(request, f"An error occurred while processing the file: {e}")
            
            return redirect('dashboard')
    else:
        form = BulkUploadForm()
    return render(request, 'main/bulk_upload.html', {'form': form})

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

def manage_students(request):
    students = Student.objects.all()
    return render(request, 'main/manage_students.html', {'students': students})

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

