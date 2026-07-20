from django.urls import path
from .views import *

urlpatterns = [

    path('departments/',                    DepartmentListCreateView.as_view(),          name='department-list'),
    path('departments/<int:id>',           DepartmentDetailView.as_view(),              name='department-list'),

]