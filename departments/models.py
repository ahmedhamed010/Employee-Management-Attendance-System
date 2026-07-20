from django.db import models
from employees.models import *

# Create your models here.

class Department(models.Model):
    name        = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    manager     = models.OneToOneField(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_department'
    )
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        db_table            = 'departments'
        verbose_name        = 'Department'
        verbose_name_plural = 'Departments'
        ordering            = ['name']

    def __str__(self):
        return self.name
