from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.dashboard, name='dashboard'),
    path('events/<int:event_id>/attendees/', views.view_attendees, name='view_attendees'),
    path('take_attendance/', views.take_attendance, name='take_attendance'),
    path('attendance_success/', views.attendance_success, name='attendance_success'),
    path('manage_students/', views.manage_students, name='manage_students'),
    path('add_student/', views.add_student, name='add_student'),
    path('add_event/', views.add_event, name='add_event'),
    path('manage_events/', views.manage_events, name='manage_events'),
    path('edit_event/<int:event_id>/', views.edit_event, name='edit_event'),
    path('delete_event/<int:event_id>/', views.delete_event, name='delete_event'),
]

