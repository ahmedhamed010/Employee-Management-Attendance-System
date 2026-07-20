from rest_framework import serializers
from .models import AttendanceRecord

class AttendanceSerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField()
    working_hours = serializers.SerializerMethodField()

    class Meta:
        model  = AttendanceRecord
        fields = [
            'id', 'employee', 'employee_name',
            'date', 'check_in', 'check_out',
            'working_hours', 'status', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_employee_name(self, obj):
        return obj.employee.user.get_full_name()

    def get_working_hours(self, obj):
        if obj.check_in and obj.check_out:
            from datetime import datetime
            check_in  = datetime.combine(obj.date, obj.check_in)
            check_out = datetime.combine(obj.date, obj.check_out)
            diff      = check_out - check_in
            hours     = diff.seconds // 3600
            minutes   = (diff.seconds % 3600) // 60
            return f"{hours}h {minutes}m"
        return None

    def validate(self, attrs):
        check_in  = attrs.get('check_in')
        check_out = attrs.get('check_out')
        if check_in and check_out and check_out <= check_in:
            raise serializers.ValidationError({'check_out': 'Check-out must be after check-in.'})
        return attrs