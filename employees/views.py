from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from accounts.permissions import *
from .models import *
from .serializers import *
from .filters import *
from .pagination import *


# -----------------------------------------------
# 1. List & Create Employees
# -----------------------------------------------
class EmployeeListCreateView(APIView):
    permission_classes = [IsAuthenticated , IsAdminOrHR]

    def get(self , request):
        employees = Employee.objects.select_related('user' , 'manager').all()
        serializer = EmployeeSerializer(employees , many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)
    
    def post(self , request):
        serializer = CreateEmployeeSerializer(data=request.data)
        if serializer.is_valid():
            employee = serializer.save()
            return Response(
                EmployeeSerializer(employee).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -----------------------------------------------
# 2. Get, Update & Delete Employee
# -----------------------------------------------
class EmployeeDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrHR]
    
    def get_object(self , id):
        try : 
            return Employee.objects.select_related('user' , 'manager').get(id=id)
        except Employee.DoesNotExist :
            return None

    def get(self , request , id):
        employee = self.get_object(id)
        if not employee :
            return Response({'error': 'Employee not found.'} , status=status.HTTP_404_NOT_FOUND)
        return Response(EmployeeSerializer(employee).data)

    def put(self , request , id):
        employee = self.get_object(id)
        if not employee :
            return Response({'error': 'Employee not found.'} , status=status.HTTP_404_NOT_FOUND)

        serializer = CreateEmployeeSerializer(employee , data=request.data , partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(EmployeeSerializer(employee).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self , request , id):
        employee = self.get_object(id)
        if not employee :
            return Response({'error': 'Employee not found.'}, status=status.HTTP_404_NOT_FOUND)
        employee.delete()
        return Response({'message': 'Employee deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)


# -----------------------------------------------
# 3. Employee Search
# -----------------------------------------------
class EmployeeSearchView(APIView):
    permission_classes = [IsAuthenticated , IsAdminOrHR]

    filter_backends = [DjangoFilterBackend , SearchFilter , OrderingFilter]
    filter_classes = EmployeeFilter
    pagination_classes = EmployeePagination

    # Search
    search_fields  = [
        'user__first_name',
        'user__last_name',
        'user__email',
        'department',
        'employee_id',
    ]

    # Ordering
    ordering_fields = ['hire_date', 'salary', 'created_at', 'department']
    ordering = ['created_at']

    def get(self , request):
        queryset = Employee.objects.select_related('user' , 'manager').all()
        
        # Filtering
        filterset = EmployeeFilter(request.GET , queryset=queryset)
        if filterset.is_valid():
            queryset=filterset.qs
        
        # Search
        search = request.GET.get('search')
        if search :
            queryset = queryset.filter(
                models.Q(user__first_name__icontains = search) |
                models.Q(user__last_name__icontains = search) |
                models.Q(user__email__icontains = search)     |
                models.Q(department__icontains = search)
            )

        # Ordering
        ordering = request.GET.get('ordering', '-created_at')
        if ordering.lstrip('-') in ['hire_date', 'salary', 'created_at', 'department']:
            queryset = queryset.order_by(ordering)

        # Pagination
        paginator = EmployeePagination()
        page      = paginator.paginate_queryset(queryset, request)
        serializer = EmployeeSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)