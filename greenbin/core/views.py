from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

from core.forms import RegistrationForm
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView


from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('core:index')
    else:
        form = RegistrationForm()

    return render(request, 'registration/signup.html', {'form': form})

@login_required(login_url="/login")
def whatsnext(request):
    return render(request, 'core/whats_next.html')