from django.urls import path
from .views import *

urlpatterns = [
    path('register/',                 RegisterView.as_view(),          name='register'),
    path('login/',                    LoginView.as_view(),             name='login'),
    path('logout/',                   LogoutView.as_view(),            name='logout'),
    path('profile/',                  ProfileView.as_view(),           name='profile'),
    path('changepassword/',           ChangePasswordView.as_view(),    name='changepassword'),
    path('refresh/',                  RefreshTokenView.as_view(),      name='refresh'),
    path('users/',                    AllUsersView.as_view(),          name='all-users'),
    path('users/<int:user_id>/role/', AssignRoleView.as_view(),        name='assign-role'),

]