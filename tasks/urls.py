from django.urls import path
from .views import (
    TaskListView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    toggle_task,
    register_view,
    login_view,
    logout_view
)

urlpatterns = [
    path('', TaskListView.as_view(), name='home'),
    path('add/', TaskCreateView.as_view(), name='add_task'),
    path('edit/<int:pk>/', TaskUpdateView.as_view(), name='edit_task'),
    path('delete/<int:pk>/', TaskDeleteView.as_view(), name='delete_task'),
    path('toggle/<int:pk>/', toggle_task, name='toggle_task'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]



