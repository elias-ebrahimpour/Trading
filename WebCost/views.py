# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages

#####
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from json import JSONEncoder
from django.views.decorators.csrf import csrf_exempt
from WebCost.models import User, Token, Expense, Income, NewUserForm
from datetime import datetime
from django.conf import settings
import random
# Create your views here


def homepage(request):
    """View function for home page of site."""
    return HttpResponse("this is just for test in homepage :)")


def logout(request):
    # logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("login")


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                messages.info(request, f"You are now logged in as {username}")
                return redirect('homepage')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"form": form})


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            login(request, user)
            return redirect("")

        else:
            for msg in form.error_messages:
                print(form.error_messages[msg])

            return render(request=request,
                          template_name="register.html",
                          context={"form": form})

    form = UserCreationForm
    return render(request=request,
                  template_name="register.html",
                  context={"form": form})


@csrf_exempt
def submit_expense(request):
    """ user submit an expense """
    this_token = request.POST['token']
    this_user = User.objects.filter(token__token=this_token).get()
    if 'date' not in request.POST:
        now = datetime.now()
    Expense.objects.create(
        user=this_user, amount=request.POST['amount'], text=request.POST['text'], date=now)

    return JsonResponse({
        'status': 'ok',
    }, encoder=JSONEncoder)


@csrf_exempt
def submit_income(request):
    """ user submit an income """
    this_token = request.POST['token']
    this_user = User.objects.filter(token__token=this_token).get()
    if 'date' not in request.POST:
        now = datetime.now()
    Income.objects.create(
        user=this_user, amount=request.POST['amount'], text=request.POST['text'], date=now)

    return JsonResponse({
        'status': 'ok',
    }, encoder=JSONEncoder)
