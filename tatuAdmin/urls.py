from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('',views.admin_home,name='admin_home'),
    path('user_management/',views.user_management,name='user_management'),
]

