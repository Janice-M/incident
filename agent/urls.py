
from django.conf.urls import url
from django.urls import path
from . import views



urlpatterns = [
    path('',views.agent_home,name='agent_home'),
    path('take_or_assign_ticket/<int:pk>/',views.take_or_assign_ticket,name='take_or_assign_ticket'),
    # path('profile/',views.profile,name='profile'),
]
