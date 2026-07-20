from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from accounts.permissions import *
from .models import *
from .serializers import *

# Create your views here.

# -----------------------------------------------
# 1. List & Create
# -----------------------------------------------
class DepartmentListCreateView(APIView):
    permission_classes = [IsAuthenticated , IsAdminOrHR]
    
    def get(self , request):
        departments = Department.objects.prefetch_related('employees').all()
        serializer = DepartmentSerializer(departments , many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)

    def post(self , request):
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)


# -----------------------------------------------
# 2. Get, Update & Delete
# -----------------------------------------------
class DepartmentDetailView(APIView):
    permission_classes = [IsAuthenticated , IsAdminOrHR]
    
    def get_object(self , id):
        try : 
            return Department.objects.prefetch_related("employees").get(id = id)
        except Department.DoesNotExist:
            return None

    def get(self , request , id):
        department = self.get_object(id)
        if not department:
            return Response({'error':'Departments Not Fount'} , status=status.HTTP_404_NOT_FOUND)
        return Response(DepartmentSerializer(department).data)

    def put(self , request , id):
        department = self.get_object(id=id)
        if not department:
            return Response({'error':'Departments Not Fount'} , status=status.HTTP_404_NOT_FOUND)
        serializer = DepartmentSerializer(department , data=request.data , partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

    def delete(self , request , id):
        department = self.get_object(id=id)
        if not department :
            return Response({'error': 'Department not found.'}, status=status.HTTP_404_NOT_FOUND)
        department.delete()
        return Response({'message': 'Department deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)



