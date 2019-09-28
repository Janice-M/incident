
from django.conf.urls import url
from django.urls import path
from . import views



urlpatterns = [
   
    path('',customer_views.index,name='index'),

    path('',customer_views.index,name='index'),
    
]



if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)