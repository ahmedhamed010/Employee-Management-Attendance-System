from django.db import models
from employees.models import Employee

# Create your models here.


class LeaveType(models.TextChoices):
    ANNUAL    = 'annual',    'Annual'
    SICK      = 'sick',      'Sick'
    EMERGENCY = 'emergency', 'Emergency'
    UNPAID    = 'unpaid',    'Unpaid'

class LeaveStatus(models.TextChoices):
    PENDING   = 'pending'  , 'Pending'
    MANAGER_APPROVED  = 'manager_approved',  'Manager Approved'
    APPROVED  = 'approved' , 'Approved'
    REJECTED  = 'rejected' , 'Rejected'
    CANCELLED = 'cancelled', 'Cancelled'



class LeaveRequest(models.Model):

    employee = models.ForeignKey(Employee , on_delete=models.CASCADE , related_name='leave_requests')
    leave_type = models.CharField(choices=LeaveType.choices)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(choices=LeaveStatus , default=LeaveStatus.PENDING)
    manager_action_by = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='manager_approvals'
    )
    hr_action_by      = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='hr_approvals'
    )
    rejection_reason  = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table            = 'leave_requests'
        verbose_name        = 'Leave Request'
        verbose_name_plural = 'Leave Requests'
        ordering            = ['-created_at']

    def __str__(self):
        return f"{self.employee} - {self.leave_type} - {self.status}"
    




