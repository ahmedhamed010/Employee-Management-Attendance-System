from django.db import models
from accounts.models import User


class EmployeeStatus(models.TextChoices):
    ACTIVE     = 'active',     'Active'
    INACTIVE   = 'inactive',   'Inactive'
    SUSPENDED  = 'suspended',  'Suspended'
    TERMINATED = 'terminated', 'Terminated'


class Employee(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile')
    employee_id = models.CharField(max_length=20, unique=True)
    # department  = models.CharField(max_length=100)
    department = models.ForeignKey(
        'departments.Department',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='employees')
    job_title   = models.CharField(max_length=100)
    salary      = models.DecimalField(max_digits=10, decimal_places=2)
    hire_date   = models.DateField()
    manager     = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subordinates'
    )
    status      = models.CharField(
        max_length=20,
        choices=EmployeeStatus.choices,
        default=EmployeeStatus.ACTIVE
    )
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        db_table        = 'employees'
        verbose_name    = 'Employee'
        verbose_name_plural = 'Employees'
        ordering        = ['-created_at']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.employee_id}"