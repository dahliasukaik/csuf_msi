from django.db import models


class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    contact_info = models.TextField(null=True, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Event(models.Model):
    event_name = models.CharField(max_length=100)
    event_date = models.DateField()

    def __str__(self):
        return self.event_name

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    attendance_date = models.DateField()
    status = models.CharField(max_length=20)  # e.g., Present, Absent

    def __str__(self):
        return f"{self.student} - {self.event} - {self.status}"

class Alumni(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    graduation_date = models.DateField()

    def __str__(self):
        return f"{self.student} - {self.graduation_date}"
