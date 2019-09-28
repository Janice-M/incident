
from django.conf.urls import url
from django.urls import path
from . import views



urlpatterns = [
   
    path('',views.index,name='index'),

    path('create_ticket/',views.create_ticket.,name='createticket'),
    
]



if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)