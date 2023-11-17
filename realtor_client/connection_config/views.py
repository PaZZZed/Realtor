from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

from .forms import UserForm
from django.contrib import messages
from .odoo_rpc import OdooRpc
from django.urls import reverse
from django.views.generic import DetailView, ListView
import logging

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

# Create your views here.


class IndexView(ListView):
    model = User
    template_name = "connection_config/index.html"
    context_object_name = 'user_login'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['form'] = UserForm

        return context

def logout_view(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # The user is authenticated, so log them out
        logout(request)
        return redirect('/')
    else:
        # The user is not authenticated, so redirect them to the login page
        return redirect('/')
        
def login_new(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            # The form is valid, so we can try to authenticate the user
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # Call the function to authenticate the user using the XML-RPC protocol
            authenticated = OdooRpc.authenticate(username=username, password=password)
                              
            # if user is None:
            if authenticated is None:
                messages.error(request,"User does not exist!")
                logging.exception("Erreur lors de la connexion au système Odoo")
            else:
                # authenticate(username=authenticated.username, password=password)
                login(request, authenticated)
                
                return redirect('/')  
    else:
        form = UserForm()
        return render(request, 'connection_config/index.html', {'form': form, 'error': 'Invalid username or password'})

