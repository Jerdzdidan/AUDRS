from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    # path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    # path('officer/dashboard/', views.officer_dashboard, name='officer_dashboard'),
    path('create-user/', views.create_user, name='create-user'),
    path('student-list/', views.accounts_list_students, name='student-list'),
    path('officer-list/', views.accounts_list_officers, name='officer-list'),
    path('admin-list/', views.accounts_list_admins, name='admin-list'),
    path('update/<int:user_id>/', views.update_user, name='account-update'),
    path('delete/<int:user_id>/', views.delete_user, name='account-delete-confirm'),
]