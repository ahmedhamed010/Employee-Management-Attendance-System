from django.urls import path
from .views import *

urlpatterns = [

    path('leaves/',                             LeaveRequestListCreateView.as_view(),                name='leaves'),
    path('leaves/<int:id>/',                    LeaverequestDetailView.as_view(),                    name='leaves'),
    path('leaves/<int:id>/status/',             LeaveStatusView.as_view(),                           name='leave-status'),
    path('leaves/<int:id>/manager-approval/',   ManagerApprovalView.as_view(),                       name='manager-approval'),
    path('leaves/<int:id>/hr-approval/',   HrApprovalView.as_view(),                            name='hr-approval'),

]