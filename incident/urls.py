"""incident URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from customer import views as customer_views

from django.contrib.auth import views as auth_views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('',customer_views.index,name='index'),
    path('register/',customer_views.register,name='register'),
    path('login/',auth_views.LoginView.as_view(template_name='registration/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='registration/logout.html'),name='logout'),
    path('tatuadmin/',include('tatuAdmin.urls')),
    path('customer/',include('customer.urls')),
    path('agent/', include('agent.urls')),
    # path('auth/', include('djoser.urls')),
    # path('auth/', include('djoser.urls.authtoken')),
    # path('api/', include('chat.urls')),

]

# # djoser urls
# urlpatterns += [
#     path('auth/', include('djoser.urls')),
#     path('auth/', include('djoser.urls.authtoken')),
# ]


# chat app urls
# urlpatterns += [
#     path('api/', include('chat.urls')),
# ]
#



if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
