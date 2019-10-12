from django.conf.urls import url
from django.urls import path
from . import views



urlpatterns = [
    path('',views.agent_home,name='agent_home'),
    path('take_or_assign_ticket/<int:pk>/',views.take_or_assign_ticket,name='take_or_assign_ticket'),
    path('my_tickets/',views.my_tickets,name='my_tickets'),
    path('resolve_tickets/<int:pk>',views.resolve_ticket,name='resolve_ticket'),
    # path('profile/',views.profile,name='profile'),
    path('agent_profile/',views.profile,name='agent_profile'),
    path('create_ticket_for_customer',views.create_ticket_for_customer,name='create_ticket_for_customer'),
]
