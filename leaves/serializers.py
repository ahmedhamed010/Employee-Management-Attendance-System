from rest_framework import serializers
from .models import *

class LeaveRequestSerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField()
    manager_action_by = serializers.SerializerMethodField() 
    hr_action_by      = serializers.SerializerMethodField()
    total_days = serializers.SerializerMethodField()
    
    class Meta:
        model = LeaveRequest
        fields = [
            'id', 'employee', 'employee_name',
            'leave_type', 'start_date', 'end_date',
            'total_days', 'reason', 'status',
            'rejection_reason' , 'manager_action_by','hr_action_by',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'status', 'created_at', 'updated_at']
    
    def get_employee_name(self , obj):
        return obj.employee.user.get_full_name()
    
    def get_total_days(self , obj):
        return (obj.end_date - obj.start_date).days + 1
    
    def get_manager_action_by(self , obj):
        if obj.manager_action_by:
            return {
                'id':   obj.manager_action_by.id,
                'name': obj.manager_action_by.user.get_full_name()
            }
        return None
    
    def get_hr_action_by(self , obj):
        if obj.hr_action_by :
            return{
                'id' : obj.hr_action_by.id,
                'name' : obj.hr_action_by.user.get_full_name()
            }
        return None
    
    def validate(self , attrs):
        start_date = attrs.get('start_date' , self.instance.start_date if self.instance else None)
        end_date = attrs.get('end_date' ,   self.instance.end_date   if self.instance else None)
        
        if end_date < start_date :
            raise serializers.ValidationError(
                {'end_date':'End date must be after start date.'}
            )
        
        employee = attrs.get('employee')
        overlapping = LeaveRequest.objects.filter(
            employee=employee,
            status__in = ['pending' , 'approved'],
            start_date__lte=end_date,
            end_date__gte = start_date
        )
        if self.instance :
            overlapping = overlapping.exclude(id=self.instance.id)
        if overlapping.exists():
            raise serializers.ValidationError(
                {'start_date':'You already have a leave request in this period.'}
            )
        return attrs



class LeavaStatusSerializer(serializers.ModelSerializer):
    class Meta :
        model = LeaveRequest
        fields = ['status']




class LeaveApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model  = LeaveRequest
        fields = ['status', 'rejection_reason']

    def validate_status(self, value):
        allowed = ['manager_approved', 'approved', 'rejected', 'cancelled']
        if value not in allowed:
            raise serializers.ValidationError(f'Status must be one of {allowed}')
        return value




