from rest_framework import serializers
from .models import Department

class DepartmentSerializer(serializers.ModelSerializer):
    manager_name = serializers.SerializerMethodField()
    total_employees = serializers.SerializerMethodField()
    
    class Meta:
        model = Department
        fields = [
            'id', 'name', 'description',
            'manager', 'manager_name',
            'total_employees',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
        
    def get_manager_name(self, obj):
        if obj.manager:
            return obj.manager.user.get_full_name()
        return None

    def get_total_employees(self, obj):
        return obj.employees.count()
        