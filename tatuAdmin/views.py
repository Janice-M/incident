from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import *
from .models import *
from django.views.generic import (UpdateView,DeleteView)
from django.contrib.auth.mixins import (LoginRequiredMixin,UserPassesTestMixin)
from django.contrib.messages.views import SuccessMessageMixin

# Create your views here.
@login_required
def admin_home(request):
    return render(request,'adminHome.html')

