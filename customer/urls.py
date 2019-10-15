from django.conf.urls import url
from django.urls import path
from . import views



urlpatterns = [
    path('',views.index,name='index'),
    path('create_ticket/',views.create_ticket,name='createticket'),
    path('profile/',views.profile,name='profile'),
    path('ajax/load-subtypes/',views.load_subtypes,name='ajax_load_subtypes'),
    url(r'^search/$',views.search_issues,name='search_results'),

]
