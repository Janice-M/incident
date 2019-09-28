
from django.conf.urls import url

from django.urls import path

from customer import views as customer_views

from django.contrib.auth import views as auth_views



urlpatterns = [
   
    path('',customer_views.index,name='index'),
    
]



if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)