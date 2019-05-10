# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.http import *
from .models import Account
from .forms import AccountForm

# Create your views here.
def signup_view(request):
    if request.method=='POST':
        nombre = request.POST['nombre']
        apellido= request.POST['apellido']
        correo = request.POST['correo']
        clave = request.POST['clave']
        account = Account.objects.create(nombre = nombre, appellido = apellido,
                                       correo = correo,
                                       clave = clave, is_superuser = False)
        account.save()
        nickname = nombre + apellido
        user = User.objects.create_user(username=nickname, email=correo, password=clave)
        user.save()
        accounts = Account.objects.all()
        return redirect('/accounts/signup', {'accounts': accounts})
    accounts = Account.objects.all()
    return render(request,'accounts/signup.html', {'accounts': accounts})

def login_view(request):
    if request.method=='POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            username = User.objects.get(email=email).username
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/home')
        except User.DoesNotExist:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    return render(request,'accounts/login.html')


def logout_view(request):
    if request.method=='POST':
        logout(request)
        return redirect('.')

def account_details(request, account_key):
    account_keys= account_key.split("-")
    account= Account.objects.get(nombre=account_keys[0], appellido=account_keys[1])

    if request.method=='POST':
        nombre = request.POST['nombre']
        appellido= request.POST['appellido']
        correo = request.POST['correo']
        clave = request.POST['clave']
        nickname= nombre+appellido
        original_email=account.correo
        user=User.objects.get(email=original_email)
        print(user.username)
        print(user.email)
        print(user.password)
        account.nombre=nombre
        account.appellido=appellido
        account.correo=correo
        account.clave=clave
        account.save()
        user.email=correo
        user.username=nickname
        user.set_password(clave)
        user.save()
        print(user.password)

        return redirect('/accounts/signup')

    """Para cuando se seleccione el botón de curso"""

     # filter puede retornar más de un parámetro
    return render(request, 'accounts/accounts_details.html', {'account': account})

def delete_account(request):
    if request.method=='POST':
        id=request.POST['id_account']
        account=Account.objects.get(id=id)
        mail = account.correo
        account.delete()
        usuario = User.objects.get(email=mail)
        usuario.delete()
    accounts= Account.objects.all()
    return render(request, 'accounts/signup.html',{'accounts':accounts})


