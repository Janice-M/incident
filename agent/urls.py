
from django.conf.urls import url
from django.urls import path
from . import views



urlpatterns = [
    path('',views.index,name='index'),
    path('take_or_assign_ticket/<int:pk>/',views.take_or_assign_ticket,name='take_or_assign_ticket'),
    # path('profile/',views.profile,name='profile'),
]
