from rest_framework import serializers
from accounts.serializers import UserSerializer
from .models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    user    = UserSerializer(read_only=True)
    manager = serializers.SerializerMethodField()

    class Meta:
        model  = Employee
        fields = [
            'id', 'user', 'employee_id', 'department',
            'job_title', 'salary', 'hire_date',
            'manager', 'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_manager(self, obj):
        if obj.manager:
            return {
                'id':          obj.manager.id,
                'employee_id': obj.manager.employee_id,
                'name':        obj.manager.user.get_full_name(),
            }
        return None


class CreateEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Employee
        fields = [
            'user', 'employee_id', 'department',
            'job_title', 'salary', 'hire_date',
            'manager', 'status'
        ]

    def validate_user(self, value):
        if Employee.objects.filter(user=value).exists():
            raise serializers.ValidationError('This user already has an employee profile.')
        return value