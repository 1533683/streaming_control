from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
#from django.contrib.auth import update_session_auth_hash
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
#from rest_framework import status
import json
from accounts.user_info import *
from django.shortcuts import render, redirect
from accounts.models import *
#hash password
from django.contrib.auth.hashers import make_password


@require_http_methods(['GET', 'POST'])
@csrf_exempt
def log_in(request):
    if request.method=='POST':
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        user = authenticate(username=username, password=password)
        agrs = {}
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                request.session['has_commented'] = True 
                return HttpResponse(status=202)
        else:
            agrs["detail"] = "Incorect username or password!"
            messages = json.dumps(agrs)
            return HttpResponse(messages, content_type='application/json', status=203)
    '''User is realy login, logout user session'''
    log_out(request)
    return render_to_response('accounts/login.html')
    
def log_out(request):
    logout(request)
    response = HttpResponseRedirect('/accounts/login')
    response.delete_cookie('user_location')
    return response

@require_http_methods(['GET', 'POST'])
@csrf_exempt
def password_change(request):
    if request.method == 'POST':
        agrs = {}
        data = json.loads(request.body)
        oldpassword = data['oldpassword']
        newpassword = data['newpassword']
        retypepassword = data['retypepassword']
        #Check password input incorrect
        if newpassword != retypepassword:
            agrs["detail"] = "Sorry, passwords do not match!"
            messages = json.dumps(agrs)
            return HttpResponse(messages, content_type='application/json', status=203)
        #check new password whith current password
        username = request.user.username
        user = user = authenticate(username=username, password=oldpassword)
        if user is None:
            agrs["detail"] = "Sorry, password incorrect!"
            messages = json.dumps(agrs)
            return HttpResponse(messages, content_type='application/json', status=203)
        #Check new pass word  not same old password
        if newpassword == oldpassword:
            agrs["detail"] = "Sorry, new password same old password!"
            messages = json.dumps(agrs)
            return HttpResponse(messages, content_type='application/json', status=203)
        user = User.objects.get(pk=int(request.user.id))
        user.set_password('root')
        # users = user.save()
        # update_session_auth_hash(request, users)
        agrs["detail"] = "Password change sucessfuly!"
        messages = json.dumps(agrs)
        return HttpResponse(messages, content_type='application/json', status=202)
    else:
        return render_to_response('accounts/password_change.html')

@require_http_methods(['GET', 'POST'])
@csrf_exempt
def profile(request):
    return render_to_response('accounts/profile.html')
        
    

@require_http_methods(['GET'])
def profile_json(request):
    user = User.objects.get(pk=int(request.user.id))
    agrs = []
    agrs.append({
        'username'      : user.username,
        'email'         : user.email,
        'first_name'    : user.first_name,
        'last_name'     : user.last_name,
        'is_staff'      : user.is_staff,
        'is_active'     : user.is_active,
        'date_joined'   : str(user.date_joined),
        'last_login'    : str(user.last_login)
        })
    return HttpResponse(json.dumps(agrs), content_type='application/json', status=200)
    