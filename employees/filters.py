import django_filters
from .models import Employee

class EmployeeFilter(django_filters.FilterSet):
    
    name = django_filters.CharFilter(method='filter_by_name', label='Name')
    email = django_filters.CharFilter(field_name='user__email' , lookup_expr='icontains')
    department = django_filters.CharFilter(field_name='department' , lookup_expr='icontains')
    status = django_filters.ChoiceFilter(choices=[
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
        ('terminated', 'Terminated'),
    ])
    
    salary_min = django_filters.NumberFilter(field_name='salary', lookup_expr='gte')
    salary_max = django_filters.NumberFilter(field_name='salary', lookup_expr='lte')
    
    hire_date_from = django_filters.DateFilter(field_name='hire_date', lookup_expr='gte')
    hire_date_to   = django_filters.DateFilter(field_name='hire_date', lookup_expr='lte')
    
    class Meta:
        model  = Employee
        fields = ['name', 'email', 'department', 'status', 'salary_min', 'salary_max']

    def filter_by_name(self, queryset, name, value):
        return queryset.filter(
            models.Q(user__first_name__icontains=value) |
            models.Q(user__last_name__icontains=value)
        )
    
    
    
    