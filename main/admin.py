# main/admin.py
from django.contrib import admin
from .models import Student, Event, Attendance, Alumni

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone')
    search_fields = ('first_name', 'last_name', 'email')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'event_date')
    search_fields = ('event_name',)

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'event', 'status')
    search_fields = ('student__first_name', 'student__last_name', 'event__event_name')



@admin.register(Alumni)
class AlumniAdmin(admin.ModelAdmin):
    list_display = ('student', 'graduation_date')
    search_fields = ('student__first_name', 'student__last_name')

