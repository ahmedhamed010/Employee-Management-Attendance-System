from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import time as dtime


from accounts.permissions import IsAdminOrHR, IsAdminOrManager
from .models import *
from .serializers import AttendanceSerializer


# -----------------------------------------------
# 1. List & Create
# -----------------------------------------------
class AttendanceListCreateView(APIView):
    permission_classes = [IsAuthenticated , IsAdminOrHR]

    def get(self , request):
        records = AttendanceRecord.objects.select_related('employee__user').all()

        # Filter by employee
        employee_id = request.GET.get('employee_id')
        if employee_id:
            records = records.filter(employee_id=employee_id)

        # Filter by date range
        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')
        if date_from  :
            records = records.filter(date__gte=date_from)
        if date_to :
            records = records.filter(date__lte=date_to)

        # Filter by status
        status_filter = request.GET.get('status')
        if status_filter :
            records = records.filter(status=status_filter)

        serializer = AttendanceSerializer(records , many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)

    def post(self , request):
        serializer = AttendanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)


# -----------------------------------------------
# 2. Get, Update & Delete
# -----------------------------------------------
class AttendanceDetailView(APIView):
    permission_classes = [IsAuthenticated , IsAdminOrHR]

    def get_object(self , id):
        try:
            return AttendanceRecord.objects.select_related('employee__user').get(id=id)
        except AttendanceRecord.DoesNotExist :
            return None

    def get(self , request , id):
        record = self.get_object(id)
        if not record :
            return Response({'error':'Record not found.'} , status=status.HTTP_404_NOT_FOUND)
        return Response(AttendanceSerializer(record).data)

    def put(self , request , id):
        record = self.get_object(id)
        if not record:
            return Response({'error':'Record not found.'} , status=status.HTTP_404_NOT_FOUND)
        serializer = AttendanceSerializer(record , data=request.data , partial=True)
        if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self , request , id):
        record = self.get_object(id)
        if not record :
            return Response({'error': 'Employee not found.'}, status=status.HTTP_404_NOT_FOUND)
        record.delete()
        return Response({'message': 'Record deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)


# -----------------------------------------------
# 3. My Attendance
# -----------------------------------------------
class MyAttendanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            employee = request.user.employee_profile
        except Exception:
            return Response({'error': 'Employee profile not found.'}, status=status.HTTP_404_NOT_FOUND)

        records    = AttendanceRecord.objects.filter(employee=employee)
        serializer = AttendanceSerializer(records, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# -----------------------------------------------
# 4. Check-In
# -----------------------------------------------
class CheckInView(APIView):
    permission_classes = [IsAuthenticated]
    
    WORK_START_TIME = dtime(9, 0, 0)   
    LATE_THRESHOLD  = dtime(9, 15, 0)  
    
    def post(self , request):
        try:
            employee = request.user.employee_profile
        except Exception as e :
            return Response( {'error': str(e)} , status=status.HTTP_404_NOT_FOUND)

        today = timezone.localdate()
        now = timezone.localtime().time()
        
        # Prevent duplicate check-in
        existing_record = AttendanceRecord.objects.filter(employee=employee , date=today).first()
        if existing_record:
            return Response(
                {
                    'error': 'Already checked in today.',
                    'check_in': existing_record.check_in,
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if now > self.LATE_THRESHOLD:
            attendance_status = AttendanceStatus.LATE
        else :
            attendance_status - AttendanceStatus.PRESENT
        
        record = AttendanceRecord.objects.create(
            employee=employee,
            date=today,
            check_in=now,
            status=attendance_status
        )
        
        return Response(
            {
                'message': 'Checked in successfully.',
                'is_late':attendance_status == AttendanceStatus.LATE,
                'data': AttendanceSerializer(record).data
            },
            status=status.HTTP_201_CREATED
        )


# -----------------------------------------------
# 5. Check-Out
# -----------------------------------------------
class CheckOutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self , request):
        try:
            employee = request.user.employee_profile
        except Exception as e:
            return Response({'error':str(e)} , status=status.HTTP_404_NOT_FOUND)

        today = timezone.localdate()
        now = timezone.localtime().time()

        record = AttendanceRecord.objects.filter(employee=employee , date=today).first()

        if not record :
            return Response({
                    'error': 'You have not checked in today.',
                    'check_out': record.check_out,
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if record.check_out is not None:
            return Response(
                {
                    'error': 'Already checked out today.',
                    'check_out': str(record.check_out),
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        record.check_out = now
        record.save(update_fields=['check_out', 'updated_at']) 
        record.refresh_from_db()

        return Response(
            {
                'message': 'Checked out successfully.',
                'data': AttendanceSerializer(record).data
            },
            status=status.HTTP_200_OK)









