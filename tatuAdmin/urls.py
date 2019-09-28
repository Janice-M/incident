from django.conf.urls import url
from django.urls import path
from . import views
from .views import TicketDeleteView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.admin_home,name='admin_home'),
    path('user_management/',views.user_management,name='user_management'),
    path('user_management/create_agent',views.create_agent,name='create_agent'),
    path('user_management/<int:pk>/edit_agent',views.edit_agent,name='edit_agent'),
    path('department_management/',views.department_management,name='department_management'),
    path('department_management/create_department',views.create_department,name='create_department'),
    path('department_management/<int:pk>/edit_department',views.edit_department,name='edit_department'),
    path('ticket_management/',views.ticket_management,name='ticket_management'),
    path('ticket_management/create_ticket',views.create_ticket,name='create_ticket'),
    path('ticket_management/<int:pk>/edit_ticket',views.edit_ticket,name='edit_ticket'),
    path('ticket_management/<int:pk>/delete_ticket',views.TicketDeleteView.as_view(),name='delete_ticket'),
    path('ticket_management/create_subtype',views.create_ticket_subtypes,name='create_ticket_subtype'),
    path('logout/',auth_views.LogoutView.as_view(template_name='registration/logout.html')),
    path('login/',auth_views.LoginView.as_view(template_name='registration/login.html'),name='login'),
    
    
]

