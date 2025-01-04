from django.urls import path
from .views import *

urlpatterns = [
    path('admin/signup/', AdminSignupView.as_view(), name='admin-signup'),
    path('admin/login/', LoginView.as_view(), name='login'),
    path('admin/users/', UserListView.as_view(), name='user-list'),
    path('admin/users/<str:user_id>/', UserDetailView.as_view(), name='user-detail'),
    path('admin/users/<str:user_id>/status/', UpdateUserStatusView.as_view(), name='user-status-update'),
    path('admin/users/<str:user_id>/delete/', DeleteUserView.as_view(), name='user-delete'),
]
