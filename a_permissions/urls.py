from django.urls import path
from . import views

app_name = 'permissions'

urlpatterns = [
    path('my-permissions/', views.MyPermissionsView.as_view(), name='my_permissions'),
    path('pending/', views.PendingPermissionsView.as_view(), name='pending'),
    path('history/', views.PermissionHistoryView.as_view(), name='history'),
    path('<int:pk>/', views.PermissionDetailView.as_view(), name='detail'),
    path('<int:pk>/approve/', views.ApprovePermissionView.as_view(), name='approve'),
    path('<int:pk>/reject/', views.RejectPermissionView.as_view(), name='reject'),
    path('list/', views.PermissionListView.as_view(), name='permission_list'),
] 