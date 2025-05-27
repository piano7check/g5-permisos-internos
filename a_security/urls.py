from django.urls import path
from . import views

app_name = 'security'

urlpatterns = [
    path('register-access/', views.RegisterAccessView.as_view(), name='register_access'),
    path('access-history/', views.AccessHistoryView.as_view(), name='access_history'),
    path('record-access/', views.RecordAccessView.as_view(), name='record_access'),
    path('permission/<int:pk>/', views.PermissionDetailView.as_view(), name='permission_detail'),
] 