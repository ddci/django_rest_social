from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from accounts.forms import LoginForm


def login_view(request):
    next_page = request.GET.get('next')
    title = "Login"
    form = LoginForm(request.POST or None)

    if request.user.is_authenticated:
        if next_page:
            return redirect(next_page)
        return redirect("/posts/")

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next_page:
            return redirect(next_page)
        return redirect("/posts/")
    return render(request, "accounts/login.html", {"form": form, "title": title})


def index_view(request):
    if request.user.is_authenticated:
        return redirect("/posts/")
    else:
        return redirect("/login/")
