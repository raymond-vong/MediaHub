
from django.shortcuts import render, redirect
import requests
import json
from .forms import *

URL = "http://localhost:8000/"

def index(request):
	return render(request, 'index.html')

def login(request):
	if request.method == 'GET':
		context = {"login_form":LoginForm()}
		return render(request, 'login.html', context)
	if request.method == 'POST':
		login_form = LoginForm(request.POST)
		if login_form.is_valid():
			r = requests.get(URL + "api/users/" + login_form["username"].value() + "/" + login_form["password"].value())

			if r.status_code == 200:
				response = json.loads(r.json())
				if response["valid"]:
					request.session["username"] = login_form["username"].value()
					return redirect(dashboard)
			return redirect(login)
		return redirect(login)
	return redirect(login)

def dashboard(request):
	try:
		if request.session["username"] != "":
			context = {"name":request.session["username"]}
			return render(request, 'dashboard.html', context)
		else:
			return redirect(login)
	except:
		return redirect(login)

def logout(request):
	request.session["username"] = ""
	return redirect(index)

def register(request):
	if request.method == 'GET':
		context = {"register_form":RegisterForm()}
		return render(request, 'register.html', context)
	if request.method == 'POST':
		register_form = RegisterForm(request.POST)
		if register_form.is_valid():
			details = dict()
			details["userID"] = register_form["username"].value()
			details["userName"] = register_form["name"].value()
			details["userPassword"] = register_form["password"].value()
			r = requests.post(URL + "api/users/", json=details)
			if r.status_code == 201:
				request.session["username"] = register_form["username"].value()
				return redirect(dashboard)
		return redirect(register)
	return redirect(register)
