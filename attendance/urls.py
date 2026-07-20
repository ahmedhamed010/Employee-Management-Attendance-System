from django.urls import path
from .views import *

urlpatterns = [

    path('attendance/',             AttendanceListCreateView.as_view(), name='attendance-list-create'),
    path('attendance/me/',          MyAttendanceView.as_view(),         name='my-attendance'),
    path('attendance/check-in/',    CheckInView.as_view(),              name='check-in'),
    path('attendance/check-out/',   CheckOutView.as_view(),             name='check-out'),
    path('attendance/<int:id>/',    AttendanceDetailView.as_view(),     name='attendance-detail'),

]