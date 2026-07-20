from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('employees/', include('employees.urls')),
    path('departments/', include('departments.urls')),
    path('attendance/', include('attendance.urls')),
    path('leaves/', include('leaves.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
