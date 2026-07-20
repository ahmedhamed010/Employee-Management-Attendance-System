from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


from accounts.permissions import IsAdminOrHR , IsManager 
from .models import *
from .serializers import *

# Create your views here.

# -----------------------------------------------
# 1. List & Create
# -----------------------------------------------
class LeaveRequestListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self , request):
        if request.user.role in ['admin' , 'hr']:
            leaves = LeaveRequest.objects.select_related('employee__user').all()
        else:
            leaves = LeaveRequest.objects.filter(employee = request.user.employee_profile)
        serializer = LeaveRequestSerializer(leaves , many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)
    
    def post(self , request):
        try:
            employee = request.user.employee_profile 
        except Exception as e :
            return Response({'error':str(e)} , status=status.HTTP_404_NOT_FOUND)
        
        data = request.data.copy()
        data['employee'] = employee.id
        
        serializer = LeaveRequestSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -----------------------------------------------
# 2. Get, Update & Delete
# -----------------------------------------------
class LeaverequestDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self , id):
        try : 
            return LeaveRequest.objects.select_related('employee__user').get(id=id)
        except LeaveRequest.DoesNotExist :
            return None
    
    def get(self , request , id):
        leave = self.get_object(id)
        if not leave :
            return Response({'error':'Leave Request Not Found'} , status=status.HTTP_404_NOT_FOUND)
        return Response(LeaveRequestSerializer(leave).data)
    
    def patch(self , request , id):
        leave = self.get_object(id)
        if not leave :
            return Response({'error':'Leave Request Not Found'} , status=status.HTTP_404_NOT_FOUND)
        
        if leave.employee.user != request.user:
            return Response({'error':'Permission denied.'} , status=status.HTTP_403_FORBIDDEN)
        if leave.status != 'pending':
            return Response ({'error':'Cannot edit a processed leave request.'} , status=status.HTTP_400_BAD_REQUEST)
        
        serializer = LeaveRequestSerializer(leave , data=request.data , partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self , request , id):
        leave = self.get_object(id)
        if not leave :
            return Response({'error': 'Leave request not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        if leave.employee.user != request.user:
            return Response({'error':'Permission denied.'} , status=status.HTTP_403_FORBIDDEN)
        if leave.status != 'pending':
            return Response ({'error':'Cannot delete a processed leave request.'} , status=status.HTTP_400_BAD_REQUEST)
        
        leave.delete()
        return Response({'message': 'Leave request deleted successfully.'}, status=status.HTTP_200_OK)


# -----------------------------------------------
# 3. Approve & Reject  (Admin & HR بس)
# -----------------------------------------------
class LeaveStatusView(APIView):
    permission_classes = [IsAuthenticated , IsAdminOrHR]
    
    def patch(self , request ,id):
        try :
            leave = LeaveRequest.objects.get(id=id)
        except LeaveRequest.DoesNotExist :
            return Response({'error': 'Leave request not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = LeavaStatusSerializer(leave , data=request.data , partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': f'Leave request {leave.status}.',
                'data': LeaveRequestSerializer(leave).data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -----------------------------------------------
# 4. Manager Approval
# -----------------------------------------------
class ManagerApprovalView(APIView):
    permission_classes = [IsAuthenticated , IsManager]
    
    def patch(self , request , id):
        try:
            leave = LeaveRequest.objects.get(id=id)
        except LeaveRequest.DoesNotExist:
            return Response(
                {'error': 'Leave request not found.'} ,
                status=status.HTTP_404_NOT_FOUND)
        
        if leave.status != 'pending':
            return Response(
                {'error': f'Cannot process a {leave.status} request.'},
                status=status.HTTP_400_BAD_REQUEST)
        action = request.data.get('action')
        if action == 'approve':
            leave.status = LeaveStatus.MANAGER_APPROVED
            leave.manager_action_by = request.user.employee_profile
        elif action == 'reject':
            leave.status            = LeaveStatus.REJECTED
            leave.manager_action_by = request.user.employee_profile
            leave.rejection_reason  = request.data.get('rejection_reason', '')
        else :
            return Response(
                {'error':'Action must be approve or reject.'},status=status.HTTP_400_BAD_REQUEST
            )
        leave.save()
        return Response ({
            'message': f'Leave request {leave.status} by Manager.',
            'data': LeaveRequestSerializer(leave).data
        }, status=status.HTTP_200_OK)


# -----------------------------------------------
# 5. HR Approval
# -----------------------------------------------
class HrApprovalView(APIView):
    permission_classes = [IsAuthenticated , IsAdminOrHR]
    
    def patch(self , request , id):
        try:
            leave = LeaveRequest.objects.get(id=id)
        except LeaveRequest.DoesNotExist :
            return Response({'error': 'Leave request not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        if leave.status != 'manager_approved':
            return Response(
                {'error': 'Leave request must be approved by manager first.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        action = request.data.get('action')
        if action == 'approve':
            leave.status = LeaveStatus.APPROVED
            leave.hr_action_by = request.user.employee_profile
        elif action == 'reject':
            leave.status = LeaveStatus.REJECTED
            leave.hr_action_by = request.user.employee_profile
            leave.rejection_reason = request.data.get('rejection_reason','')
        else :
            return Response(
                {'error': 'Action must be approve or reject.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        leave.save()
        return Response({
                'message': f'Leave request {leave.status} by HR.',
                'data': LeaveRequestSerializer(leave).data
            }, status=status.HTTP_200_OK)

















