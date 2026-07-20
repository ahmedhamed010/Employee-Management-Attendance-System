from django.db import models
from employees.models import Employee

# Create your models here.

class AttendanceStatus(models.TextChoices):
    PRESENT  = 'present',  'Present'
    ABSENT   = 'absent',   'Absent'
    LATE     = 'late',     'Late'
    REMOTE   = 'remote',   'Remote'
    HALF_DAY = 'half_day', 'Half-Day'


class AttendanceRecord(models.Model):
    employee = models.ForeignKey(Employee , on_delete=models.CASCADE , related_name='attendance_records')
    date      = models.DateField()
    check_in  = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    status    = models.CharField(
        max_length=20,
        choices=AttendanceStatus.choices,
        default=AttendanceStatus.PRESENT
    )
    notes     = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table            = 'attendance_records'
        verbose_name        = 'Attendance Record'
        verbose_name_plural = 'Attendance Records'
        ordering            = ['-date']
        unique_together     = ['employee', 'date'] 

    def __str__(self):
        return f"{self.employee} - {self.date} - {self.status}"