# main/forms.py
from django import forms
from .models import Attendance, Event, Student



class BulkUploadForm(forms.Form):
    file = forms.FileField(label='Select a CSV file')

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'contact_info', 'email', 'phone']
        widgets = {
            'contact_info': forms.Textarea(attrs={'rows': 4}),
            'email': forms.EmailInput(attrs={'placeholder': 'student@example.com'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone Number'}),
        }
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'contact_info': 'Contact Information',
            'email': 'Email Address',
            'phone': 'Phone Number',
        }
        help_texts = {
            'email': 'Enter a valid email address.',
        }

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['event_name', 'event_date']
        widgets = {
            'event_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'event_name': 'Event Name',
            'event_date': 'Event Date',
        }



ATTENDANCE_STATUS_CHOICES = [
    ('Present', 'Present'),
    ('Absent', 'Absent'),
    ('Excused', 'Excused'),
]

class AttendanceForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=True, help_text="Enter the student's first name")
    last_name = forms.CharField(max_length=50, required=True, help_text="Enter the student's last name")
    email = forms.EmailField(required=True, help_text="Enter the student's email address")
    status = forms.ChoiceField(choices=ATTENDANCE_STATUS_CHOICES, required=True)

    class Meta:
        model = Attendance
        fields = ['event', 'first_name', 'last_name', 'email', 'status']
        labels = {
            'event': 'Event',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
            'status': 'Attendance Status',
        }
        help_texts = {
            'first_name': 'Enter the student\'s first name.',
            'last_name': 'Enter the student\'s last name.',
            'email': 'Enter the student\'s email address.',
        }

    
