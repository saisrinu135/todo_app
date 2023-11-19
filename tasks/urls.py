from django.urls import path
from .views import *
app_name = 'tasks'

urlpatterns = [
    path('register/', register_view,name='register'),
    path('login/',login_view,name='login'),
    path('logout/',logout_view,name='logout'),
    path('home/', home,name='home'),
]