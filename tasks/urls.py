from django.urls import path
from .views import *
app_name = 'tasks'

urlpatterns = [
    path('register/', register_view,name='register'),
    path('login/',login_view,name='login'),
    path('logout/',logout_view,name='logout'),
    path('home/', home,name='home'),
    path('update-task/<int:id>/', update_task, name='update-task'),
    path('delete-task/<int:id>/', delete_task, name='delete-task'),
]